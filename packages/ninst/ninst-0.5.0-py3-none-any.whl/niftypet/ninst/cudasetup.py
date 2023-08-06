#!/usr/bin/env python
"""Tools for CUDA compilation and set-up for Python 3."""
import importlib
import logging
import os
import platform
import re
import shutil
import sys
from distutils.sysconfig import get_python_inc
from subprocess import PIPE, run
from textwrap import dedent

# from pkg_resources import resource_filename
try:
    from numpy import get_include as get_numpy_inc
except ImportError:
    pass
else:
    nphdr = get_numpy_inc()  # numpy header path

log = logging.getLogger(__name__)

prefix = sys.prefix
pyhdr = get_python_inc()  # Python header paths
mincc = 35  # minimum required CUDA compute capability


def path_niftypet_local():
    """Get the path to the local (home) folder for NiftyPET resources."""
    # if using conda put the resources in the folder with the environment name
    if "CONDA_DEFAULT_ENV" in os.environ:
        try:
            env = re.findall(r"envs[/\\](.*)[/\\]bin[/\\]python", sys.executable)[0]
        except IndexError:
            env = os.environ["CONDA_DEFAULT_ENV"]
        log.info("install> conda environment found: {}".format(env))
    else:
        env = ""
    # create the path for the resources files according to the OS platform
    if platform.system() in ("Linux", "Darwin"):
        path_resources = os.path.expanduser("~")
    elif platform.system() == "Windows":
        path_resources = os.getenv("LOCALAPPDATA")
    else:
        raise ValueError("Unknown operating system: {}".format(platform.system()))
    path_resources = os.path.join(path_resources, ".niftypet", env)

    return path_resources


def find_cuda():
    """Locate the CUDA environment on the system."""
    # search the PATH for NVCC
    for fldr in os.environ["PATH"].split(os.pathsep):
        cuda_path = os.path.join(fldr, "nvcc")
        if os.path.exists(cuda_path):
            cuda_path = os.path.dirname(os.path.dirname(cuda_path))
            break
        cuda_path = None

    if cuda_path is None:
        log.warning("nvcc compiler could not be found from the PATH!")
        return

    # serach for the CUDA library path
    lcuda_path = os.path.join(cuda_path, "lib64")
    if "LD_LIBRARY_PATH" in os.environ:
        if lcuda_path in os.environ["LD_LIBRARY_PATH"].split(os.pathsep):
            log.info("found CUDA lib64 in LD_LIBRARY_PATH: {}".format(lcuda_path))
    elif os.path.isdir(lcuda_path):
        log.info("found CUDA lib64 in: {}".format(lcuda_path))
    else:
        log.warning("folder for CUDA library (64-bit) could not be found!")

    return cuda_path, lcuda_path


def dev_setup():
    """figure out what GPU devices are available and choose the supported ones."""
    log.info(
        dedent(
            """
            --------------------------------------------------------------
            Setting up CUDA ...
            --------------------------------------------------------------"""
        )
    )
    # check first if NiftyPET was already installed and use the choice of GPU
    path_resources = path_niftypet_local()
    # if so, import the resources and get the constants
    if os.path.isfile(os.path.join(path_resources, "resources.py")):
        resources = get_resources()
    else:
        log.error("resources file not found/installed.")
        return

    # get all constants and check if device is already chosen
    Cnt = resources.get_setup()
    if "CCARCH" in Cnt and "DEVID" in Cnt:
        log.info("using this CUDA architecture(s): {}".format(Cnt["CCARCH"]))
        return Cnt["CCARCH"]

    from miutil import cuinfo

    if "DEVID" in Cnt:
        ccstr = cuinfo.nvcc_flags(int(Cnt["DEVID"]))
        devid = Cnt["DEVID"]
    else:
        devid = cuinfo.num_devices() - 1
        if devid == -1:
            return ""
        ccstr = ";".join(set(map(cuinfo.nvcc_flags, range(devid + 1))))

    # passing this setting to resources.py
    fpth = os.path.join(
        path_resources, "resources.py"
    )  # resource_filename(__name__, 'resources/resources.py')
    with open(fpth, "r") as f:
        rsrc = f.read()
    # get the region of keeping in synch with Python
    i0 = rsrc.find("# # # start GPU properties # # #")
    i1 = rsrc.find("# # # end GPU properties # # #")
    # list of constants which will be kept in sych from Python
    cnt_dict = {"DEV_ID": str(devid), "CC_ARCH": repr(ccstr)}
    # update the resource.py file
    with open(fpth, "w") as f:
        f.write(rsrc[:i0])
        f.write("# # # start GPU properties # # #\n")
        for k, v in cnt_dict.items():
            f.write(k + " = " + v + "\n")
        f.write(rsrc[i1:])

    return ccstr


def resources_setup(gpu=True):
    """
    This function checks CUDA devices, selects some and installs resources.py
    """
    log.info("installing file <resources.py> into home directory if it does not exist.")
    path_current = os.path.dirname(os.path.realpath(__file__))
    # get the path to the local resources.py (on Linux machines it is in ~/.niftypet)
    path_resources = path_niftypet_local()
    log.info("current path: {}".format(path_current))

    # does the local folder for niftypet exists? if not create one.
    if not os.path.exists(path_resources):
        os.makedirs(path_resources)
    # is resources.py in the folder?
    if not os.path.isfile(os.path.join(path_resources, "resources.py")):
        if os.path.isfile(os.path.join(path_current, "raw", "resources.py")):
            shutil.copyfile(
                os.path.join(path_current, "raw", "resources.py"),
                os.path.join(path_resources, "resources.py"),
            )
        else:
            raise IOError("could not find <resources.py")
    else:
        log.info(
            "<resources.py> already found in local NiftyPET folder: {}".format(
                path_resources
            )
        )
        get_resources()

    # find available GPU devices, select one or more and output the compilation flags
    # return gpuarch for cmake compilation
    return dev_setup() if gpu else ""


def get_resources(sys_append=True, reload=True):
    path_resources = path_niftypet_local()
    if sys_append:
        if path_resources not in sys.path:
            sys.path.append(path_resources)
    try:
        import resources
    except ImportError:
        log.error(
            dedent(
                """\
        --------------------------------------------------------------------------
        NiftyPET resources file <resources.py> could not be imported.
        It should be in ~/.niftypet/resources.py (Linux) or
        in //Users//USERNAME//AppData//Local//niftypet//resources.py (Windows)
        but likely it does not exists.
        --------------------------------------------------------------------------"""
            )
        )
        raise
    else:
        return importlib.reload(resources) if reload else resources


def cmake_cuda(
    path_source, path_build, nvcc_flags="", logfile_prefix="py_", msvc_version=""
):
    # CUDA installation
    log.info(
        dedent(
            """
            --------------------------------------------------------------
            CUDA compilation
            --------------------------------------------------------------"""
        )
    )

    if not os.path.isdir(path_build):
        os.makedirs(path_build)
    path_current = os.path.abspath(os.curdir)
    try:
        os.chdir(path_build)

        # cmake installation commands
        cmds = [
            [
                "cmake",
                path_source,
                f"-DPython3_ROOT_DIR={sys.prefix}",
                f"-DCUDA_NVCC_FLAGS={nvcc_flags}",
            ],
            ["cmake", "--build", "./"],
        ]

        if platform.system() == "Windows":
            cmds[0] += ["-G", msvc_version]
            cmds[1] += ["--config", "Release"]

        # run commands with logging
        cmakelogs = [
            "{logfile_prefix}cmake_config.log",
            "{logfile_prefix}cmake_build.log",
        ]
        errs = False
        for cmd, cmakelog in zip(cmds, cmakelogs):
            log.info("Command:%s", cmd)
            p = run(cmd, stdout=PIPE, stderr=PIPE)
            stdout = p.stdout.decode("utf-8")
            stderr = p.stderr.decode("utf-8")

            with open(cmakelog, "w") as fd:
                fd.write(stdout)

            if p.returncode:
                errs = True

            log.info(
                dedent(
                    """
                    ----------- compilation output ----------
                    %s
                    ------------------ end ------------------"""
                ),
                stdout,
            )

            if p.stderr:
                log.error(
                    dedent(
                        """
                        --------------- process errors ----------------
                        %s
                        --------------------- end ---------------------"""
                    ),
                    stderr,
                )
        if errs:
            raise SystemError("compilation failed")
    finally:
        os.chdir(path_current)

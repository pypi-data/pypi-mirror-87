#!/usr/bin/env python3
"""initialise the NiftyPET ninst package"""
import platform

from tqdm.auto import tqdm

from . import cudasetup as cs
from . import install_tools as tls
from .install_tools import LOG_FORMAT

__all__ = [
    "LOG_FORMAT",
    "LogHandler",
    "path_resources",
    "resources",
    "dev_info",
    "gpuinfo",
]


class LogHandler(tls.LogHandler):
    """Custom formatting and tqdm-compatibility"""

    def handleError(self, record):
        super().handleError(record)
        raise IOError(record)

    def emit(self, record):
        """Write to tqdm's stream so as to not break progress-bars"""
        try:
            msg = self.format(record)
            tqdm.write(msg, file=self.stream, end=getattr(self, "terminator", "\n"))
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)


# log = logging.getLogger(__name__)
# technically bad practice to add handlers
# https://docs.python.org/3/howto/logging.html#library-config
# log.addHandler(LogHandler())  # do it anyway for convenience


path_resources = cs.path_niftypet_local()
resources = cs.get_resources()

if getattr(resources, "CC_ARCH", "") and platform.system() in ["Linux", "Windows"]:
    from .dinf import dev_info, gpuinfo
else:
    dev_info, gpuinfo = None, None

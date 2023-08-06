from niftypet.ninst.dinf import dev_info


def test_dev_info(capsys, nvml):
    devs = dev_info()
    out, err = capsys.readouterr()
    assert not any((out, err))
    dev_info(showprop=True)
    out, err = capsys.readouterr()
    assert not err
    assert not devs or out

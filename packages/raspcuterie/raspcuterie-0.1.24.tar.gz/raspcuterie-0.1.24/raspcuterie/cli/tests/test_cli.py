from .. import devices


def test_devices(runner):

    result = runner.invoke(devices, catch_exceptions=False)
    assert result.exit_code == 0, result.exception

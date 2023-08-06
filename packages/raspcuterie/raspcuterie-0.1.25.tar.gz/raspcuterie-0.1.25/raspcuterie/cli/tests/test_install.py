import sys

import pytest

from .. import install

if sys.platform.startswith("win"):
    pytest.skip("skipping windows", allow_module_level=True)


def test_cron(runner):
    result = runner.invoke(install.cron, catch_exceptions=False)
    assert result.exit_code == 0, result.exception


def test_systemd(runner):
    result = runner.invoke(install.systemd, catch_exceptions=False)
    assert result.exit_code == 0, result.exception

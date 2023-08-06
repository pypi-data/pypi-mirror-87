from .. import cron


def test_log_values(runner):
    result = runner.invoke(cron.log, catch_exceptions=False)
    assert result.exit_code == 0, result.exception

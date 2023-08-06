from .. import fake


def test_fake_humidity(runner):

    result = runner.invoke(fake.humidity, catch_exceptions=False)
    assert result.exit_code == 0, result.exception

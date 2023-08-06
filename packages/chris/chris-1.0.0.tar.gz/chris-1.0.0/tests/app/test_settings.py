import os
import pytest

from chris.app import settings


def get_settings():
    # Contains (setting variable name, environment variable name, variable default value)
    return [
        ('FLASK_RUN_PORT', settings.VAR_FLASK_RUN_PORT, settings.DEFAULT_FLASK_RUN_PORT),
        ('FLASK_DEBUG', settings.VAR_FLASK_DEBUG, settings.DEFAULT_FLASK_DEBUG),
        ('FLASK_HOST', settings.VAR_FLASK_HOST, settings.DEFAULT_FLASK_HOST),
        ('LOG_FILE_NAME', settings.VAR_LOG_FILE_NAME, settings.DEFAULT_LOG_FILE_NAME),
        ('INSTRUMENTATION_KEY', settings.VAR_INSTRUMENTATION_KEY, settings.DEFAULT_INSTRUMENTATION_KEY),
    ]


class TestSettings:

    @pytest.mark.parametrize('setting', get_settings())
    def test_settings(self, setting):
        setting_name, env_variable, default_value = setting
        if os.environ.get(env_variable) is None:
            assert getattr(settings, setting_name) == default_value
        else:
            assert getattr(settings, setting_name) == os.environ[env_variable]

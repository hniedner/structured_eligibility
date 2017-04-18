from flask import config
import os


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '2z54e22a-1r39-4319-b42a-t43cw3au3e5b'
    BOOTSTRAP_SERVE_LOCAL = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = False


config = {
    "development": "structured_eligibility.config.DevelopmentConfig",
    "testing": "structured_eligibility.config.TestingConfig",
    "default": "structured_eligibility.config.BaseConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
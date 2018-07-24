"""
# instance/config.py
# For environment configuration
# config.py
# contains environment settings
 """

class Config(object):
    """Sharing variables configs (cross origin etc)"""
    DEBUG = False
    CSRF_ENABLED = True


class DevelopmentConfig(Config):
    """Development environment variables config."""
    DEBUG = True


class ProductionConfig(Config):
    """Production environment variables config."""
    DEBUG = False
    TESTING = False


class TestConfig(Config):
    """Configurations for Testing, with its own database."""
    TESTING = True
    DEBUG = True

APP_CONFIG = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
}

#Configs for various environments
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    BASIC_AUTH_FORCE = True
    USERS_INFO = {}
    GLOBAL_INDEX = 0
    BASIC_AUTH_USERNAME = 'api-key'
    BASIC_AUTH_PASSWORD = 'generatesomesecurekeyforthis'
    BASIC_AUTH_REALM = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True

class TestingConfig(Config):
    TESTING = True

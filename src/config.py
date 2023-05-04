class Config():
    SECRET_KEY = 'B!weNAt1T^%kvhUI*S^'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'lara'
    MYSQL_PASSWORD = '123456'
    MYSQL_DB = 'bibliotecav'

config ={
    'development': DevelopmentConfig
}
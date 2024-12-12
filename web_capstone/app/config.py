import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'C6CPHairstyleRec2024')  
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql://C6CP:S.Tr.Kom2024@194.31.53.102/C6CP')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
#  'mysql://root:@localhost/tukang_cukur'
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True            # Gunakan TLS (True untuk 587)
    MAIL_USE_SSL = False           # Gunakan SSL (True untuk 465)
    MAIL_USERNAME = 'seriusblack65@gmail.com'  # Email pengirim
    MAIL_PASSWORD = 'waty zcke pvsq pney'  # Password email
    MAIL_DEFAULT_SENDER = 'seriusblack65@gmail.com'  #Default pengirim email

class DevelopmentConfig(Config):
    """Konfigurasi untuk pengembangan."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///dev.db')

class ProductionConfig(Config):
    """Konfigurasi untuk produksi."""
    DEBUG = False

class TestingConfig(Config):
    """Konfigurasi untuk pengujian."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///test.db')

# Gunakan ini di `app/__init__.py`
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}

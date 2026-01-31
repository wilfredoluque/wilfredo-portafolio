import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'luquemaytawilfredo@gmail.com'
    MAIL_PASSWORD = 'jqgz ayca gguh uhmz'
    MAIL_DEFAULT_SENDER = 'luquemaytawilfredo@gmail.com'  # Debe coincidir con Gmail


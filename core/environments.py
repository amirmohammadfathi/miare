from os import environ

DEBUG = bool(int(environ.get('DEBUG', 0)))
SECRET_KEY = environ.get('SECRET_KEY')
ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS', ' ').split()

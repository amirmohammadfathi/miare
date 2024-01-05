from os import environ
from dotenv import load_dotenv

load_dotenv()

DEBUG = bool(int(environ.get('DEBUG', 0)))
SECRET_KEY = environ.get('SECRET_KEY')
ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS', ' ').split()



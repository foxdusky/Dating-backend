import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

DB_CON_STR = os.getenv('DB_CON_STR')

PICTURES_DIR = os.getenv("PICTURES_DIR")

IS_DEV_ENV = int(os.getenv('IS_DEV_ENV'))

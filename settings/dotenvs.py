from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import os


def load_env_values():
    env_path = Path.cwd() / 'settings' / '.env'
    return load_dotenv(env_path) if env_path.exists() else False


load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

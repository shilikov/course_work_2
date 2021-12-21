from pathlib import Path
from dotenv import load_dotenv

def load_env_values():
    env_path = Path.cwd() / 'settings' / '.env'
    return load_dotenv(env_path) if env_path.exists() else False
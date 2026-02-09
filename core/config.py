'''
set enviroment settings
'''

'''
╭──────────────────────────────────────────────╮
│                  Import Modules              │
╰──────────────────────────────────────────────╯
'''

from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # mini_crm/



'''
╭──────────────────────────────────────────────╮
│                   Settings                   │
╰──────────────────────────────────────────────╯
'''

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str

    model_config = {
        "env_file":BASE_DIR / ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()
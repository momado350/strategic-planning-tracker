import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


def normalize_database_url(url: str | None) -> str:
    if not url:
        return f"sqlite:///{BASE_DIR / 'app.db'}"
    url = url.strip()
    if url.startswith('postgres://'):
        return url.replace('postgres://', 'postgresql+psycopg://', 1)
    if url.startswith('postgresql://') and '+psycopg' not in url:
        return url.replace('postgresql://', 'postgresql+psycopg://', 1)
    return url


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    SQLALCHEMY_DATABASE_URI = normalize_database_url(os.getenv('DATABASE_URL'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = None
    APP_NAME = 'Library Strategic Priorities Tracker'
    AUTO_CREATE_TABLES = os.getenv('AUTO_CREATE_TABLES', 'true').lower() == 'true'
    AUTO_SEED_DATA = os.getenv('AUTO_SEED_DATA', 'true').lower() == 'true'
    PREFERRED_URL_SCHEME = os.getenv('PREFERRED_URL_SCHEME', 'https')

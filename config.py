# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = 'uploads'
    PROCESSED_FOLDER = 'processed'
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    @staticmethod
    def init_app(app):
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.PROCESSED_FOLDER, exist_ok=True)

        if not Config.ANTHROPIC_API_KEY:
            raise ValueError("Anthropic APIキーが設定されていません。環境変数 'ANTHROPIC_API_KEY' を設定してください。")
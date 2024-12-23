import json
import os
from typing import Dict
from config import Config

class I18nManager:
    _instance = None
    _translations: Dict[str, Dict] = {}
    _current_language = Config.DEFAULT_LANGUAGE

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(I18nManager, cls).__new__(cls)
            cls._instance._load_translations()
        return cls._instance

    def _load_translations(self):
        for lang in Config.SUPPORTED_LANGUAGES:
            file_path = f"locales/{lang}/translation.json"
            with open(file_path, "r", encoding="utf-8") as f:
                self._translations[lang] = json.load(f)

    def set_language(self, language: str):
        if language in Config.SUPPORTED_LANGUAGES:
            self._current_language = language

    def get_text(self, key: str) -> str:
        return self._translations.get(self._current_language, {}).get(
            key, f"Missing translation: {key}"
        )

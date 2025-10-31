import os
import yaml

msg_dir = os.path.join(os.path.dirname(__file__), "lang")

class Language:
    def getLanguageFromKey(self, langCode: str, langKey: str) -> str:
        if not langCode or not isinstance(langCode, str):
            langCode = 'en'

        file_path = os.path.join(msg_dir, f"{langCode}.yaml")
        if not os.path.exists(file_path):
            file_path = os.path.join(msg_dir, "en.yaml")

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get(langKey)
import json
import os
from typing import Dict, Any, Optional

dat_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(dat_dir, exist_ok=True) 

SETTINGS = os.path.join(dat_dir,'user-settings.json')

class Main():
    def __init__(self):
        self._checkForFile()
        
    def _checkForFile(self):
        if not os.path.exists(SETTINGS):
            with open(SETTINGS,'w',encoding='utf-8') as f:
                json.dump({},f,indent=4)
    def _loadSettings(self) -> Dict[str,Any]:
        with open(SETTINGS,'r',encoding='utf-8') as f:
            return json.load(f)
    def _saveSettings(self, data:Dict[str,Any]):
        with open(SETTINGS, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def update(self, user_id: int, updates: Dict[str, Any]):
        all_data = self._loadSettings()
        str_id = str(user_id)

        if str_id not in all_data:
            self.createDefaults(user_id)
            all_data = self._loadSettings()

        if "preferences" not in all_data[str_id]:
            all_data[str_id]["preferences"] = {}

        for key, value in updates.items():
            if key in ["preferredLang", "firstMessageId"]:
                all_data[str_id][key] = value
            else:
                all_data[str_id]["preferences"][key] = value

        self._saveSettings(all_data)

    def createDefaults(self, user_id: int):
        data = self._loadSettings()
        string_id = str(user_id)

        if string_id in data:
            return False

        default_settings = {
            "ltsMessageId": None,
            "ltsChatId": None,
            "preferredLang": "en", # used for message editing
            "preferences": { # settings_obj['id']['preferences']['subsetting name'] OR user_settings['preferences']['subsetting name]
                "autodeleteTimer" : 30, # for autodeleting small messages, like success/error notifications, idk lol
                "onboardingStep" : "none"
            }
        }

        data[string_id] = default_settings
        self._saveSettings(data)
    
    def get_settings(self, user_id: int) -> Optional[Dict[str, Any]]:
        data = self._loadSettings()
        str_id = str(user_id)

        if str_id not in data:
            self.createDefaults(user_id)
            data = self._loadSettings()

        return data.get(str(user_id))

    def set_first_message_id(self, user_id: int, message_id: int, chat_id: int):
        data = self._loadSettings()
        str_id = str(user_id)

        if str_id not in data:
            self.createDefaults(user_id)
            data = self._loadSettings()

        data[str_id]["ltsMessageId"] = message_id
        data[str_id]["ltsChatId"] = chat_id
        self._saveSettings(data)
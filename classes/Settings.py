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

    def createDefaults(self, user_id: int) -> bool:
        data = self._loadSettings()
        string_id = str(user_id)

        if string_id in data:
            return False

        default_settings = {
            "firstMessageId": None, # used for message editing
            "subSettings": {
                # might be used later
            }
        }

        data[string_id] = default_settings
        self._saveSettings(data)
        return True
    
    def get_settings(self, user_id: int) -> Optional[Dict[str, Any]]:
        data = self._loadSettings()
        str_id = str(user_id)

        if str_id not in data:
            self.createDefaults(user_id)
            data = self._loadSettings()

        return data.get(str(user_id))

    def set_first_message_id(self, user_id: int, message_id: int):
        data = self._loadSettings()
        str_id = str(user_id)

        if str_id not in data:
            self.createDefaults(user_id)
            data = self._loadSettings()

        data[str_id]["firstMessageId"] = message_id
        self._saveSettings(data)
# type: ignore
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot
from typing import List, TypedDict

from classes.Language import Language
from classes.Settings import Main as Settings

class ButtonInfo(TypedDict):
    ButtonTextKey: str
    ButtonCallback: str

l = Language()
s = Settings()

class Main:
    def __init__(self, bot: TeleBot):
        self.instance = bot

    def _ensure_first_message(self, message: Message) -> int:
        user_id = message.from_user.id
        user_settings = s.get_settings(user_id)
        first_msg_id = user_settings.get("firstMessageId")

        if not first_msg_id:
            sent = self.instance.send_message(
                chat_id=message.chat.id,
                text="👀"
            )
            s.set_first_message_id(user_id, sent.id)
            return sent.id
        return first_msg_id

    def _make_button(self, lang_code: str, text_key: str, callback: str) -> InlineKeyboardButton:
        text = l.getLanguageFromKey(langCode=lang_code, langKey=text_key)
        return InlineKeyboardButton(text, callback_data=callback)

    def updateMessage( # major part of this function has been cleaned up by an AI
        self,           # have I ensured that it still works correctly? Yes.
        message: Message,# as much as I'd like to not use AI, its 4 in the morning.
        updateTextWith: str,# i'd rather have 20 minutes more sleep than not use AI
        updateMarkupWith: List[List[ButtonInfo]]
    ) -> None:
        user_id = message.from_user.id
        chat_id = message.chat.id
        lang_code = message.from_user.language_code or "en"

        message_id = self._ensure_first_message(message)

        markup = InlineKeyboardMarkup()
        for button_row in updateMarkupWith:
            buttons = [
                self._make_button(lang_code, btn["ButtonTextKey"], btn["ButtonCallback"])
                for btn in button_row
            ]
            markup.row(*buttons) 

        try:
            self.instance.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=updateTextWith,
                reply_markup=markup
            )
        except Exception as e:
            print(f"⚠️ Failed to update message {message_id} for user {user_id}: {e}")
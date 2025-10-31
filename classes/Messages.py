# type: ignore
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiTelegramException
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

    def _ensure_first_message(self, user_id: int, chat_id: int) -> int:
        user_settings = s.get_settings(user_id)
        first_msg_id = user_settings.get("ltsMessageId")
        first_chat_id = user_settings.get("ltsChatId")

        if not first_msg_id or (chat_id != first_chat_id):
            sent = self.instance.send_message(
                chat_id=chat_id,
                text="👀"
            )
            s.set_first_message_id(user_id, sent.id, sent.chat.id)
            return sent.id
        return first_msg_id

    def _make_button(self, lang_code: str, text_key: str, callback: str) -> InlineKeyboardButton:
        text = l.getLanguageFromKey(langCode=lang_code, langKey=text_key)
        return InlineKeyboardButton(text, callback_data=callback)

    def updateMessage(
        self,
        user_id: int,
        chat_id: int,  # needed for sending/editing
        updateTextWith: str,
        updateMarkupWith: List[List[ButtonInfo]],
        isOnboarding: bool = False
    ) -> None:
        user_settings = s.get_settings(user_id)
        lang_code = user_settings['preferredLang']
        if isOnboarding:
            # During onboarding, we may not have saved preferredLang yet
            # So we fall back to Telegram's reported language
            # But note: we can't get it without a Message or User object!
            # → So we must pass it explicitly or store it early
            pass  # We'll handle this below

        message_id = self._ensure_first_message(user_id, chat_id)

        markup = InlineKeyboardMarkup()
        for button_row in updateMarkupWith:
            buttons = [
                self._make_button(lang_code, btn["ButtonTextKey"], btn["ButtonCallback"])
                for btn in button_row
            ]
            markup.row(*buttons)

        text = l.getLanguageFromKey(langCode=lang_code, langKey=updateTextWith)
        if text is None:
            text = "⚠️ Missing translation for key: " + updateTextWith

        try:
            self.instance.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=markup,
                parse_mode="markdown"
            )
        except ApiTelegramException as e:
            if e.error_code == 400 and "message to edit not found" in e.description.lower():
                print(f"Message {message_id} deleted, user {user_id}. Sending new message.")
                new_message = self.instance.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=markup,
                    parse_mode="markdown"
                )
                s.set_first_message_id(user_id, new_message.id, new_message.chat.id)
            else:
                print(f"API error, user {user_id}: {e}")
                raise
        except Exception as e:
            print(f"Unexpected error, user {user_id}: {e}")

    def updateMessageWithLang(
        self,
        user_id: int,
        chat_id: int,
        lang_code: str,
        updateTextWith: str,
        updateMarkupWith: List[List[ButtonInfo]]
    ) -> None:
        message_id = self._ensure_first_message(user_id, chat_id)

        markup = InlineKeyboardMarkup()
        for button_row in updateMarkupWith:
            buttons = [
                self._make_button(lang_code, btn["ButtonTextKey"], btn["ButtonCallback"])
                for btn in button_row
            ]
            markup.row(*buttons)

        text = l.getLanguageFromKey(langCode=lang_code, langKey=updateTextWith)
        if text is None:
            text = "⚠️ Missing translation for key: " + updateTextWith

        try:
            self.instance.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=markup
            )
        except ApiTelegramException as e:
            if e.error_code == 400 and "message to edit not found" in e.description.lower():
                new_message = self.instance.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=markup
                )
                s.set_first_message_id(user_id, new_message.id, new_message.chat.id)
            else:
                raise
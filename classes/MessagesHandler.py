# type: ignore
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot

from classes.Language import Language

# Initialize the shared language handler
l = Language()


class Main:
    def __init__(self, bot: TeleBot):
        self.instance = bot
        # No need to manage language files here — delegate to Language class

    def startMessage(self, message: Message):
        try:
            lang_code = message.from_user.language_code

            # Use the Language class method (note: correct method name!)
            msg_data = l.getLanguageFromKey(langCode=lang_code, langKey="start_message")
            if msg_data and "text" in msg_data:
                welcome_text = msg_data["text"]
            else:
                welcome_text = """🎉 Welcome to My Bot!\n\nUse /help to see all available commands."""

            self.instance.send_message(message.chat.id, welcome_text)
            return True, None

        except Exception as e:
            return False, str(e)

    def settingsMessage(self, message: Message):
        try:
            lang_code = message.from_user.language_code

            # Fetch the entire 'settings_message' dict
            settings_data = l.getLanguageFromKey(langCode=lang_code, langKey="settings_message")
            
            # Fallback if key not found
            if not settings_data:
                settings_data = {
                    "text": "⚙️ Settings",
                    "button_row1_left": "Language",
                    "button_row1_right": "Notifications",
                    "button_row2_center": "Advanced Settings",
                    "button_row3_left": "Help",
                    "button_row3_right": "About"
                }

            markup = InlineKeyboardMarkup()

            # Row 1
            btn1 = InlineKeyboardButton(settings_data["button_row1_left"], callback_data="lang")
            btn2 = InlineKeyboardButton(settings_data["button_row1_right"], callback_data="notif")
            markup.row(btn1, btn2)

            # Row 2
            big_btn = InlineKeyboardButton(settings_data["button_row2_center"], callback_data="advanced")
            markup.row(big_btn)

            # Row 3
            btn3 = InlineKeyboardButton(settings_data["button_row3_left"], callback_data="help")
            btn4 = InlineKeyboardButton(settings_data["button_row3_right"], callback_data="about")
            markup.row(btn3, btn4)

            self.instance.send_message(
                message.chat.id,
                settings_data.get("text", "⚙️ Settings"),
                reply_markup=markup
            )
            return True, None

        except Exception as e:
            return False, str(e)
# type: ignore
from telebot import types as tl
from telebot.types import CallbackQuery as call
import telebot, os, time, asyncio
from dotenv import load_dotenv
from classes.Language import Language
from classes.Settings import Main as Settings

from classes.Messages import Main as m

load_dotenv()

BOT_TOKEN = os.getenv('TKN')

# i couldnt be bothered to make .env file
# so i have to go along with this. I dont mind though.
bot = telebot.TeleBot(token=BOT_TOKEN)
Messages = m(bot)

l = Language()
s = Settings()

ONBOARDING_STEP_LANGUAGE = "select_language"
ONBOARDING_STEP_AUTODELETE = "select_autodelete"
ONBOARDING_STEP_DONE = "done"

@bot.message_handler(commands=['start'])
def handle_start(message: tl.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    user_settings = s.get_settings(user_id)
    onboarding_done = user_settings["preferences"]["onboardingStep"]

    telegram_lang = message.from_user.language_code or 'en'
    if not user_settings.get("telegramLang"):
        s.update(user_id, {"telegramLang": telegram_lang})

    if onboarding_done == "done":
        Messages.updateMessage(
            user_id=user_id,
            chat_id=chat_id,
            updateTextWith="main_menu",
            updateMarkupWith=[
                [{"ButtonTextKey": "btn_help", "ButtonCallback": "settings"}]
            ]
        )
        return

    s.update(user_id, {"onboardingStep": ONBOARDING_STEP_LANGUAGE})

    Messages.updateMessage(
        user_id=user_id,
        chat_id=chat_id,
        updateTextWith="onboarding_ask_language",
        updateMarkupWith=[
            [
                {"ButtonTextKey": "lang_en", "ButtonCallback": "onb_lang_en"},
                {"ButtonTextKey": "lang_es", "ButtonCallback": "onb_lang_es"}
            ],
            [
                {"ButtonTextKey": "lang_ru", "ButtonCallback": "onb_lang_ru"},
            ]
        ],isOnboarding=True
    )
    return

#region Onboarding Stuff

@bot.callback_query_handler(func=lambda call: call.data.startswith("onb_lang_")) # onboarding process
def handle_language_select(call: tl.CallbackQuery):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    lang_code = call.data.split("_", 2)[-1]

    s.update(user_id, {
        "preferredLang": lang_code,
        "onboardingStep": ONBOARDING_STEP_AUTODELETE
    })

    Messages.updateMessageWithLang(
        user_id=user_id,
        chat_id=chat_id,
        lang_code=lang_code,
        updateTextWith="onboarding_ask_autodelete",
        updateMarkupWith=[
            [
                {"ButtonTextKey": "timer_5s", "ButtonCallback": "onb_timer_5"},
                {"ButtonTextKey": "timer_30s", "ButtonCallback": "onb_timer_30"}
            ],
            [
                {"ButtonTextKey": "timer_1m", "ButtonCallback": "onb_timer_60"},
                {"ButtonTextKey": "timer_5m", "ButtonCallback": "onb_timer_300"}
            ],
            [
                {"ButtonTextKey": "timer_10m", "ButtonCallback": "onb_timer_600"}
            ]
        ]
    )
    return

@bot.callback_query_handler(func=lambda call: call.data.startswith("onb_timer_")) # onboarding process
def handle_autodelete_select(call: tl.CallbackQuery):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    timer_val = call.data.split("_", 2)[-1]

    s.update(user_id, {
        "autodeleteTimer": timer_val,
        "wentThoughOnboarding": True,
        "onboardingStep": ONBOARDING_STEP_DONE
    })

    lang_code = s.get_settings(user_id)['preferredLang']
    Messages.updateMessageWithLang(
        user_id=user_id,
        chat_id=chat_id,
        lang_code=lang_code,
        updateTextWith="onboarding_complete",
        updateMarkupWith=[
            [{"ButtonTextKey": "btn_finish", "ButtonCallback": "onb_finish"}]
        ]
    )
    return

@bot.callback_query_handler(func=lambda call: call.data == "onb_finish") # onboarding process
def handle_finish(call: tl.CallbackQuery):
    bot.answer_callback_query(call.id)
    
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=l.getLanguageFromKey(s.get_settings(call.from_user.id)["preferredLang"],'finalizing')
    )
    time.sleep(3)
    bot.delete_message(call.message.chat.id,call.message.message_id)
    Messages.updateMessage(
            user_id=call.from_user.id,
            chat_id=call.message.chat.id,
            updateTextWith="main_menu",
            updateMarkupWith=[
                [{"ButtonTextKey": "btn_help", "ButtonCallback": "settings"}]
            ]
        )
    return

#region Main Query Handlers

@bot.callback_query_handler(func=lambda call: call.data == "settings")
def handle_settings(call: tl.CallbackQuery):
    print('processing.')

    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    Messages.updateMessage(user_id,chat_id,"help_message",[
        [
            {"ButtonTextKey": "help_lang", 
             "ButtonCallback": "help_lang_change"},  
            {"ButtonTextKey": "help_autodelete", 
             "ButtonCallback": "help_auto_change"},  
        ],
        [
            {"ButtonTextKey":"btn_back",
             "ButtonCallback":"back_menu"}
        ]
    ])
    return

@bot.callback_query_handler(func=lambda call: call.data.startswith('help_'))
def handle_help(call:tl.CallbackQuery):
    bot.answer_callback_query(call.id)
    data = call.data

    setting = data.split('_')[-1]
    if setting == 'auto':
        Messages.updateMessage(
            call.from_user.id,
            call.message.chat.id,
            'help_lang',
            [
                [
                    {"ButtonTextKey": "lang_ru", 
                    "ButtonCallback": "help_ru"},  
                    {"ButtonTextKey": "lang_en", 
                    "ButtonCallback": "help_en"},  
                ],
                [
                    {"ButtonTextKey": "lang_es", 
                    "ButtonCallback": "help_es"},  
                    {"ButtonTextKey": "btn_back", 
                    "ButtonCallback": "back_help"},  
                ],
            ]
        )


    if setting in ['en','es','ru']:
        langKey = "lang_".join(setting)
        langMessage = l.getLanguageFromKey(s.get_settings(call.from_user.id)['preferredLang'],'feedbackLang200')
        langLang = l.getLanguageFromKey(s.get_settings(call.from_user.id)['preferredLang'],langKey)

        langJoined = str(langMessage)+str(langLang)

        feedback = bot.send_message(call.message.chat.id,langJoined)
        s.update(call.from_user.id, {
            "preferredLang": setting
        })
        time.sleep(int(s.get_settings(call.from_user.id)['preferences']['autodeleteTimer']))

        bot.delete_message(feedback.chat.id,feedback.id)

    return

@bot.callback_query_handler()
def PrintCallbacks(call:tl.CallbackQuery):
    return print(call.data) # for debug

if __name__=='__main__':
    bot.polling(non_stop=True)
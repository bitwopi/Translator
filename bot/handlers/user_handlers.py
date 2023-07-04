import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot.keyboards import reply
from bot.services.translator import transfer
from bot.services.orm_engine import save_current_user_lang, get_user_current_language
from bot.services.orm_engine import get_user_history, save_translation_to_history, delete_user_history
from bot.states.user_states import LangStates

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Starts communication with user
async def user_start(message: types.Message):
    text = "Hi, I'm Translator and i do what i do - translating\nTo start translating please choose one of languages"
    await LangStates.LANG_CHANGED.set()
    await message.answer(text, reply_markup=reply.get_reply_lang_keyboard())


# Change user current language
async def change_lang(message: types.Message, state: FSMContext):
    lang_code = message.text.lower()[:2]
    response = save_current_user_lang(user_id=message.from_user.id, current_lang_code=lang_code)
    if not response:
        logger.info("User successfully set new language")
        await message.answer("Language successfully set", reply_markup=reply.get_reply_home_keyboard())
        await LangStates.LANG_SET.set()
    else:
        logger.warning("Failed during changing language")
        await message.answer("Something went wrong", reply_markup=reply.get_reply_home_keyboard())
        await state.finish()


# Translates message text to current user language
async def translate(message: types.Message):
    text = message.text
    lang_code = get_user_current_language(message.from_user.id)[0]
    try:
        transfer_data = await transfer(target_lang=lang_code, text=text)
        translated_text = transfer_data[0]['text']
        detected_code = transfer_data[0]['detectedLanguageCode']
        if not save_translation_to_history(message.from_user.id, detected_code, text, lang_code, translated_text):
            await message.reply(translated_text)
            logger.info("Text successfully translated")
        else:
            await message.reply("Sorry, I can't translate it(")
    except IndexError:
        logger.warning("Failed during translating text")
        await message.reply("It looks like you choose incorrect language, pls change it.",
                            reply_markup=reply.get_reply_lang_keyboard())
        await LangStates.LANG_CHANGED.set()


async def choose_feature(message: types.Message, state: FSMContext):
    text = message.text
    if text == "Change language ✏️":
        await state.set_state(LangStates.LANG_CHANGED)
        await message.answer("You can choose one of the optional language or type your own.\nIt could looks like 'en'.",
                             reply_markup=reply.get_reply_lang_keyboard())
    elif text == "Show history 🕑":
        await show_user_history(message)
    elif text == "Clear history 🧹":
        await clear_user_history(message)
    else:
        await translate(message)


# Replies user if he must set new language
async def std_reply(message: types.Message, state: FSMContext):
    if get_user_current_language(message.from_user.id):
        await LangStates.LANG_SET.set()
        await choose_feature(message, state)
    else:
        await LangStates.LANG_CHANGED.set()
        await message.answer("Please choose target language", reply_markup=reply.get_reply_lang_keyboard())


# Shows user's history
async def show_user_history(message: types.Message):
    data = get_user_history(message.from_user.id)
    text = ""
    if data:
        for obj in data:
            text += obj.__repr__()
        await message.reply(text)
    else:
        await message.answer("I haven't translated for you earlier. Lets do this 💪")


# Clears user's history
async def clear_user_history(message: types.Message):
    if not delete_user_history(message.from_user.id):
        await message.answer("Your history successfully cleared.\nDon't worry)")
        logger.info("User history successfully cleared")
    else:
        await message.answer("Sorry, but there's nothing to clear.")
        logger.warning("Failed during deleting user history")


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*", content_types=['text'])
    dp.register_message_handler(change_lang, state=LangStates.LANG_CHANGED, content_types=['text'])
    dp.register_message_handler(choose_feature, state=LangStates.LANG_SET, content_types=['text'])
    dp.register_message_handler(std_reply, state=None, content_types=['text'])

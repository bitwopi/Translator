from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def get_reply_lang_keyboard():
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton("en 🇬🇧"),
        KeyboardButton("ru 🇷🇺"),
        KeyboardButton("es 🇪🇸"),
        KeyboardButton("ja 🇯🇵"),
        KeyboardButton("zh 🇨🇳"),
        KeyboardButton("de 🇩🇪"),
    ]
    for button in buttons:
        reply_markup.insert(button)
    return reply_markup


def get_reply_home_keyboard():
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton("Change language ✏️"),
        KeyboardButton("Show history 🕑"),
        KeyboardButton("Clear history 🧹"),
    ]
    for button in buttons:
        reply_markup.insert(button)
    return reply_markup

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = [[
    KeyboardButton(text='test')
]]
keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
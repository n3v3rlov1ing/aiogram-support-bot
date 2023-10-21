from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


kb_profile = [
        [
        KeyboardButton(text='Создать тикет')
    ],
    [
        KeyboardButton(text='Мои запросы')
    ]]
keyboard_profile = ReplyKeyboardMarkup(keyboard=kb_profile, resize_keyboard=True, one_time_keyboard=True)

kb_priority = [
        [
        KeyboardButton(text='Низкий')
    ],
    [
        KeyboardButton(text='Средний')
    ],
    [
        KeyboardButton(text='Высокий')
    ]]
keyboard_priority = ReplyKeyboardMarkup(keyboard=kb_priority, resize_keyboard=True, one_time_keyboard=True)

kb_admin = [
        [
        KeyboardButton(text='Неотвеченные тикеты')
    ],
    [
        KeyboardButton(text='Рассылка')
    ]]
keyboard_admin = ReplyKeyboardMarkup(keyboard=kb_admin, resize_keyboard=True, one_time_keyboard=True)

kb_return = [
        [
        KeyboardButton(text='Профиль')
    ]]
keyboard_return = ReplyKeyboardMarkup(keyboard=kb_return, resize_keyboard=True, one_time_keyboard=True)
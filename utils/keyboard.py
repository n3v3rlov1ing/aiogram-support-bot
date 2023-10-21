from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


kb_profile = [
        [
        KeyboardButton(text='Создать тикет')
    ],
    [
        KeyboardButton(text='Мои запросы')
    ],
    [
        KeyboardButton(text='О боте')
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
    ],
    [
        KeyboardButton(text='Профиль')
    ],
    [
        KeyboardButton(text='Ответить на запрос')
    ],
    [
        KeyboardButton(text='О боте')
    ]]
keyboard_admin = ReplyKeyboardMarkup(keyboard=kb_admin, resize_keyboard=True)


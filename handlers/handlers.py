from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from utils.config import admin_id, username, links
from aiogram.fsm.context import FSMContext
from utils.states import Distribution, Ticket, AnswerTicket
from db import Database
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import ExceptionMessageFilter
from utils.keyboard import *
from utils.filters import IsAdmin

db = Database()
handler = Router()

@handler.message(Command('start'))
async def cmd_start(message: Message):
    kb = [[
        KeyboardButton(text='Профиль')
    ]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    if db.user_exist(message.from_user.id) == True:
        await message.answer(f'Привет, {message.from_user.first_name}', reply_markup=keyboard)
    else:
        db.reg_user(message.from_user.id)
        await message.answer(f'{message.from_user.first_name}, вы были успешно зарегистрированы!')

@handler.message(Command('send'), IsAdmin())
@handler.message(F.text == 'Рассылка')
async def cmd_admin(message: Message, state: FSMContext):
    await state.set_state(Distribution.text)
    await message.answer('Введите текст рассылки')

@handler.message(Distribution.text)
async def load_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer('Укажите фото. 0 - для рассылки без фотографии.')
    await state.set_state(Distribution.photo)

@handler.message(Distribution.photo)
async def load_photo(message: Message, state: FSMContext, bot: Bot):
    if message.text == '0':
        errors = 0
        user_data = await state.get_data()
        text = user_data['text']
        for i in db.get_users():
            try:
                await bot.send_message(i[0], text)
            except Exception as e:
                errors += 1
        await message.answer(f'Рассылка завершена!\n\nУдачно: {db.count_users()-errors}')
        
    else:
        errors = 0
        file_id = message.photo[-1].file_id
        await state.update_data(photo=file_id)
        user_data = await state.get_data()
        text = user_data['text']
        photo = user_data['photo']
        try:
                for i in db.get_users():
                    try:
                        await bot.send_photo(i[0], photo, caption=text)
                    except Exception as e:
                        errors += 1
        except TypeError:
            await message.answer('Загрузите фото еще раз!')
            await state.set_state(Distribution.photo)
        await message.answer(f'Рассылка завершена!\nПолучено: {db.count_users()-errors}')
        await state.clear()

@handler.message(Command('admin'), IsAdmin())
async def cmd_admin(message: Message):
    kb = [[
        KeyboardButton(text='Рассылка'),
    ],
    [
        KeyboardButton(text='Статистика')
    ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Добро пожаловать в админ-панель!', reply_markup=keyboard)


@handler.message(F.text == 'Статистика', IsAdmin())
async def cmd_stats(message: Message):
    await message.answer(f'Статистика бота:\nПользователей: {db.count_users()}')

@handler.message(F.text == 'Профиль', IsAdmin())
@handler.message(Command('profile'))
async def cmd_stats(message: Message):
    await message.answer(f'Профиль {message.from_user.first_name}:\n\nID: {message.from_user.id}\nСтатус: Администратор', reply_markup=keyboard_admin)

@handler.message(F.text == 'Профиль')
@handler.message(Command('profile'))
async def cmd_profile(message: Message):
    await message.answer(f'Профиль {message.from_user.first_name}:\n\nID: {message.from_user.id}', reply_markup=keyboard_profile)

@handler.message(F.text == 'Создать тикет')
async def cmd_create_ticket(message: Message, state: FSMContext):
    await message.answer('Введите сообщение для администратора')
    await state.set_state(Ticket.text)

@handler.message(Ticket.text)
async def load_ticket_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Ticket.priority)
    await message.answer('Выберите приоритет ответа', reply_markup=keyboard_priority)

@handler.message(Ticket.priority)
async def load_ticket_priority(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(priority=message.text)
    await message.answer('Ваш тикет успешно отправлен!', reply_markup=keyboard_profile)
    data = await state.get_data()
    text = data['text']
    priority = data['priority']
    db.reg_ticket(message.from_user.id, text, priority)
    await bot.send_message(admin_id, f'Запрос №{db.get_info2(message.from_user.id)} от @{message.from_user.username}\n\nЗапрос: {text}\nПриоритет ответа: {priority}')
    await state.clear()

@handler.message(F.text == 'Мои запросы')
async def cmd_mytickets(message: Message):
    result = ''
    for i in db.get_info(message.from_user.id):
        result += f'ID: {i[0]}\nТекст: {i[1]}\nПриоритет: {i[2]}\nОтвет: {i[3]}\n\n'
    await message.answer(result)


@handler.message(F.text == 'Ответить на запрос', IsAdmin())
async def cmd_unanswered_tickets(message: Message, state: FSMContext):
    await state.set_state(AnswerTicket.id)
    await message.answer('Введите ID запроса для ответа')
        
@handler.message(AnswerTicket.id)
async def load_ticket_id(message: Message, state: FSMContext):
    await state.update_data(id = message.text)
    user_data = await state.get_data()
    req_id = user_data['id']
    info = db.get_info_byid(req_id)
    if db.is_answered(req_id) == True:
        await message.answer('Вы уже отвечали на данный запрос!', reply_markup=keyboard_admin)
    else:
        await message.answer(f'Запрос №{req_id}\n\nВопрос: {info[0]}\nПриоритет: {info[1]}')
        await message.answer(f'Введите ответ на запрос №{req_id}')
        await state.set_state(AnswerTicket.text)


@handler.message(AnswerTicket.text)
async def load_ticket_id(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(text = message.text)
    user_data = await state.get_data()
    req_id = user_data['id']
    text = user_data['text']
    db.answer_ticket(text, req_id)
    await message.answer(f'Ответ на запрос №{req_id} успешно отправлен!\n\nТекст: {text}', reply_markup=keyboard_admin)
    user_id = db.get_info_byid(req_id)[3]
    id = db.get_info_byid(req_id)[0]
    await bot.send_message(user_id, f'Поступил ответ от администратора:\n\nID:{id}\nОтвет: {text}')
    await state.clear()


@handler.message(F.text == 'Неотвеченные тикеты')
async def cmd_unanswered_tickets(message: Message):
    # if isadmin(message.from_user.id) == True:
        result = ''
        for i in db.get_un_answered_tickets():
            result += f'ID: {i[0]}\nТекст: {i[1]}\nПриоритет: {i[2]}\n\n'
        await message.answer(result)

@handler.message(F.text == 'О боте')
async def cmd_unanswered_tickets(message: Message):
    await message.answer(f'Создатель бота: {username}\n\nДополнительные ссылки: {links}')




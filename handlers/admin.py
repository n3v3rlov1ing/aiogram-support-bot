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
admin_router = Router()

@admin_router.message(F.text == 'Отмена', IsAdmin())
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer('Действие отменено!', reply_markup=keyboard_admin)


@admin_router.message(Command('send'), IsAdmin())
@admin_router.message(F.text == 'Рассылка', IsAdmin())
async def cmd_admin(message: Message, state: FSMContext):
    await state.set_state(Distribution.text)
    await message.answer('Введите текст рассылки', reply_markup=keyboard_cancel)

@admin_router.message(Distribution.text)
async def load_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer('Укажите фото. 0 - для рассылки без фотографии.', reply_markup=keyboard_cancel)
    await state.set_state(Distribution.photo)

@admin_router.message(Distribution.photo)
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

@admin_router.message(Command('admin'), IsAdmin())
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


@admin_router.message(F.text == 'Статистика', IsAdmin())
async def cmd_stats(message: Message):
    await message.answer(f'Статистика бота:\nПользователей: {db.count_users()}')

@admin_router.message(F.text == 'Профиль', IsAdmin())
@admin_router.message(Command('profile'), IsAdmin())
async def cmd_stats(message: Message):
    await message.answer(f'Профиль {message.from_user.first_name}:\n\nID: {message.from_user.id}\nСтатус: Администратор', reply_markup=keyboard_admin)




@admin_router.message(F.text == 'Ответить на запрос', IsAdmin())
async def cmd_unanswered_tickets(message: Message, state: FSMContext):
    await state.set_state(AnswerTicket.id)
    await message.answer('Введите ID запроса для ответа', reply_markup=keyboard_cancel)
        
@admin_router.message(AnswerTicket.id)
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


@admin_router.message(AnswerTicket.text)
async def load_ticket_id(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(text = message.text)
    user_data = await state.get_data()
    req_id = user_data['id']
    text = user_data['text']
    db.answer_ticket(text, req_id)
    await message.answer(f'Ответ на запрос №{req_id} успешно отправлен!\n\nТекст: {text}', reply_markup=keyboard_admin)
    user_id = db.get_info_byid(req_id)[3]
    id = db.get_info_byid(req_id)[0]
    await bot.send_message(user_id, f'Поступил ответ от администратора:\n\nВаш вопрос: {text}\nID: {id}\nОтвет: {text}')
    await state.clear()


@admin_router.message(F.text == 'Неотвеченные тикеты', IsAdmin())
async def cmd_unanswered_tickets(message: Message):
    result = ''
    for i in db.get_un_answered_tickets():
        result += f'ID: {i[0]}\nТекст: {i[1]}\nПриоритет: {i[2]}\n\n'
    await message.answer(result)






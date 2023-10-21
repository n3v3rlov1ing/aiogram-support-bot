from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import Distribution, Ticket, AnswerTicket
from db import Database
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.keyboard import *
from utils.config import admin_id


db = Database()
user_router = Router()


@user_router.message(F.text == 'Отмена')
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer('Действие отменено!', reply_markup=keyboard_profile)


@user_router.message(Command('start'))
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


@user_router.message(F.text == 'Профиль')
@user_router.message(Command('profile'))
async def cmd_profile(message: Message):
    await message.answer(f'Профиль {message.from_user.first_name}:\n\nID: {message.from_user.id}', reply_markup=keyboard_profile)


@user_router.message(F.text == 'Создать тикет')
async def cmd_create_ticket(message: Message, state: FSMContext):
    await message.answer('Введите сообщение для администратора', reply_markup=keyboard_cancel)
    await state.set_state(Ticket.text)

@user_router.message(Ticket.text)
async def load_ticket_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Ticket.priority)
    await message.answer('Выберите приоритет ответа', reply_markup=keyboard_priority)

@user_router.message(Ticket.priority)
async def load_ticket_priority(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(priority=message.text)
    await message.answer('Ваш тикет успешно отправлен!', reply_markup=keyboard_profile)
    data = await state.get_data()
    text = data['text']
    priority = data['priority']
    db.reg_ticket(message.from_user.id, text, priority)
    await bot.send_message(admin_id, f'Запрос №{db.get_info2(message.from_user.id)} от @{message.from_user.username}\n\nЗапрос: {text}\nПриоритет ответа: {priority}')
    await state.clear()


@user_router.message(F.text == 'Мои запросы')
async def cmd_mytickets(message: Message):
    result = ''
    for i in db.get_info(message.from_user.id):
        result += f'ID: {i[0]}\nТекст: {i[1]}\nПриоритет: {i[2]}\nОтвет: {i[3]}\n\n'
    await message.answer(result)

@user_router.message(F.text == 'О боте')
async def cmd_unanswered_tickets(message: Message):
    await message.answer(f'Создатель бота: {username}\n\nДополнительные ссылки: {links}')
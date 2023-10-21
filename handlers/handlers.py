from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from utils.config import admin_id
from aiogram.fsm.context import FSMContext
from utils.states import Distribution
from db import Database
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import ExceptionMessageFilter

db = Database()
handler = Router()

def isadmin(id):
    return bool(id==admin_id)

@handler.message(Command('start'))
async def cmd_start(message: Message):
    if db.user_exist(message.from_user.id) == True:
        await message.answer(f'Привет, {message.from_user.first_name}')
    else:
        db.reg_user(message.from_user.id)
        await message.answer(f'{message.from_user.first_name}, вы были успешно зарегистрированы!')

@handler.message(Command('send'))
@handler.message(F.text == 'Рассылка')
async def cmd_admin(message: Message, state: FSMContext):
    if message.from_user.id == admin_id:
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
        await message.answer(f'Рассылка завершена!\nПолучено: {db.get_users()-errors}')
        await state.clear()

@handler.message(Command('admin'))
async def cmd_admin(message: Message):
    if message.from_user.id == admin_id:
        kb = [[
            KeyboardButton(text='Рассылка'),
        ],
        [
            KeyboardButton(text='Статистика')
        ]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Вы админ', reply_markup=keyboard)


@handler.message(F.text == 'Статистика')
async def cmd_stats(message: Message):
    if isadmin(message.from_user.id) == True:
        await message.answer(f'Статистика бота:\nПользователей: {db.count_users()}')






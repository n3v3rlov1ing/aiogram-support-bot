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


@handler.message(Command('start'))
async def cmd_start(message: Message):
    if db.user_exist(message.from_user.id) == True:
        await message.answer(f'Привет, {message.from_user.first_name}')
    else:
        db.reg_user(message.from_user.id)
        await message.answer(f'{message.from_user.first_name}, вы были успешно зарегистрированы!')

@handler.message(Command('send'))
@handler.message(F.text.lower() == 'Рассылка')
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
    try:
        if message.text == '0':
            user_data = await state.get_data()
            text = user_data['text']
            for i in db.get_users():
                await bot.send_message(i[0], text)
                await state.clear()
        else:
            file_id = message.photo[-1].file_id
            await state.update_data(photo=file_id)
            user_data = await state.get_data()
            text = user_data['text']
            photo = user_data['photo']

            for i in db.get_users():
                await bot.send_photo(i[0], photo, caption=text)
            await state.clear()
    except TypeError:
        await message.answer('Произошла ошибка')
        await state.set_state(Distribution.photo)
    except Exception as e:
        pass

@handler.message(Command('admin'))
async def cmd_admin(message: Message):
    if message.from_user.id == admin_id:
        kb = [[
            KeyboardButton(text='Рассылка'),
        ]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Вы админ', reply_markup=keyboard)


    





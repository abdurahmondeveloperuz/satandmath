from filters.private_chat_filter import IsPrivate
import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default.buttons import main
from loader import dp, db, bot

from utils.misc.imgur import upload

@dp.message_handler(IsPrivate(),commands=['start'])
async def start_bot(message: types.Message):
    await message.answer(f"<b>👋 Assalomu alaykum hurmatli <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>!</b>\n\n\n<i>💭Ushbu bot @uzsatmath ning rasmiy boti bo'lib javoblarni qabul qilishda ishlatiladi.\n👇 Pastdagi \"📝 Test tekshirish\" tugmasi orqali test javoblaringizni tekshirib olishingiz mumkin</i>", reply_markup=main)


from filters.private_chat_filter import IsPrivate
import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default.buttons import main
from loader import dp, db, bot

from utils.misc.imgur import upload

@dp.message_handler(IsPrivate(),text_contains='📊 Mening natijalarim')
async def start_bot(message: types.Message):
    await message.answer("📊 Test natijalarni <code>/getrankings testId</code> orqali ko'rishingiz mumkin!\n\n❗️ Misol uchun: <code>/getrankings 12345</code>")

@dp.message_handler(IsPrivate(),text_contains='✍️ About creator')
async def start_bot(message: types.Message):
    await message.answer("🤖 Bu bot E'tirof maktabi IT yo'nali 8-sinf o'quvchisi tomonidan tayyorlandi!\n\n🏫 Maktab telegram sahifasi: @EtirofXM")

    
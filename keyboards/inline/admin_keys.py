from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loader import bot
mainMenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🆕 Yangi test", callback_data='admin:new_test'),
        ],
        [
            InlineKeyboardButton(text="🆕 Yangi test", callback_data='admin:new_test'),
            
        ]
    ],
)


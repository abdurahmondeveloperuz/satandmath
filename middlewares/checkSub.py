import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.misc import subscription
from loader import db, bot
import datetime
import sqlite3


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self,update:types.Update,data:dict):
        if update.message:
            user = update.message.from_user.id
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data =='check_subs':
                await update.callback_query.message.delete()
        else:
            return


        buttons = InlineKeyboardMarkup(row_width=1)
        final_status = True 
        CHANNELS = ["@uzsatmath"]
        for channel in CHANNELS:
            status = await subscription.check(user_id=user, channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)
            if not status:
                invite_link = await channel.export_invite_link()
                buttons.add(InlineKeyboardButton(text=f"{channel.title}",url=f"{invite_link}"))
        if not final_status:

            buttons.add(InlineKeyboardButton(text="✅Obuna bo'ldim",callback_data="check_subs"))
            if update.message:await update.message.answer('⚠️ Botdan foydalanish uchun, quyidagi kanallarga obuna bo\'ling:',reply_markup=buttons)
            else:await update.callback_query.message.answer('⚠️ Botdan foydalanish uchun, quyidagi kanallarga obuna bo\'ling:',reply_markup=buttons)
            raise CancelHandler()
        


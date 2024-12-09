from aiogram import executor
from time import sleep
from loader import dp, db,bot
import middlewares, filters, handlers
# from utils.notify_admins import on_startup_notify,on_shutdown_notify
from utils.set_bot_commands import set_default_commands
from data.config import ADMINS

async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    try:
        db.create_table_users()
    except Exception as err:pass



if __name__ == '__main__':
    executor.start_polling(dp)
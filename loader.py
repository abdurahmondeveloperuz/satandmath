from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.sqlite import Database, TestManager, UserRankings


from data import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(path_to_db="data/main.db")
testmgr = TestManager(path_to_db="data/testmanager.db")
rankings = UserRankings(path_to_db="data/testmanager.db")
sched = AsyncIOScheduler()

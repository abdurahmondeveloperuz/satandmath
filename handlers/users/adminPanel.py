from keyboards.inline.admin_keys import mainMenu
from filters.private_chat_filter import IsPrivate
import sqlite3
import os
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from server import postRatings
from utils.misc.imgur import upload as photoUpload

from data.config import ADMINS
from keyboards.default.buttons import main, back
from loader import dp, db, bot, testmgr, rankings
from aiogram.types import *

@dp.message_handler(commands = "newtest", user_id=ADMINS)
async def adminPanel(message: Message):
	msg = message.get_args()
	parts = msg.split("*")
	test_id = parts[0]
	answers = parts[1].lower()
	answers = ''.join([char for char in answers if not char.isdigit()])
	test_id = testmgr.save_test(answers=answers, test_id=test_id)
	if test_id == "error":
		await message.answer("✅ Bu test id allaqachon mavjud")
		return
	await message.answer(f"<b>🆕 Yangi test saqlandi!\n\n📝 Test IDsi: <code>{test_id}</code>\n❓ Savollar soni: {len(answers)}\n📊 Natijalarni ko'rish uchun <code>/getrankings {test_id}</code></b>")
@dp.message_handler(commands = "getrankings")
async def handleCommand(message: Message):
	test_id = message.get_args()
	user_id = message.from_user.id 
	answersData = rankings.get_user_test(user_id, test_id)
	if answersData is None:
		correct = 0
		wrong = 0
		percent = 0
	else:
		correct = answersData['correct']
		wrong = answersData['wrong']
		percent = round(100 / (wrong+correct) * correct, 1)

	msgwarn = await message.answer("📊 Natijalar tahlil qilinyabdi ...")

	allRatings = rankings.getAllRatings(test_id=test_id)

	studentsData = []

	for student in allRatings:
		profile_photos = await bot.get_user_profile_photos(student['userId'])
	
		if profile_photos.total_count > 0:
			photo_file_id = profile_photos.photos[0][-1].file_id
			file_info = await bot.get_file(photo_file_id)
			file_path = file_info.file_path
			
			save_path = f"./photos/{user_id}.jpg"
			os.makedirs(os.path.dirname(save_path), exist_ok=True)
			await bot.download_file(file_path, save_path)
			url = photoUpload(save_path)
		else:
			url = ""
		user_data = await bot.get_chat(student['userId'])
		full_name = user_data.full_name
		score = student['score']
		profile_link = f"https://t.me/{user_data.username}"
		profile_photo = url
		studentsData.append({
			'first_name': full_name,
			'last_name': "⠀",
			'score': score,
			'image': profile_photo,
			'profile_url': profile_link,
			})

	params = {"class_id": test_id}

	data = {"class_name": "SAT & Math", "students": studentsData}

	res = await postRatings(data=data, params=params)

	if res.status_code != 200:
		await msgwarn.edit_text("❌ Hech kim bu testni ishlamadi!")
	else:
		await msgwarn.edit_text(f"""
📊 Testda ko'rsatgan natijangiz:

📖 Test kodi: {test_id}
✏️ Jami savollar soni: {wrong+correct} ta
✅ To'g'ri javoblar soni: {correct} ta
📈 Foiz: {percent} %

<a href="https://rankingsofstudents.fly.dev/rankings?class_id={test_id}">👉 Bu yerda barchaning reytinglarini ko'rishingiz mumkin!</a>
	""")
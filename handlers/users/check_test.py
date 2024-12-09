from filters.private_chat_filter import IsPrivate
import sqlite3
import os
from utils.misc.imgur import upload as photoUpload
from server import postRatings

from aiogram.dispatcher import FSMContext

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from datetime import datetime

from data.config import ADMINS
from keyboards.default.buttons import main, back
from loader import dp, db, bot, testmgr, rankings

@dp.message_handler(IsPrivate(), state="*", text_contains=['🔙 Ortga'])
async def start_bot(message: types.Message, state: FSMContext):
    await message.answer(f"<b>👋 Assalomu alaykum hurmatli <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>!</b>\n\n\n<i>💭Ushbu bot @uzsatmath ning rasmiy boti bo'lib javoblarni qabul qilishda ishlatiladi.\n👇 Pastdagi \"📝 Test tekshirish\" tugmasi orqali test javoblaringizni tekshirib olishingiz mumkin</i>", reply_markup=main)
    await state.finish()

@dp.message_handler(IsPrivate(), text_contains=['📝 Test tekshirish'])
async def start_bot(message: types.Message, state: FSMContext):
    await message.answer(f"<b>✍️ Test kodini yuboring:</b>\n\n📃 Test kodi @uzsatmath kanalidan olishingiz mumkin!", reply_markup=back)
    await state.set_state("test_code")

@dp.message_handler(IsPrivate(), state="test_code")
async def check_test_id(message: types.Message, state: FSMContext):
    test_id = message.text
    user_id = message.from_user.id
    test_status = testmgr.check_status(test_id)
    user_status = rankings.check_userId(test_id, user_id)
    count = testmgr.get_test_count(test_id)


    if test_status == "online":
        pass
    elif test_status == "notExist":
        await message.answer("<b>❌ Test kodi noto'g'ri! Ishonchingiz komilmi?</b>\n\n<b>👇 Qayatadan kiritib ko'ring: </b>", reply_markup=back)
        await state.set_state("test_code")
        return
    else:
        await message.answer("<b>❌ Test muddati tugagan boshqa testlarni ishlashga harakat qilib ko'ring!</b>", reply_markup=back)
        await state.finish()
        return
    if user_status:
        pass
    else:
        await message.answer(f"<b>✅ Siz bu testni allaqachon yakunlagansiz va natijangiz ro'yxatga olingan!\n<code>/getrankings {test_id}</code> orqali natiganizni ko'rishingiz mumkin</b>\n\n<i>\"🔙Ortga\" tugmasi orqali bosh menyuga qaytishingiz mumkin.</i>", reply_markup=back)
        await state.finish()
        return
    await message.answer(f"<b>✍️ <code>{test_id}</code> kodli testda {count} ta kalit mavjud. Marhamat o'z javoblaringizni yuboring.</b>\n\n"
                        f"<b>M-n:</b> abcd(ABCD)... yoki 1a2b3c4d(1A2B3C4D)...")

    await state.set_data({f"{user_id}": test_id})
    await state.set_state("check_answers")

@dp.message_handler(IsPrivate(), state="check_answers")
async def check_test_answers(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    state_data = await state.get_data() 
    await state.finish()
    test_id = state_data[f'{user_id}']
    answers = ''.join([char for char in message.text.lower() if not char.isdigit()])
    count = testmgr.get_test_count(test_id)
    if len(answers) == count:
        pass
    else:
        await message.answer(f"<b>🎯 <code>{test_id}</code> raqamli testda {count}ta test bor.\n\n📥 Sizning javoblaringiz soni esa {len(answers)}.\n📋 Javoblaringizni qayta ko'rib chiqing!</b>")
        await state.set_data({f"{user_id}": test_id})
        
        await state.set_state("check_answers")
        return

    msg = await message.answer("⏰ Tekshirilyapti ... ")

    answersData = testmgr.check_test(test_id, answers)
    correct = answersData['correct']
    wrong = answersData['wrong']

    rankings.saveRating(test_id, user_id, correct=correct, wrong=wrong, answers=answers)

    user_id = message.from_user.id


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


    await postRatings(data=data, params=params)

    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    answersquery = ""
    for rank, value in answersData['answers'].items():
        if value['correct'] == value['selected']:
            answersquery += f"{rank}. {value['correct'].upper()} ✅\n"
        else:
            answersquery += f"{rank}. {value['selected'].upper()} ❌ {value['correct'].upper()} ✅\n"
    await msg.edit_text(answersquery)
    await message.answer(f"""
📊 Testda ko'rsatgan natijangiz:

📖 Test kodi: <code>{test_id}</code>
✏️ Jami savollar soni: {wrong+correct} ta
✅ To'g'ri javoblar soni: {correct} ta
📈 Foiz: {round(100 / (wrong+correct) * correct, 1)} %

<a href="https://rankingsofstudents.fly.dev/rankings?class_id={test_id}">👉 Bu yerda barchaning reytinglarini ko'rishingiz mumkin!</a>
""")


        


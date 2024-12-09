from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
	[
		KeyboardButton("📝 Test tekshirish")
	],
	[
		KeyboardButton("📊 Mening natijalarim")

	],
	[
		KeyboardButton("✍️ About creator")
	],


], resize_keyboard=True)

back = ReplyKeyboardMarkup(keyboard=[
	[
		KeyboardButton("🔙 Ortga")
	]
], resize_keyboard=True)
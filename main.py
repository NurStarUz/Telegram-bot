import json
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from keep_alive import keep_alive

keep_alive()  # Flask serverni ishga tushirish

# 📌 BOT TOKENINGIZNI SHU YERGA YOZING!
API_TOKEN = "677810027:AAHqD6IwmCUmRfdeskvTOx-0LwLiK-f8RM4"

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# 🔹 Testlarni yuklash
with open("tests.json", "r", encoding="utf-8") as f:
    tests = json.load(f)

# 🔹 Foydalanuvchilarning testlarini va natijalarini saqlash
user_tests = {}
scores = {}

# 📌 Statistika faylini yuklash yoki yaratish
try:
    with open("scores.json", "r", encoding="utf-8") as f:
        scores = json.load(f)
except FileNotFoundError:
    scores = {}

# 📌 🔘 Tugmalar menyusini yaratamiz
menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Testni boshlash")],
        [KeyboardButton(text="📊 Mening statistikam"), KeyboardButton(text="🏆 Reyting")]
    ],
    resize_keyboard=True  # Tugmalarni kichraytirish
)

# 📌 🏁 Start buyrug‘i
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("👋 Salom! Testni boshlash uchun quyidagi tugmalardan foydalaning:", reply_markup=menu_buttons)

# 📌 📝 Testni boshlash
@dp.message(lambda message: message.text == "📝 Testni boshlash")
async def start_test(message: Message):
    user_id = str(message.from_user.id)
    user_tests[user_id] = {
        "questions": random.sample(tests, 10),
        "current_index": 0,
        "correct_answers": 0
    }
    await send_question(message, user_id)

# 📌 Viktorina yuborish funksiyasi (Ketma-ket testlar)
async def send_question(message, user_id):
    test_index = user_tests[user_id]["current_index"]

    if test_index >= len(user_tests[user_id]["questions"]):
        correct = user_tests[user_id]["correct_answers"]
        await bot.send_message(message.chat.id, f"✅ Test tugadi!\n\n🎯 To‘g‘ri javoblar: {correct} / 10", reply_markup=menu_buttons)

        if user_id not in scores:
            scores[user_id] = {"name": message.from_user.full_name, "score": 0}
        scores[user_id]["score"] += correct

        with open("scores.json", "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=4)

        return

    test = user_tests[user_id]["questions"][test_index]

    await bot.send_poll(
        chat_id=message.chat.id,
        question=test["

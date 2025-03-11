import json
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from keep_alive import keep_alive  # UptimeRobot uchun Flask server

keep_alive()  # Botni fonda ushlab turish

# 📌 BOT TOKENINGIZNI SHU YERGA YOZING!
API_TOKEN = "677810027:AAHqD6IwmCUmRfdeskvTOx-0LwLiK-f8RM4"

# 🔹 Aiogram 3.7.0 uchun mos bot yaratish
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# 🔹 Testlarni yuklash
with open("tests.json", "r", encoding="utf-8") as f:
    tests = json.load(f)

# 🔹 Foydalanuvchilarning testlarini saqlash
user_tests = {}

# 🔹 /start buyrug‘i uchun handler
@dp.message(Command("start"))
async def start_cmd(message: Message):
    user_tests[message.from_user.id] = random.sample(tests, 10)  # Tasodifiy 10 ta test
    await send_question(message.from_user.id, 0)

# 🔹 Viktorina yuborish funksiyasi
async def send_question(user_id, test_index):
    if test_index >= len(user_tests[user_id]):
        await bot.send_message(user_id, "✅ Test tugadi! Qayta boshlash uchun /start buyrug‘ini yuboring.")
        return

    test = user_tests[user_id][test_index]

    await bot.send_poll(
        chat_id=user_id,
        question=test["savol"],
        options=test["variantlar"],
        type="quiz",
        correct_option_id=test["togri"],
        is_anonymous=False
    )

    await asyncio.sleep(2)
    await send_question(user_id, test_index + 1)

# 🔹 Botni ishga tushirish funksiyasi
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

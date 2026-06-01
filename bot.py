import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# O'zingiz nusxalab olgan tokeni shu yerga qo'ying
TOKEN = "8958938811:AAGauDd6UyQ2AL_2JsMQ6q6O0pv4cOPHM80"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Assalomu alaykum! Men ishlayapman! 🚀")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
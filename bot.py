import asyncio
import logging
import sys


from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


TOKEN = "7233075659:AAFDQLicBx8aPaYayQ34RWsmkBHFaZSYhwM"

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    in_btn = InlineKeyboardButton(text="Info", callback_data=f"info_{message.from_user.id}")
    in_btn2 = InlineKeyboardButton(text="Info", callback_data=f"start_{message.from_user.id}")
    keybaord = InlineKeyboardMarkup(inline_keyboard=[[in_btn, in_btn2]])

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=keybaord)

@dp.callback_query()
async def ans_to_callback(callback: CallbackQuery):
    if callback.data.startswith("info"):
        await callback.message.answer(text="Foydalanuvchi ma'limumot olmoqchi")
    else:
        await callback.message.answer(text="Foydalanuvchi start bosdi")



@dp.message(F.text.isdigit())
async def echo_handler(message: Message) -> None:
    k = 1
    n = int(message.text)
    m = int(n ** 0.5)
    qoldiq = n - m * m

    if n == 0:
        await message.answer("Tozalandi", reply_markup=ReplyKeyboardRemove())
        return

    matrix = []

    for i in range(m):
        row = []
        for j in range(m):
            row.append(KeyboardButton(text=f"{k}"))
            k += 1
        matrix.append(row)

    row = []
    for i in range(qoldiq):
        row.append(KeyboardButton(text=f"{k}"))
        k += 1

    matrix.append(row)


    await message.answer("Tayyor", reply_markup=ReplyKeyboardMarkup(keyboard=matrix, resize_keyboard=True))




async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
# import asyncio
# import logging
# import sys
#
# from aiogram import Bot, Dispatcher, html, F
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart
# from aiogram.types import Message, CallbackQuery
# from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#
#
# TOKEN = "7828936588:AAH_6TBsJjcRyZ6YP-SyQEmotO4_xfHMDWw"
#
# dp = Dispatcher()
#
#
# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     buttons = [
#         [KeyboardButton(text="Korzinka")],
#
#     ]
#     keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
#     await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!", reply_markup=keyboard)
#
#
# @dp.message(F.text == "Korzinka")
# async def korzinka_menu(message: Message):
#     buttons = [
#         [KeyboardButton(text="Mevalar"), KeyboardButton(text="Telefonlar")]
#     ]
#     keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
#     await message.answer("Kategoriyalardan birini tanlang:", reply_markup=keyboard)
#
#
# @dp.message(F.text == "Mevalar")
# async def fruits_menu(message: Message):
#     buttons = [
#         [KeyboardButton(text="Olma"), KeyboardButton(text="Banan")],
#         [KeyboardButton(text="Uzum"), KeyboardButton(text="Mango")],
#         [KeyboardButton(text="Qaytish")]
#     ]
#     keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
#     await message.answer("Mevalar:", reply_markup=keyboard)
#
#
# @dp.message(F.text == "Telefonlar")
# async def phones_menu(message: Message):
#     buttons = [
#         [KeyboardButton(text="iPhone 14"), KeyboardButton(text="Samsung S23")],
#         [KeyboardButton(text="Redmi Note 12"), KeyboardButton(text="Qaytish")]
#     ]
#     keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
#     await message.answer("Telefonlar:", reply_markup=keyboard)
#
#
# @dp.message(F.text == "Qaytish")
# async def back_to_main(message: Message):
#         await korzinka_menu(message)
#
#
# @dp.message(F.text.isdigit())
# async def echo_handler(message: Message) -> None:
#     k = 1
#     n = int(message.text)
#     m = int(n ** 0.5)
#     qoldiq = n - m * m
#
#     if n == 0:
#         await message.answer("Tozalandi", reply_markup=ReplyKeyboardRemove())
#         return
#
#     matrix = []
#
#     for i in range(m):
#         row = []
#         for j in range(m):
#             row.append(KeyboardButton(text=f"{k}"))
#             k += 1
#         matrix.append(row)
#
#     row = []
#     for i in range(qoldiq):
#         row.append(KeyboardButton(text=f"{k}"))
#         k += 1
#
#     matrix.append(row)
#
#     await message.answer("Tayyor", reply_markup=ReplyKeyboardMarkup(keyboard=matrix, resize_keyboard=True))
#
#
# async def main() -> None:
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())



















import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio


with open('names.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    all_names = data['names']

NAMES_PER_PAGE = 10
TOTAL_PAGES = (len(all_names) // NAMES_PER_PAGE) + (1 if len(all_names) % NAMES_PER_PAGE else 0)

bot = Bot(token="7828936588:AAH_6TBsJjcRyZ6YP-SyQEmotO4_xfHMDWw")
dp = Dispatcher()


def get_names_page(page: int):
    start_idx = (page - 1) * NAMES_PER_PAGE
    end_idx = start_idx + NAMES_PER_PAGE
    page_names = all_names[start_idx:end_idx]

    names_text = "\n".join([f"{name['id']}. {name['name']}" for name in page_names])
    caption = f"Ismlar {start_idx + 1}-{min(end_idx, len(all_names))}:\n\n{names_text}"

    builder = InlineKeyboardBuilder()
    if page > 1:
        builder.button(text="⬅️ Oldingi", callback_data=f"prev_{page}")
    if page < TOTAL_PAGES:
        builder.button(text="Keyingi ➡️", callback_data=f"next_{page}")

    builder.adjust(2)
    keyboard = builder.as_markup()

    return caption, keyboard


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text, keyboard = get_names_page(1)
    await message.answer(text, reply_markup=keyboard)



@dp.callback_query(lambda c: c.data.startswith(("prev_", "next_")))
async def process_callback(callback: types.CallbackQuery):
    action, current_page = callback.data.split("_")
    current_page = int(current_page)

    if action == "prev":
        new_page = current_page - 1
    else:
        new_page = current_page + 1

    text, keyboard = get_names_page(new_page)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

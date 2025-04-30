from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

get_phone = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="tel", request_contact=True)]
    ],
    resize_keyboard=True
)

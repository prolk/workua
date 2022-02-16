import logging
import json
import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from aiogram.utils.markdown import hbold, hlink
from config import TOKEN
from main import main

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_bot(message: types.Message):
    start_buttons = ['Find a Job', 'Fake']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Bot started', reply_markup=keyboard)


@dp.message_handler(Text(equals='Find a Job'))
async def find_job(message: types.Message):
    await message.answer('waiting......')

    os.remove('main.json')
    main()

    with open('main.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        card = f'{hlink(item.get("link_title"), item.get("link"))}\n' \
            f'{hbold("Вакансія: ")} {item.get("title")}\n' \
            f'{hbold("Зарплатня:")} {item.get("salary")}\n' \
            f'{hbold("Опубліковано: ")} {item.get("added")}\n'
        try:
            await message.answer(card)
        except Exception as e:
            return e


@dp.message_handler(Text(equals='Fake'))
async def fake(message: types.Message):
    await message.answer('press other button...')


if __name__ == '__main__':
    executor.start_polling(dp)

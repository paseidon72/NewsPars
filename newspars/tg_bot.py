import asyncio
import json
import datetime

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
from config import token, user_id
from pars import check_news_update

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Всі новини", "Останні 5", "Свіжі новини"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Полоса новин", reply_markup=keyboard)


@dp.message_handler(Text(equals="Всі новини"))
async def get_all_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        # news = f"<b>{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}</b>\n" \
        #        f"<u>{v['articles_title']}</u>\n" \
        #        f"<code>{v['article_desc']}</code>\n" \
        #        f"{v['article_url']}"
        # news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
        #        f"{hunderline(v['articles_title'])}\n" \
        #        f"{hcode(v['article_desc'])}\n" \
        #        f"{hlink(v['articles_title'], v['article_url'])}"
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
               f"{hlink(v['articles_title'], v['article_url'])}"

        await message.answer(news)


@dp.message_handler(Text(equals="Останні 5"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
               f"{hlink(v['articles_title'], v['article_url'])}"
        await message.answer(news)


@dp.message_handler(Text(equals="Свіжі новини"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                   f"{hlink(v['articles_title'], v['article_url'])}"
            await message.answer(news)
    else:
        await message.answer("New - News is NO!")


async def nes_every_minute():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                       f"{hlink(v['articles_title'], v['article_url'])}"
                await bot.send_message(user_id, news, disable_notification=True)
        else:
            await bot.send_message(user_id, "New News is NO!", disable_notification=True)
        await asyncio.sleep(20)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(nes_every_minute())
    executor.start_polling(dp)














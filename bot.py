import random
import asyncio
from os import getenv
from sys import exit
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from parser import *
from avito_db import *


bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    """Обработчик команды '/start'"""
    await msg.reply(f"Привет, {msg.from_user.first_name}!\nЯ маленький бот который умеет отслеживать объявления с avito.ru.\nПожалуйста, если у тебя есть пожелания напиши: t.me/espadane",disable_web_page_preview=True)
    user_id = msg.from_user.id
    loop = asyncio.get_event_loop()
    loop.create_task(ads_every_minute(user_id))

@dp.message_handler(commands=['help'])
async def process_help_command(msg: types.Message):
    """Обработчик команды '/help'"""
    await msg.reply("Чтобы отслеживать объявления из авито пришли мне ссылку на поисковый запрос.\nЧтобы прекратить отслеживание снова пришли мне ссылку или напиши комманду '/all_ads'.")

@dp.message_handler(commands=['all_ads'])
async def process_start_command(msg: types.Message):
    """Обработчик команды '/all_ads'для удаления всех отслеживаемых объявлений"""
    all_ads = get_all_users_ads(msg.from_user.id)
    for ad in all_ads:
        ad_url = str(ad).split("'")[1]
        ad_title = str(ad).split("'")[3].replace('\\xa0', ' ')
        button=(types.InlineKeyboardButton(text=f"Перестать отслеживать", callback_data='delete_ad'))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(button)
        await msg.answer(f'{ad_title}\n\n{ad_url}', reply_markup=keyboard,disable_web_page_preview=True)


@dp.callback_query_handler(text='delete_ad')
async def delete_ad(call: types.callback_query):
    """Удаление остлеживаемых объявлений по клику на кнопку"""
    url_to_delete = str(call.message.text).split('\n')[2]
    title_to_delete = str(call.message.text).split('\n')[0]
    user_id = str(call.message.chat.id)
    delete_old_data(user_id, url_to_delete)
    await call.answer(str(f'Объявление больше не отслеживается: {title_to_delete}'), show_alert=True)

@dp.message_handler(Text)
async def add_tracked_ad(msg:types.Message):
    """Функция проверяет пришла ли ссылка с авито, если да то проверяет отслеживается ли объявления. Если нет, объявления начинают отслеживаться, если да, то удаляюются из отслеживания."""
    if 'https://www.avito.ru' or 'https://m.avito.ru' in msg.text:
        try:
            tracked_url_title = get_requested_page_title(msg.text)
            user_id = msg.from_user.id
            tracked_url = msg.text
            last_ad = get_ad_data(tracked_url)
            last_ad_url = last_ad[4]
            result = check_data(user_id, tracked_url, last_ad_url)
            if result == 'no data':
                await msg.answer(f'Теперь отслеживаю:\n{tracked_url_title}',disable_web_page_preview=True)
                last_ad = build_nice_message(msg.text)
                print(last_ad + 'asda')
                await msg.answer(f'Последнее объявление:\n{last_ad}',disable_web_page_preview=True)
                data = (user_id, tracked_url, last_ad_url, tracked_url_title)
                write_url_on_db(data)
            elif result == 'delete data':
                delete_old_data(user_id, tracked_url)
                await msg.answer(f'Больше не отслеживаю:\n{tracked_url_title}', disable_web_page_preview=True)
        except Exception as ex:
            print(ex)
            await msg.answer(f'Авито нас спалил. Мы уже работаем над решением проблемы. Ваше мнение очень важно для нас')
    else:
        await msg.reply('Простите, хозяин :(.\n Я вас не понял.')

def build_nice_message(url):
    """Функция вывода объявления в более читаемом виде"""
    try:
        ad_list = get_ad_data(url)
        return f'Название - {ad_list[0]}\nЦена - {ad_list[1]}\nРайон: {ad_list[3]}\n\n{ad_list[2]}\n\n{ad_list[4]}'
    except Exception as ex:
        print(ex)

async def ads_every_minute(user_id):
    """Проверка новых объявлений каждую минуту"""
    while True:
        ads_users_list = get_all_users_ads(user_id)
        if len(ads_users_list) >= 1:
            for ads in ads_users_list:
                ads_url = str(ads).split("'")[1]
                tracked_url_title = get_requested_page_title(ads_url)
                old_ad = get_old_ad_from_db(user_id, tracked_url=ads_url)
                old_ad_url = str(old_ad).split("'")[1]
                new_ad_url = get_ad_data(ads_url)[-1]
                new_ad_data = (user_id, ads_url, new_ad_url,tracked_url_title)
                if new_ad_url != old_ad_url:
                    delete_old_data(user_id, tracked_url=ads_url)
                    write_url_on_db(new_ad_data)

                    await bot.send_message( user_id, f'{build_nice_message(ads_url)}',disable_web_page_preview=True)
                else:
                    print('Обновлений нет ')

        await asyncio.sleep(random.randint(40, 90))



if __name__ == '__main__':
    executor.start_polling(dp)

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import telebot
from telebot import types
import pandas as pd
from telebot.types import LabeledPrice
import requests
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import telegram
from datetime import datetime
import datetime

bot = telebot.TeleBot('2124981817:AAFnVlMfAQNcWvRoqqRFFWeuiRa_ZDn_1Cg')

class main:
    db_string = "postgresql://postgres:qweasdzxc123@database-2.cfnsbden5utu.us-east-2.rds.amazonaws.com:5432/"
    con = create_engine(db_string, pool_size=10, max_overflow=20)
    link = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']  # задаем ссылку на Гугл таблици
    my_creds = ServiceAccountCredentials.from_json_keyfile_name('gogol.json', link)  # формируем данные для входа из нашего json файла
    client = gspread.authorize(my_creds)  # запускаем клиент для связи с таблицами
    sheet1 = client.open('Гоголь').worksheet("users")
    sheet2 = client.open('Гоголь').worksheet("payment")
    sheet3 = client.open('Гоголь').worksheet("logs")  # открываем нужную на таблицу и лист
    sheet4 = client.open('Гоголь').worksheet("sources")

    kb_refresh = telebot.types.InlineKeyboardMarkup()
    kb_refresh.row(telebot.types.InlineKeyboardButton('Gogol tables', callback_data='Gogol tables'),
                    telebot.types.InlineKeyboardButton('Gogol dashboard', callback_data='Gogol dashboard'))
    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, f'Что обновляем?',reply_markup=main.kb_refresh)


    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        user_id = call.message.chat.ids
        if call.data == "Gogol tables":
            payment = pd.read_sql('''select user_id::text,package::text,price::text,process_dttm::text, symbols from gogol.payment_logs''', main.con)
            sources = pd.read_sql('''select id::text,name::text,promo::text,symbols::text,price::text from gogol.sources''', main.con)
            users = pd.read_sql("""select id::text,spend_symbols::text,total_payment::text,algoritm::text,date_joined::text,source::text,allowed_symbols::text,mode::text,lastcall::text from gogol.users""", main.con)
            logs = pd.read_sql('''select idt::text,	userid::text,text::text,mutated_text::text,	cos,lev,fit,alg,lang,duration::text,ip_proxy::text,	dtime::text from gogol."logs_gogol_andip" order by dtime desc limit 50''', main.con)

            main.sheet1.update([users.columns.values.tolist()] + users.values.tolist())
            main.sheet2.update([payment.columns.values.tolist()] + payment.values.tolist())
            main.sheet3.update([logs.columns.values.tolist()] + logs.values.tolist())
            main.sheet4.update([sources.columns.values.tolist()] + sources.values.tolist())
            bot.send_message(call.message.chat.id, f'Таблицы обновлены',reply_markup=main.kb_refresh)

bot.polling()
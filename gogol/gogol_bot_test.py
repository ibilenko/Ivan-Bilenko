from sqlalchemy import create_engine
import telebot
from telebot import types
import pandas as pd
import telegram
from datetime import datetime
from telebot.types import LabeledPrice

bot = telebot.TeleBot('2029906477:AAHbVVLfwawBz0z5cYCKeR1spwU6hIyCiUU')


class main:
    db_string = "postgresql://hmxdnwubdttbnz:9e63e8f51fbdaa5a7dfd36e69526ffd277c532dd124debf16f9ef3cebcea5d79@ec2-52-31-233-101.eu-west-1.compute.amazonaws.com:5432/d10gqjnnkpealj"
    engine = create_engine(db_string, pool_size=10, max_overflow=20)
    bot_before_init = True  # при True означает, что в переменных класса отсутсвует актуальная инфа по пользователю из базы
    bot_working = False  # при True означает, что сейчас режим обмена текса с Гоголем и можно выйти из режима только кнопкой Меню
    ask_promo = False  # при True ожидает промокод
    check_promo = False  # при True позволяет пользвотелю нажимать кнопки Да, Нет промокода
    new_user = False  # при True сценарий с запросом промокода
    prohibition = False
    alg_easy = """ЛЁГКИЙ _(меняет не сильно, без потери смысла)_"""
    alg_hard = """СЛОЖНЫЙ _(высокая уникальность, бывает потеря смысла)_"""
    alg = alg_easy
    dict_price = {'Курсовой': 10000, 'Диплом': 40000, 'Писатель': 100000}
    dict_symbols = {'Курсовой': 10000, 'Диплом': 50000, 'Писатель': -1}
    pay_token = '381764678:TEST:29902'
    start_txt = """Салют 🎇 , я искусственный интеллект! 
Могу перефразировать твой текст, повышая оригинальность и убирая ошибки."""

    begin_txt = """Итак, начнём:
🔸 Напишите ️свой текст (лучше вставлять абзацами до 300 символов, так легче работать)

🔸  Получите оригинальный текст в ответном сообщении. Процент оригинальности при проверке на антиплагиат будет *80 и больше*!"""
    balance_txt = """Хотел бы я работать бесплатно, но чернила, перья и сервера стоят денег… 

У меня есть к вам три предложения:
    
🔶 Пакет «КУРСАЧ» *10 000* символов за *100* рублей. 
_Хватит, чтобы обработать курсовой проект!_

🔶 Пакет «ДИПЛОМ» *50 000* символов за *400* рублей. 
_На весь диплом!_

🔶 Пакет «ПИСАТЕЛЬ» *Сколько угодно!* за *1000* рублей.
_Этим я сам в своё время пользовался._
"""
    promo_ask = """У вас есть промокод?"""
    manual = """*Инструкция*:

Вот все, что нужно знать обо мне:
🤖 Я искусственный интеллект. Могу перефразировать текст и повысить его оригинальность 

📲 Чтобы работать со мной, нужно прислать мне текст. В ответном сообщении я отправлю его оригинальный вариант.

💡 Под оригинальностью я понимаю процент оригинальности, который покажет Антиплагиат.

📃 Я могу работать с текстом любой длины, но советую загружать абзацами до 300 символов, так будет удобнее вам.

💳 У вас есть баланс символов, которые вы можете мне отправить. Для его расширения используйте кнопку пополнения баланса.

🆘 По любым вопросам и предложениям можно написать в чат поддержки.

  
"""
    promo_text = """Принял!
Вам подарок 🎁 - """
    zero_sym_txt = """😔Жаль, но превышен лимит доступных для обработки символов.
Пополните баланс или уменьшите размер текста😉"""

    kb_algo = telebot.types.InlineKeyboardMarkup()
    kb_algo.row(telebot.types.InlineKeyboardButton('Алгоритм 🔛', callback_data='change_alg_working_mode'),
                telebot.types.InlineKeyboardButton('Меню 📱', callback_data='menu'))
    kb_no_promo = telebot.types.InlineKeyboardMarkup()
    kb_no_promo.row(telebot.types.InlineKeyboardButton('Ввести ещё раз🔄', callback_data='promo_yes'),
                    telebot.types.InlineKeyboardButton('Продолжить ➡️', callback_data='promo_no'))

    kb_manual = telebot.types.InlineKeyboardMarkup()
    kb_manual.row(telebot.types.InlineKeyboardButton('Всё понятно!', callback_data='menu'),
                  telebot.types.InlineKeyboardButton('Задать вопрос', callback_data='support',
                                                     url='https://t.me/izgarshevegor'))
    kb_menu = telebot.types.InlineKeyboardMarkup()
    kb_menu.row(telebot.types.InlineKeyboardButton('Начать ▶', callback_data='begin'),
                telebot.types.InlineKeyboardButton('Инструкция 🗝', callback_data='manual'))
    kb_menu.row(telebot.types.InlineKeyboardButton('Баланс 💳', callback_data='balance'),
                telebot.types.InlineKeyboardButton('Алгоритм 🔛', callback_data='change_alg'))
    kb_menu.add(
        telebot.types.InlineKeyboardButton('Чат поддержки', callback_data='support', url='https://t.me/izgarshevegor'))
    kb_balance = telebot.types.InlineKeyboardMarkup()
    kb_balance.row(telebot.types.InlineKeyboardButton('Курсач', callback_data='first'),
                   telebot.types.InlineKeyboardButton('Диплом', callback_data='second'),
                   telebot.types.InlineKeyboardButton('Писатель', callback_data='third'))
    kb_balance.add(telebot.types.InlineKeyboardButton('Меню 📱', callback_data='back'))
    kb_zero_symbols = telebot.types.InlineKeyboardMarkup()
    kb_zero_symbols.row(telebot.types.InlineKeyboardButton('Баланс 💳', callback_data='balance'),
                        telebot.types.InlineKeyboardButton('Меню 📱', callback_data='menu'))
    kb = telebot.types.InlineKeyboardMarkup()
    kb.row(
        telebot.types.InlineKeyboardButton('ДА☺️', callback_data='promo_yes'),
        telebot.types.InlineKeyboardButton('НЕТ🥲', callback_data='promo_no')
    )

    def get_promo(promo: str, engine):
        '''Достаёт подарочное кол-во символов по промокоду'''
        df = pd.read_sql(f"""select symbols from gogol.sources where promo = '{promo}'""", engine)
        if not df.empty:
            return df['symbols'][0]
        else:
            return False

    def check_user(user_id: int, engine) -> None:
        '''Проверяет новый юзер или нет'''
        df = pd.read_sql(f"""select id from gogol.users where id = {user_id}""", engine)
        if df.empty:
            print(df)
            main.new_user = True
        else:
            print('пустой фрейм')
            main.new_user = False

    def append_user(user_id: int, engine) -> None:
        '''Добавляет юзера в базу'''
        now = str(datetime.now().date())
        engine.connect().execute(f"""insert into gogol.users values ({user_id},0, 0,'Лёгкий', '{now}' ,null,100,'menu')""")
        main.new_user = False

    def append_promo(user_id: int, promo, engine) -> None:
        '''Добавляет источник от которого пришёл юзер'''
        engine.connect().execute(
            f"""update gogol.users set source = (select id from gogol.sources where promo = '{promo}')
                                     where id = {user_id}""")

    def allowed(user_id: int, symbols: int, engine) -> None:
        '''Расширяет диапазон доступных символов для юзера'''
        if symbols != -1:
            engine.connect().execute(f"""update gogol.users set allowed_symbols = allowed_symbols + {symbols}
                                         where id = {user_id}""")
        else:
            engine.connect().execute(f"""update gogol.users set allowed_symbols = {-1}
                                                     where id = {user_id}""")

    def spend(user_id: int, symbols: int, engine) -> None:
        '''Обновляет инфу по потраченным символам'''
        if main.allowed_symbols != -1:
            engine.connect().execute(f"""update gogol.users set allowed_symbols = allowed_symbols - {symbols}
                                         where id = {user_id}""")
            engine.connect().execute(f"""update gogol.users set spend_symbols = spend_symbols + {symbols}
                                         where id = {user_id}""")
        else:
            engine.connect().execute(f"""update gogol.users set spend_symbols = spend_symbols + {symbols}
                                                     where id = {user_id}""")

    def get_menu_info(user_id: int, engine) -> None:
        '''Достаёт инфу для текущего баланса'''
        df = pd.read_sql(f"""select spend_symbols, allowed_symbols, algoritm, mode from gogol.users where id = {user_id}""",
                         engine)
        if not df.empty:
            main.allowed_symbols = df['allowed_symbols'][0]
            main.spend_symbols = df['spend_symbols'][0]
            main.bot_working = True if df['mode'][0] == 'work' else False
            if df['algoritm'][0] == 'Лёгкий'
                main.alg = main.alg_easy
            else:
                main.alg = main.alg_hard
        else:
            raise NameError(f'Пользователь user_id = {user_id} отсутсвует в gogol.users')

    def payment_insert(user_id: int, package: str, price: int, symbols: int, engine) -> None:
        '''Добавляет информацию об оплате'''
        now = datetime.now()
        engine.connect().execute(
            f"""insert into gogol.payment_logs values ({user_id},'{package}',{price},'{now}',{symbols})""")

    def menu_txt() -> str:
        if main.allowed_symbols == -1:
            allowed_symbols = '∞'
        else:
            allowed_symbols = main.allowed_symbols
        menu_txt = f"""*Текущий баланс*

Доступно: *{allowed_symbols}* символов
Использовано: *{main.spend_symbols}* символов
Алгоритм: {main.alg}

Что будем делать?"""

        return menu_txt

    def check_bot_status(user_id: int, engine) -> bool:
        if main.bot_before_init:
            main.check_user(user_id, main.engine)
            if not main.new_user:
                main.get_menu_info(user_id, engine)
            main.bot_before_init = False
        return True

    def change_algoritm(user_id: int, engine, algoritm: str) -> None:
        engine.connect().execute(f"""update gogol.users set algoritm = '{algoritm}' where id = {user_id}""")

    @bot.message_handler(commands=['start'])
    def start_message(message):
        print(main.bot_working)
        if not main.bot_working:
            user_id = message.chat.id
            main.check_user(user_id, main.engine)
            if main.new_user:
                bot.send_message(user_id, main.start_txt)
                main.ask_promo = True
                main.check_promo = True
                bot.send_message(user_id, text=main.promo_ask, reply_markup=main.kb)
                main.append_user(user_id, main.engine)
                main.new_user = False
            else:
                bot.send_message(user_id, "Привет 👋 Рад вас видеть!")
                main.get_menu_info(user_id, main.engine)
                bot.send_message(user_id, main.menu_txt(), reply_markup=main.kb_menu,
                                 parse_mode=telegram.ParseMode.MARKDOWN)

    @bot.pre_checkout_query_handler(func=lambda query: True)
    def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
        bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    @bot.message_handler(content_types=['successful_payment'])
    def process_successful_payment(message):
        user_id = message.chat.id
        package = message.successful_payment.invoice_payload
        price = main.dict_price[package] // 100
        symbols = main.dict_symbols[package]
        if package == 'Курсовой':
            bot.send_message(user_id, text='Успешно! Обновляем информацию, ждём ответ от Гоголя.')
            main.payment_insert(user_id, package, price, symbols, main.engine)
            main.allowed(user_id, symbols, main.engine)
            main.get_menu_info(user_id, main.engine)
            bot.send_message(user_id, text='Отлично, работаем🤙')
            bot.send_message(user_id, text=main.menu_txt(), reply_markup=main.kb_menu,
                             parse_mode=telegram.ParseMode.MARKDOWN)
        if package == 'Диплом':
            bot.send_message(user_id, text='Успешно! Обновляем информацию, ждём ответ от Гоголя.')
            main.payment_insert(user_id, package, price, symbols, main.engine)
            main.allowed(user_id, symbols, main.engine)
            main.get_menu_info(user_id, main.engine)
            bot.send_message(user_id, text='То, что надо, чтобы закончить учебу🤌')
            bot.send_message(user_id, text=main.menu_txt(), reply_markup=main.kb_menu,
                             parse_mode=telegram.ParseMode.MARKDOWN)
        if package == 'Писатель':
            bot.send_message(user_id, text='Успешно! Обновляем информацию, ждём ответ от Гоголя.')
            main.payment_insert(user_id, package, price, symbols, main.engine)
            main.allowed(user_id, symbols, main.engine)
            main.get_menu_info(user_id, main.engine)
            bot.send_message(user_id, text='К Вашим услугам, коллега🤝')
            bot.send_message(user_id, text=main.menu_txt(), reply_markup=main.kb_menu,
                             parse_mode=telegram.ParseMode.MARKDOWN)

    @bot.message_handler(content_types=['text'])
    def send_screen(message):
        user_id = message.chat.id
        if main.check_bot_status(user_id, main.engine):
            if main.ask_promo:
                promo = message.text
                promo_symbols = main.get_promo(promo, main.engine)
                if promo_symbols:
                    main.append_promo(user_id, promo, main.engine)
                    main.allowed(user_id, promo_symbols, main.engine)
                    main.get_menu_info(user_id, main.engine)
                    bot.send_message(user_id, text=main.promo_text + f'{promo_symbols} символов')
                    bot.send_message(user_id, text=main.menu_txt(), reply_markup=main.kb_menu,
                                     parse_mode=telegram.ParseMode.MARKDOWN)
                    main.check_promo = False
                else:
                    bot.send_message(user_id, text="хм…😏Не нашёл такого промокода", reply_markup=main.kb_no_promo)
                main.ask_promo = False
            if main.bot_working and not main.prohibition:  # (1) здесь он принимает текст от пользователя
                len_symbols = len(message.text)
                if len_symbols > 3800:
                    main.prohibition = True
                    bot.send_message(user_id, text=f'Слишком длинный текст 🙃. Нужно убрать *{len_symbols-3800}* симв. для обработки', reply_markup=main.kb_zero_symbols,
                                     parse_mode=telegram.ParseMode.MARKDOWN)
                    main.prohibition = False
                else:
                    if main.allowed_symbols != -1 and main.allowed_symbols - len_symbols < 0:
                        bot.send_message(user_id, text=main.zero_sym_txt, reply_markup=main.kb_zero_symbols,
                                         parse_mode=telegram.ParseMode.MARKDOWN)# тут reply, когда закончились символы
                        # в текст от алгоритмов вставить
                    else:
                        main.get_menu_info(user_id, main.engine)
                        main.spend(user_id, len_symbols, main.engine)
                    bot.send_message(user_id, text='ответ', reply_markup=main.kb_algo,#тут reply на обычный ответ
                                     parse_mode=telegram.ParseMode.MARKDOWN)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        user_id = call.message.chat.id
        if main.check_bot_status(user_id, main.engine):
            if call.data == 'change_alg_working_mode':
                if main.alg == main.alg_hard:
                    main.alg = main.alg_easy
                    main.change_algoritm(user_id, main.engine, "Лёгкий")
                    bot.send_message(user_id, text=f'Поменял алгоритм на {main.alg_easy}. Введите текст:',parse_mode=telegram.ParseMode.MARKDOWN)
                else:
                    main.alg = main.alg_hard
                    main.change_algoritm(user_id, main.engine, "Сложный")
                    bot.send_message(user_id, text=f'Поменял алгоритм на {main.alg_hard}. Введите текст:',parse_mode=telegram.ParseMode.MARKDOWN)
            if call.data == 'menu':
                main.get_menu_info(user_id, main.engine)
                bot.send_message(user_id, text=main.menu_txt(), reply_markup=main.kb_menu,parse_mode=telegram.ParseMode.MARKDOWN)
                main.bot_working = False
                main.engine.connect().execute(f"update gogol.users set mode = 'menu' where id = {user_id}")
            if call.data == 'balance':
                bot.send_message(user_id, text=main.balance_txt, reply_markup=main.kb_balance,parse_mode=telegram.ParseMode.MARKDOWN)
                main.bot_working = False
            if call.data == "begin":# эта кнопка начать, по которой он включает режим ожидания текста (1)
                main.bot_working = True
                main.engine.connect().execute(f"update gogol.users set mode = 'work' where id = {user_id}")
                bot.send_message(user_id, text=main.begin_txt,parse_mode=telegram.ParseMode.MARKDOWN)
            if call.data == "manual":
                bot.send_message(user_id, text=main.manual, reply_markup=main.kb_manual,
                                 parse_mode=telegram.ParseMode.MARKDOWN)
                main.bot_working = False
            if call.data == 'first':
                bot.send_invoice(user_id, title='Пакет "Курсач"',
                                 description="""Пакет увеличивает кол-во доступных символов на 10 000 шт.""",
                                 provider_token=main.pay_token,
                                 currency='rub',
                                 is_flexible=False,
                                 prices=[LabeledPrice(label='Цена', amount=main.dict_price['Курсовой'])],
                                 invoice_payload='Курсовой')
            if call.data == 'second':
                bot.send_invoice(user_id, title='Пакет "Диплом"',
                                 description="""Пакет увеличивает кол-во доступных символов на 50 000 шт.""",
                                 provider_token=main.pay_token,
                                 currency='rub',
                                 is_flexible=False,  # True If you need to set up Shipping Fee
                                 prices=[LabeledPrice(label='Цена', amount=main.dict_price['Диплом'])],
                                 invoice_payload='Диплом')
            if call.data == 'third':
                bot.send_invoice(user_id, title='Пакет "Писатель"',
                                 description="""Пакет увеличивает кол-во доступных символов на неограниченное число""",
                                 provider_token=main.pay_token,
                                 currency='rub',
                                 is_flexible=False,  # True If you need to set up Shipping Fee
                                 prices=[LabeledPrice(label='Цена', amount=main.dict_price['Писатель'])],
                                 invoice_payload='Писатель')
            if not main.bot_working:
                if call.data == 'change_alg':
                    if main.alg == main.alg_hard:
                        main.alg = main.alg_easy
                        main.change_algoritm(user_id, main.engine, "Лёгкий")
                        bot.send_message(user_id, text='Поменял алгоритм на "Лёгкий"')
                    else:
                        main.alg = main.alg_hard
                        main.change_algoritm(user_id, main.engine, "Сложный")
                        bot.send_message(user_id, text='Поменял алгоритм на "Сложный"')
                    bot.send_message(user_id, text=main.menu_txt(), reply_markup=main.kb_menu,parse_mode=telegram.ParseMode.MARKDOWN)
                    main.bot_working = False
                if call.data == "promo_yes":
                    if main.check_promo:
                        main.ask_promo = True
                        bot.send_message(user_id, text=f"Введите промокод ↘️:")
                if call.data == "promo_no":
                    if main.check_promo:
                        main.ask_promo = False
                        main.check_promo = False
                        main.get_menu_info(user_id, main.engine)
                        bot.send_message(user_id, text=main.menu_txt(), reply_markup=main.kb_menu,parse_mode=telegram.ParseMode.MARKDOWN)
                if call.data == "back":
                    bot.send_message(user_id, text=main.menu_txt(), reply_markup=main.kb_menu,parse_mode=telegram.ParseMode.MARKDOWN)



bot.polling()

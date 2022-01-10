from threading import *
import threading
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
import pickle
import re
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import random
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import sys
import traceback
import stun
import platform
import pandas as pd
import gspread
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from oauth2client.service_account import ServiceAccountCredentials
import telebot
from telebot import types
import logging
import boto3
bot = telebot.TeleBot('1927801847:AAEZquHVkEv5V9cUUsU_tB5st5o4BgMaGyk')
logging.basicConfig(filename=f'1.log')



def download_pic(name, aws_access_key_id_ = 'AKIARDGRAYJYA7GGVPDT', aws_secret_access_key_ = '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'):
    s3 = boto3.client(
      service_name='s3',
      region_name='eu-west-3',
      aws_access_key_id=aws_access_key_id_,
      aws_secret_access_key=aws_secret_access_key_
      )
    aws_path = 'screens/' + name
    linux_path = '/home/ubuntu/dima/' + name
    s3.download_file('genlead', aws_path, linux_path)



def upload_file_to_s3(name, aws_access_key_id_ = 'AKIARDGRAYJYA7GGVPDT', aws_secret_access_key_ = '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'):
    s3 = boto3.client(
      service_name='s3',
      region_name='eu-west-3',
      aws_access_key_id=aws_access_key_id_,
      aws_secret_access_key=aws_secret_access_key_
      )

    if platform.system() == 'Windows':
        server_path = 'C:\\Users\\Ваня\\PycharmProjects\\pythonProject\\venv\\dima\\' + name
    else:
        server_path = '/home/ubuntu/dima/' + name
    aws_path = 'screens/' + name
    s3.upload_file(server_path,'genlead', aws_path)


def scroll(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1, 3))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def parsing_message(acc, driver, engine):
    bot.send_message(-595497191,'начал парсить message')
    try:
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
        message_button = driver.find_element_by_partial_link_text("Messaging").click()
        time.sleep(random.uniform(5, 10))

        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
        dilog_button = driver.find_element_by_xpath("//a[@data-control-name = 'view_message']").click()

        time.sleep(random.uniform(1, 2))
        a = driver.find_elements_by_tag_name('a')
        acc_number = []
        acc_name = []
        dilog_button = driver.find_element_by_xpath("//a[@data-control-name = 'view_message']").click()
        time.sleep(random.uniform(1, 2))

        for j in range(0, 1000):
            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        name = []
        mes_date = []
        last_message = []
        process_dttm = []
        for n in range(len(a)):
            if len(a[n].text.split('\n')) in (5, 7):
                acc_number.append(acc.num)
                acc_name.append(acc.name)
                name.append(a[n].text.split('\n')[0])
                mes_date.append(a[n].text.split('\n')[1])
                last_message.append(a[n].text.split('\n')[2])
                process_dttm.append(datetime.now())
        df = pd.DataFrame({'acc_number': acc_number, 'acc_name': acc_name, 'name': name, 'mes_date': mes_date,
                           'last_message': last_message, 'process_dttm': process_dttm})
        bot.send_message(-595497191 ,f"Спарсил сообщения у {acc.name}")
        with engine.connect() as con:
            con.execute(f"""delete from link.messages
                            where acc_number = {acc.num};""")
            con.close()
        df.to_sql('messages', engine, schema='link', if_exists='append', index=False)
        bot.send_message(-595497191, f"Загрузил сообщения {acc.name} в базу")
    except:
        acc.driver = entrance(acc, engine)
        bot.send_message(-595497191, "ERROR - " + traceback.format_exc())
        bot.send_message(-595497191, f"{acc.name} заново подключается к driver")


def parsing_unread_message(acc, driver, engine):
    bot.send_message(-595497191,'начал парсить непрочитанные')
    try:
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
        message_button = driver.find_element_by_partial_link_text("Messaging").click()
        time.sleep(random.uniform(5, 10))

        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
        dilog_button = driver.find_element_by_class_name('msg-conversation-card__message-snippet-body').click()

        time.sleep(random.uniform(1, 2))
        dilog_button = driver.find_element_by_class_name('msg-conversation-card__message-snippet-body').click()
        time.sleep(random.uniform(1, 2))

        url = driver.current_url
        url_unread = url + '?filter=unread'
        driver.get(url_unread)

        time.sleep(random.uniform(1, 2))
        a = driver.find_elements_by_tag_name('a')
        acc_number = []
        acc_name = []
        name = []
        mes_date = []
        last_message = []
        process_dttm = []
        for n in range(len(a)):
            if len(a[n].text.split('\n')) in (5, 7):
                acc_number.append(acc.num)
                acc_name.append(acc.name)
                name.append(a[n].text.split('\n')[0])
                mes_date.append(a[n].text.split('\n')[1])
                last_message.append(a[n].text.split('\n')[2])
                process_dttm.append(datetime.now())
        df = pd.DataFrame({'acc_number': acc_number, 'acc_name': acc_name, 'name': name, 'mes_date': mes_date,
                           'last_message': last_message, 'process_dttm': process_dttm})
        bot.send_message(-595497191 ,f"Спарсил unread сообщения у {acc.name}")
        with engine.connect() as con:
            con.execute(f"""delete from link.un_messages
                            where acc_number = {acc.num};""")
            con.close()
        df.to_sql('un_messages', engine, schema='link', if_exists='append', index=False)
        bot.send_message(-595497191 ,f"Загрузил сообщения {acc.name} в базу")
    except:
        bot.send_message(-595497191, f"ERROR - " + traceback.format_exc())
        bot.send_message(-595497191, f"{acc.name} потерял driver - сессию и заходит заново")
        acc.driver = entrance(acc, engine)


def parsing_con(acc, driver, engine):
    try:
        My = driver.find_element_by_partial_link_text("My")
        My.click()
        time.sleep(random.uniform(5, 10))
        element = WebDriverWait(driver, 500).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
        try:
            element = WebDriverWait(driver, 500).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
            Con = driver.find_element_by_class_name('mn-community-summary__entity-info')
            Con.click()
        except NoSuchElementException:
            element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
            Con = driver.find_element_by_link_text('Connections')
            Con.click()
        element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
        for j in range(0, 10):
            driver.execute_script("window.scrollTo(0, {});".format(random.uniform(30, 10)))
            time.sleep(random.uniform(1, 3))
            scroll(driver)
        li = driver.find_elements_by_tag_name('li')
        acc_number = []
        acc_name = []
        name = []
        date = []
        job = []
        process_dttm = []
        for n in range(len(li)):
            if len(li[n].text.split('\n')) == 7:
                acc_number.append(acc.num)
                acc_name.append(acc.name)
                name.append(li[n].text.split('\n')[1])
                job.append(li[n].text.split('\n')[3])
                date.append(li[n].text.split('\n')[4])
                process_dttm.append(datetime.now())
        df = pd.DataFrame({'acc_number': acc_number, 'acc_name': acc_name, 'name': name, 'job': job, 'date': date,
                           'process_dttm': process_dttm})
        bot.send_message(-595497191, f"Спарсил коннекты у {acc.name}")
        with engine.connect() as con:
            con.execute(f"""delete from link.connections
                            where acc_number = {acc.num};""")
            con.close()
        df.to_sql('connections', engine, schema='link', if_exists='append', index=False)
        bot.send_message(-595497191, f"Загрузил коннекты {acc.name} в базу")
    except:
        bot.send_message(-595497191, f"ERROR - " + traceback.format_exc())
        bot.send_message(-595497191, f"{acc.name} потерял driver - сессию и заходит заново")
        acc.driver = entrance(acc, engine)


def entrance(acc, engine):
    try:
        LOGIN_URL = "https://www.linkedin.com/login/ru?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"  # стр входа
        BUTTON_XPATH = "/html/body/div/main/div[2]/div[1]/form/div[3]/button"  # кнопка входа
        if platform.system() == 'Windows':
            bot.send_message(-595497191,'Windows')
            options = Options()
            options.add_extension('C:\\Users\\Ваня\\Documents\\medframe\\develop\\extention.crx')
            options.add_argument('ignore-certificate-errors')
            driver = Chrome('C:\\Users\\Ваня\\Documents\\medframe\\develop\\chromedriver.exe', options=options)
            bot.send_message(-595497191,'Driver готов')
        else:
            bot.send_message(-595497191,'nowin32')
            options = Options()
            #options.add_argument('--proxy-server=%s' % acc.proxy)
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = Chrome(options=options)
        driver.get(LOGIN_URL)
        bot.send_message(-595497191,'driver get url')
        login = driver.find_element_by_name('session_key')
        login.send_keys(acc.login)

        time.sleep(random.uniform(1, 2))

        password = driver.find_element_by_name('session_password')
        password.send_keys(acc.password)

        time.sleep(random.uniform(1, 3))

        driver.find_element_by_xpath(BUTTON_XPATH).click()
        bot.send_message(-595497191, f"{acc.name} выполнен вход")
        return driver
    except:
        bot.send_message(-595497191, f"{acc.name} не смог зайти в аккаунт")
        sys.exit()



def get_screen_connections(engine, acc):
    try:
        df = pd.read_sql(f'''select po.url, po.name from link.potential_clients po
                            join link.connections c on po.name = c.name
                            where c.acc_number = {acc.num}
                            and screenshots is not null
                            limit 5''', engine)
        if not df.empty:
            bot.send_message(-595497191, f"{acc.name} пошёл скринить {len(df)} аккаунтов из своего списка коннетов")
            for i in range(len(df)):
                url = df['url'][i]
                name = df['name'][i]
                if '%' in url:
                    url = url.replace('%', '%%')
                driver = acc.driver
                driver.get(url)
                time.sleep(random.uniform(5, 15))
                try:
                    div = driver.find_elements_by_tag_name('div')
                    about_count = 0
                    for row in div:
                        if 'About' in row.text and about_count == 0:
                            about = str(re.findall('\nAbout\n.+\n', str(row.text))[0]).replace('\nAbout\n', '').replace('\n','')
                            about_count += 1
                    engine.connect().execute(f"""update link.potential_clients
                                            set about = '{about}'
                                            where url = '{url}';""")
                    bot.send_message(-595497191, f"{acc.name} получил поле about")
                except:
                    pass
                driver.maximize_window()
                driver.execute_script("window.scrollBy(0,280)", "")
                try:
                    driver.find_element_by_xpath('//button[text()="see more"]').click()
                    bot.send_message(-595497191,"Сделал screen")
                    driver.get_screenshot_as_file(f"1_{name}.png")
                    upload_file_to_s3(f"1_{name}.png")
                except:
                    driver.get_screenshot_as_file(f"1_{name}.png")
                    upload_file_to_s3(f"1_{name}.png")
                    bot.send_message(-595497191,"Сделал screen")

                time.sleep(random.uniform(1, 2))
                try:
                    flag = driver.find_element_by_xpath('//h2[text()="Experience"]')
                    driver.execute_script("arguments[0].scrollIntoView();", flag)
                    driver.execute_script("window.scrollBy(0,-100)", "")
                    driver.get_screenshot_as_file(f"2_{name}.png")
                    upload_file_to_s3(f"2_{name}.png")
                    bot.send_message(-595497191,"Сделал screen")
                    path = f"2_{name}.png" + ";" + f"1_{name}.png"
                    engine.connect().execute(f"""update link.potential_clients
                                            set screenshots = '{path}'
                                            where url = '{url}';""")
                    bot.send_message(-595497191, f"{acc.name} загрузил скриншоты")
                except:
                    driver.execute_script("window.scrollBy(0,280)", "")
                    driver.get_screenshot_as_file(f"2_{name}.png")
                    upload_file_to_s3(f"2_{name}.png")
                    path = f"2_{name}.png" + ";" + f"1_{name}.png"
                    engine.connect().execute(f"""update link.potential_clients
                                            set screenshots = '{path}'
                                            where url = '{name}';""")
                    bot.send_message(-595497191, f"{acc.name} загрузил скриншоты")
        else:
            bot.send_message(-595497191, f"У {acc.name} собраны скрины из списка текущих коннектов")
    except:
        bot.send_message(-595497191, "ERROR - " + traceback.format_exc())
        acc.driver = entrance(acc, engine)


def send_connection(con_cnt, engine, acc):
    message = f'I’m {acc.first_name}, the {acc.position} at Medframe. We are working on data preparation solutions for medical AI. \n\nI thought it would be a good idea we connect.\nBest Regards, {acc.first_name}'

    df = pd.read_sql(f'''select * from link.potential_clients 
                        where acc_number = {acc.num} and status = 'nan'
                                            limit {con_cnt}''', engine)
    count = 0
    n = 0  # счётчик на количество новых коннектов
    bot.send_message(-595497191, f'{acc.name} - запускаю отправку коннектов')
    bot.send_message(-595497191, f'{acc.name} - планирую зайти в {con_cnt} профилей')
    while n < con_cnt:
        time.sleep(random.uniform(1, 2))
        url = df['url'][n]
        url_screen = url.split('https://www.linkedin.com/in/')[1]
        if '%' in url:
            url = url.replace('%', '%%')
        message_to_send = 'Hi, ' + str(
            df['firstName'][n]) + '!\n ' + message  # формируем приветствие с именем человека
        try:
            driver = acc.driver
            driver.get(url)  # открываем профиль
            bot.send_message(-595497191, f'{acc.name} - открыл профиль, url_name - {url_screen}')
            try:
                div = driver.find_elements_by_tag_name('div')
                about_count = 0
                for row in div:
                    if 'About' in row.text and about_count == 0:
                        about = str(re.findall('\nAbout\n.+\n', str(row.text))[0]).replace('\nAbout\n', '').replace(
                            '\n', '')
                        about_count += 1
                engine.connect().execute(f"""update link.potential_clients
                                        set about = '{about}'
                                        where url = '{url}';""")
                bot.send_message(-595497191 ,f"{acc.name} - загрузил поле about в базу")
            except:
                pass
            driver.maximize_window()
            driver.execute_script("window.scrollBy(0,280)", "")
            try:
                driver.find_element_by_xpath('//button[text()="see more"]').click()
                driver.get_screenshot_as_file(f"1_{url_screen}.png")
                upload_file_to_s3(f"1_{url_screen}.png")
                bot.send_message(-595497191, f"{acc.name} - нажал see more")
                bot.send_message(-595497191, f"{acc.name} - cделал screen1 и залил на S3")
            except:
                driver.get_screenshot_as_file(f"1_{url_screen}.png")
                upload_file_to_s3(f"1_{url_screen}.png")
                bot.send_message(-595497191, f"{acc.name} - cделал screen1 и залил на S3")
            time.sleep(random.uniform(1, 2))
            try:
                flag = driver.find_element_by_xpath('//h2[text()="Experience"]')
                driver.execute_script("arguments[0].scrollIntoView();", flag)
                driver.execute_script("window.scrollBy(0,-100)", "")
                driver.get_screenshot_as_file(f"2_{url_screen}.png")
                upload_file_to_s3(f"2_{url}.png")
                bot.send_message(-595497191, f"{acc.name} - cделал screen2 и залил на S3")
                path = f"2_{url_screen}.png" + ";" + f"1_{url_screen}.png"
                engine.connect().execute(f"""update link.potential_clients
                                        set screenshots = '{path}'
                                        where url = '{url}';""")
                bot.send_message(-595497191 ,f"{acc.name} - записал путь скринов в базу ")

            except:
                driver.execute_script("window.scrollBy(0,280)", "")
                driver.get_screenshot_as_file(f"2_{url_screen}.png")
                upload_file_to_s3(f"2_{url_screen}.png")
                bot.send_message(-595497191, f"{acc.name} - cделал screen2 и залил на S3")
                path = f"2_{url_screen}.png"
                engine.connect().execute(f"""update link.potential_clients
                                        set screenshots = '{path}'
                                        where url = '{url}';""")
                bot.send_message(-595497191 ,f"{acc.name} - записал путь скринов в базу ")
            driver.execute_script("window.scrollTo(document.body.scrollHeight,0 );")
            bot.send_message(-595497191, f"{acc.name} - приступаю к отправке приветсвия")
            try:
                try:
                    bot.send_message(-595497191, f"{acc.name} - пробую TRY1")
                    connect_button = driver.find_element_by_xpath("//button[@data-control-name = 'connect']")
                    driver.execute_script("arguments[0].click()", connect_button)  # нажимаем connect
                    bot.send_message(-595497191,f"{acc.name} - нажал connect")

                    time.sleep(random.uniform(1, 2))

                    add_note = driver.find_element_by_xpath("//button[@aria-label='Add a note']")
                    driver.execute_script("arguments[0].click()", add_note)  # нажимаем добавить приветсвие
                    bot.send_message(-595497191,f"{acc.name} - нажал Add a note")
                    time.sleep(random.uniform(1, 2))

               
                    text_paste = driver.find_element_by_name('message')
                    text_paste.send_keys(message_to_send)  # вставляем письмо приветсвия
                    bot.send_message(-595497191,f"{acc.name} - вставил приветсвие")
                    time.sleep(random.uniform(1, 2))

                    send = driver.find_element_by_xpath("//button[@aria-label='Send now']")
                    driver.execute_script("arguments[0].click()", send)
                    bot.send_message(-595497191, f"{acc.name} - нажал Send now")
                    time.sleep(random.uniform(60, 180))  #
                    count += 1
                    engine.connect().execute(f"""update link.potential_clients
                                        set status = 'con_sended',
                                            process_dttm = now()
                                        where url = '{url}';
                                        update link.acc_info
                                        set daily_count = daily_count + 1
                                         where acc_number = {acc.num}""")
                    bot.send_message(-595497191, f"{acc.name} - update status = 'con_sended' в базе")
                    n += 1
                except:
                    try:
                        try:
                            bot.send_message(-595497191, f"{acc.name} -  пробую TRY2(из more 2 раза жать connect, кнопка 4 по счёту)")
                            # когда кнопка connect в more
                            buttons = driver.find_elements_by_tag_name("button")
                            time.sleep(random.uniform(1, 2))
                            more = [btn for btn in buttons if btn.text == 'More']
                            more[0].click()
                            bot.send_message(-595497191, f"{acc.name} - нажал More")
    
                            time.sleep(random.uniform(1, 2))
    
                            l = driver.find_elements_by_xpath("//div[@role = 'button']")
                            l[3].click()
                            time.sleep(random.uniform(1, 2))
                            bot.send_message(-595497191, f"{acc.name} - нажал Connect выпадающий")
    
                            driver.find_element_by_xpath("//button[@aria-label = 'Connect']").click()
                            time.sleep(random.uniform(1, 2))
                            bot.send_message(-595497191, f"{acc.name} - нажал Connect button")
    
                            add_note = driver.find_element_by_xpath("//button[@aria-label='Add a note']")
                            driver.execute_script("arguments[0].click()", add_note)  # нажимаем добавить приветсвие
                            bot.send_message(-595497191, f"{acc.name} - нажал Add a note")
    
                            time.sleep(random.uniform(1, 2))
    
                            text_paste = driver.find_element_by_name('message')
                            text_paste.send_keys(message_to_send)  # вставляем письмо приветсвия
                            bot.send_message(-595497191, f"{acc.name} - нажал вставил приветсвие")
    
                            time.sleep(random.uniform(1, 2))
    
                            send = driver.find_element_by_xpath("//button[@aria-label='Send now']")
                            driver.execute_script("arguments[0].click()", send)
                            bot.send_message(-595497191, f"{acc.name} - нажал Send now")
                            time.sleep(random.uniform(60, 180))  #
                            count += 1
                            engine.connect().execute(f"""update link.potential_clients
                                                    set status = 'con_sended',
                                                        process_dttm = now()
                                                    where url = '{url}';
                                                    update link.acc_info
                                                    set daily_count = daily_count + 1
                                                     where acc_number = {acc.num}""")
                            bot.send_message(-595497191, f"{acc.name} - update status = 'con_sended' в базе")
                            n += 1
                        except:
                            bot.send_message(-595497191, f"{acc.name} -  пробую TRY3 (из more 1 раз жать connect, кнопка 4 по счёту)")
                            buttons = driver.find_elements_by_tag_name("button")
                            time.sleep(random.uniform(1, 2))
                            more = [btn for btn in buttons if btn.text == 'More']
                            more[0].click()
                            bot.send_message(-595497191, f"{acc.name} - нажал More")
                            time.sleep(random.uniform(1, 2))
    
                            l = driver.find_elements_by_xpath("//div[@role = 'button']")
                            l[3].click()
                            time.sleep(random.uniform(1, 2))
                            bot.send_message(-595497191, f"{acc.name} - нажал Connect выпадающий")
    
                            add_note = driver.find_element_by_xpath("//button[@aria-label='Add a note']")
                            driver.execute_script("arguments[0].click()", add_note)  # нажимаем добавить приветсвие
                            bot.send_message(-595497191, f"{acc.name} - нажал Add a note")
    
                            time.sleep(random.uniform(1, 2))
                            text_paste = driver.find_element_by_name('message')
                            text_paste.send_keys(message_to_send)  # вставляем письмо приветсвия
                            bot.send_message(-595497191, f"{acc.name} - вставил приветсвие")
    
                            time.sleep(random.uniform(1, 2))
    
                            send = driver.find_element_by_xpath("//button[@aria-label='Send now']")
                            driver.execute_script("arguments[0].click()", send)
                            bot.send_message(-595497191, f"{acc.name} - нажал Send now")
                            time.sleep(random.uniform(60, 180))  #
                            count += 1
                            engine.connect().execute(f"""update link.potential_clients
                                                    set status = 'con_sended',
                                                        process_dttm = now()
                                                    where url = '{url}';
                                                    update link.acc_info
                                                    set daily_count = daily_count + 1
                                                     where acc_number = {acc.num}""")
                            bot.send_message(-595497191, f"{acc.name} - update status = 'con_sended' в базе ")
                            n += 1
                    except:
                        try:
                            # когда кнопка connect в more и 3 по списку
                            bot.send_message(-595497191, f"{acc.name} -  пробую TRY4 (из more 2 раза жать connect, кнопка 3 по счёту)")
                            buttons = driver.find_elements_by_tag_name("button")
                            time.sleep(random.uniform(1, 2))
                            more = [btn for btn in buttons if btn.text == 'More']
                            more[0].click()
                            bot.send_message(-595497191, f"{acc.name} - нажал More")

                            time.sleep(random.uniform(1, 2))

                            l = driver.find_elements_by_xpath("//div[@role = 'button']")
                            l[2].click()
                            time.sleep(random.uniform(1, 2))
                            bot.send_message(-595497191, f"{acc.name} - нажал Connect выпадающий")

                            driver.find_element_by_xpath("//button[@aria-label = 'Connect']").click()
                            time.sleep(random.uniform(1, 2))
                            bot.send_message(-595497191, f"{acc.name} - нажал Connect button")

                            add_note = driver.find_element_by_xpath("//button[@aria-label='Add a note']")
                            driver.execute_script("arguments[0].click()", add_note)  # нажимаем добавить приветсвие
                            bot.send_message(-595497191, f"{acc.name} - нажал Add a note")

                            time.sleep(random.uniform(1, 2))

                            text_paste = driver.find_element_by_name('message')
                            text_paste.send_keys(message_to_send)  # вставляем письмо приветсвия
                            bot.send_message(-595497191, f"{acc.name} - нажал вставил приветсвие")

                            time.sleep(random.uniform(1, 2))

                            send = driver.find_element_by_xpath("//button[@aria-label='Send now']")
                            driver.execute_script("arguments[0].click()", send)
                            bot.send_message(-595497191, f"{acc.name} - нажал Send now")
                            time.sleep(random.uniform(60, 180))  #
                            count += 1
                            engine.connect().execute(f"""update link.potential_clients
                                                    set status = 'con_sended',
                                                        process_dttm = now()
                                                    where url = '{url}';
                                                    update link.acc_info
                                                    set daily_count = daily_count + 1
                                                     where acc_number = {acc.num}""")
                            bot.send_message(-595497191, f"{acc.name} - update status = 'con_sended' в базе")
                            n += 1
                        except:
                            bot.send_message(-595497191,
                                             f"{acc.name} -  пробую TRY5 (из more 1 раз жать connect, кнопка 3 по счёту)")
                            buttons = driver.find_elements_by_tag_name("button")
                            time.sleep(random.uniform(1, 2))
                            more = [btn for btn in buttons if btn.text == 'More']
                            more[0].click()
                            bot.send_message(-595497191, f"{acc.name} - нажал More")
                            time.sleep(random.uniform(1, 2))

                            l = driver.find_elements_by_xpath("//div[@role = 'button']")
                            l[2].click()
                            time.sleep(random.uniform(1, 2))
                            bot.send_message(-595497191, f"{acc.name} - нажал Connect выпадающий")

                            add_note = driver.find_element_by_xpath("//button[@aria-label='Add a note']")
                            driver.execute_script("arguments[0].click()", add_note)  # нажимаем добавить приветсвие
                            bot.send_message(-595497191, f"{acc.name} - нажал Add a note")

                            time.sleep(random.uniform(1, 2))
                            text_paste = driver.find_element_by_name('message')
                            text_paste.send_keys(message_to_send)  # вставляем письмо приветсвия
                            bot.send_message(-595497191, f"{acc.name} - вставил приветсвие")

                            time.sleep(random.uniform(1, 2))

                            send = driver.find_element_by_xpath("//button[@aria-label='Send now']")
                            driver.execute_script("arguments[0].click()", send)
                            bot.send_message(-595497191, f"{acc.name} - нажал Send now")
                            time.sleep(random.uniform(60, 180))  #
                            count += 1
                            engine.connect().execute(f"""update link.potential_clients
                                                    set status = 'con_sended',
                                                        process_dttm = now()
                                                    where url = '{url}';
                                                    update link.acc_info
                                                    set daily_count = daily_count + 1
                                                     where acc_number = {acc.num}""")
                            bot.send_message(-595497191, f"{acc.name} - update status = 'con_sended' в базе ")
                            n += 1
                        
            except:
                bot.send_message(-595497191, f"{acc.name} не смог получить коннект {url}")
                engine.connect().execute(f"""update link.potential_clients
                                    set status = 'can_not_send',
                                    process_dttm = now()
                                    where url = '{url}';""")
                n += 1
                bot.send_message(-595497191,
                                 f"{acc.name} - update status = 'con_NOT_sended' в базе")
                time.sleep(random.uniform(60, 180))  #
        except:
            bot.send_message(-595497191, f"{acc.name} потерял driver - сессию и заходит заново")
            bot.send_message(-595497191,'ошибка' + traceback.format_exc())
            acc.driver = entrance(acc, engine)
        time.sleep(random.uniform(1, 2))
    bot.send_message(-595497191, f"{acc.name} перешёл по {con_cnt} профилям, из них кинул {count} коннектов")
def what_acc(engine):
    """Определяет с каким аккаунтом нужно работать по ip машины, на которой запущен код"""
    ip = stun.get_ip_info()[1]
    bot.send_message(-595497191,ip)
    logging.info('ЗАПУСК')
    logging.info('ip')
    df = pd.read_sql(f"""select * from link.acc_info
    where ip = '{ip}' limit 1""",engine)
    if df.empty:
        raise NameError('такого ip нет в таблице link.acc_info ')
    else:
        return df


def main():
    try:
        db_string = "postgresql://postgres:sjvnfi_LFMR740@internal.cfnsbden5utu.us-east-2.rds.amazonaws.com:5432/"
        engine = create_engine(db_string, pool_size=10, max_overflow=20)
        link = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']  # задаем ссылку на Гугл таблици
        my_creds = ServiceAccountCredentials.from_json_keyfile_name('gogol.json', link)
        client = gspread.authorize(my_creds)
        sheet1 = client.open('link').worksheet("unread")
        sheet2 = client.open('link').worksheet("all_dialogs")

        class account:
            def __init__(self, name, first_name, login, password, ip, i, position):
                self.login = login
                self.password = password
                self.ip = ip
                self.name = name
                self.first_name = first_name
                self.count = 0
                self.driver = 0
                self.num = i
                self.position = position
        df = what_acc(engine)
        acc = account(df['acc_name'][0], df['acc_first_name'][0], df['login'][0], df['password'][0], df['ip'][0],
                      df['acc_number'][0], df['position'][0])

        acc.driver = entrance(acc,engine)
        n = 0
        count_daily = 0
        finish_day = datetime.now().day - 1
        finish_hour = datetime.now().hour - 1
        count_pars = 0
        count_unread = 0
        while True:
            df_daily_con = pd.read_sql(f'''select daily_count from link.acc_info
                                        where acc_number = {acc.num}''', engine)
            daily_con = df_daily_con['daily_count'][0]
            if daily_con >= 3 and count_daily == 0:
                bot.send_message(-595497191, f"{acc.name} отправил 15 коннектов ушёл отдыхать до завтра")
                finish_day = datetime.now().day  # день, в который бот больше не будет работать
                count_daily += 1
            if count_unread != 0 and datetime.now().hour != finish_hour:
                count_unread = 0
            if datetime.now().day > finish_day and datetime.now().hour > 8:
                if count_daily != 0:
                    engine.connect().execute(f"""update  link.acc_info 
                                                set daily_count = 0
                                                where acc_number = {acc.num};""")
                    count_daily = 0
                    count_pars = 0

                if count_pars == 0:
                    parsing_con(acc, acc.driver, engine)
                    parsing_message(acc, acc.driver, engine)
                    get_screen_connections(engine, acc)
                    #df = pd.read_sql("""select * from link.view_mes""", engine)
                    #sheet2.update([df.columns.values.tolist()] + df.values.tolist())
                    #bot.send_message(-595497191, f"Обновил диалоги у {acc.name} на листе all_dialogs")
                    count_pars += 1
                send_connection(int(random.uniform(2,5)),engine,acc)
        time.sleep(random.uniform(1, 2))
    except:
        bot.send_message(-595497191, f"Ай блииин :( {acc.name} упал")
        bot.send_message(-595497191, "ERROR - " + traceback.format_exc())

main()




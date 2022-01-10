from sqlalchemy.orm import Session

#from . import models, schemas
from database import engine
import models, schemas
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
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
import pandas as pd
import gspread
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import stun
import logging
import platform
import telebot
from telebot import types

bot = telebot.TeleBot('1927801847:AAEZquHVkEv5V9cUUsU_tB5st5o4BgMaGyk')


def init(engine):
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
                  df['acc_number'][0], df['position'])
    return acc

def what_acc(engine):
    """Определяет с каким аккаунтом нужно работать по ip машины, на которой запущен код"""
    ip = stun.get_ip_info()[1]
    print(ip)
    logging.basicConfig(filename='example.log', level=logging.DEBUG)
    logging.info('So should this')
    df = pd.read_sql(f"""select * from link.acc_info
    where ip = '{ip}' limit 1""",engine)
    if df.empty:
        raise NameError('такого ip нет в таблице link.users ')
    else:
        return df

def entrance(acc, engine):
    try:
        LOGIN_URL = "https://www.linkedin.com/login/ru?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"  # стр входа
        BUTTON_XPATH = "/html/body/div/main/div[2]/div[1]/form/div[3]/button"  # кнопка входа
        if platform.system() == 'Windows':
            print('Windows')
            options = Options()
            options.add_extension('C:\\Users\\Ваня\\Documents\\medframe\\develop\\extention.crx')
            options.add_argument('ignore-certificate-errors')
            driver = Chrome('C:\\Users\\Ваня\\Documents\\medframe\\develop\\chromedriver.exe', options=options)
            print('Driver готов')
        else:
            print('nowin32')
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = Chrome(options=options)
        driver.get(LOGIN_URL)
        print('driver get url')
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

def send_message(name,message,driver):
    Messaging = driver.find_element_by_partial_link_text("Messaging").click()
    time.sleep(random.uniform(1,3))
    time.sleep(random.uniform(1,3))
    driver.find_element_by_name('searchTerm').send_keys(name)
    driver.find_element_by_name('searchTerm').send_keys(u'\ue007')
    time.sleep(random.uniform(1,3))
    dilog = driver.find_element_by_xpath(f'//h3[text()="{name}"]').click()
    all_messages = driver.find_elements_by_tag_name('p')
    print('find p')
    all_messages[-5].send_keys(message)
    all_messages
    time.sleep(random.uniform(1,3))
    driver.find_element_by_xpath('//button[text()="Send"]').click()

def check_allow(acc_name,engine):
    df = pd.read_sql(f"""select status from link.acc_info where acc_name = {acc_name})""")
    if not df.empty:
        if df['status'] == 'sending_message':
            return False
        else:
            return True


def parsing_unread_message(acc,driver,engine):
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
    message_button = driver.find_element_by_partial_link_text("Messaging").click()
    time.sleep(random.uniform(2,5))
    url = driver.current_url
    url_unread = url + '?filter=unread'
    driver.get(url_unread)
    time.sleep(random.uniform(1,2))
    a = driver.find_elements_by_tag_name('a')
    acc_number = []
    acc_name = []
    name = []
    mes_date = []
    last_message = []
    process_dttm = []
    dialog = []
    for n in range(len(a)):
        if len(a[n].text.split('\n')) in (5,7):
            print(a[n].text.split('\n'))
            acc_number.append(acc.num)
            acc_name.append(acc.name)
            name.append(a[n].text.split('\n')[0])
            mes_date.append(a[n].text.split('\n')[1])
            last_message.append(a[n].text.split('\n')[2])
            process_dttm.append(datetime.now())
        if len(a[n].text.split('\n')) == 8:
            print(a[n].text.split('\n'))
            acc_number.append(acc.num)
            acc_name.append(acc.name)
            name.append(a[n].text.split('\n')[1])
            mes_date.append(a[n].text.split('\n')[2])
            last_message.append(a[n].text.split('\n')[3])
            process_dttm.append(datetime.now())
    for i in range(len(name)):
        driver.find_element_by_xpath(f'//h3[text()="{name[i]}"]').click()
        time.sleep(random.uniform(1,2))
        p = driver.find_elements_by_tag_name('div')
        get = False
        res = []
        j = 0
        for n in range(len(p)):
            if f'Open the options list in your conversation with {name[i]}' in p[n].text:
                number = n
                break
        for row in p[number].text.split('\n'):
            if 'Open the options list in your conversation' in row:
                get = True
            if 'Attach' in row:
                get = False
            if get and 'View' not in row and "sent the following message" not in row and "Reply" not in row and "Open the options list" not in row and "Status is" not in row:
                if 'AM' in row or 'PM' in row:
                    row = '*'+row+'*'
                print(row)
                res.append(row)
        res.pop(len(res)-1)
        res.pop(len(res)-1)
        dialog.append('\n'.join(res))
        time.sleep(random.uniform(1,2))
        path = f"1_dialog_{name[i]}.png"
        driver.get_screenshot_as_file(path)
        #driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
        print(f"{acc.name} unread messages loaded to database")
        engine.connect().execute(f"""insert into link.un_messages values ({acc_number[i]},'{acc_name[i]}','{name[i]}','{mes_date[i]}','{last_message[i]}','{process_dttm[i]}','{dialog[i]}','{path}')""")



def get_id(db: Session):
    print(db.query(models.id).first())
    return db.query(models.id).first()

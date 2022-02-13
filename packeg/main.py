# -*- coding: utf-8 -*-
from StandartMethod import *
import threading
logo = '[Butterfly] '


if __name__ == "__main__":
    print(logo + f'key: {headless.get_hwid_hash()}')
    # User = connetcion_database(headless.get_hwid(), headless.get_hwid_hash())
    # User.get_register()
    # if User.get_success():
    # print(logo + f'Лицензия активна до: {str(User.get_full_data()["date"]).split(".")[0]}')
    settings = headless.get_settings()
    count_streams = settings['Flow_count']
    for flow in range(count_streams):
        stream = threading.Thread(target=start_work.start)
        stream.start()
    stream.join()
    print(logo + 'Проверка завершена')
    time.sleep(100000)
    # else:
    #     print(logo + 'Срок вашей лицензии истек')
    #     time.sleep(100000)
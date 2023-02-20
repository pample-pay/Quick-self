import os
import json
import socket

from datetime import datetime

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_secret(setting, secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

def get_token(card_num):

    BASE_DIR = getattr(settings, 'BASE_DIR', None)
    file_path = "socket_port.json" # 통신 API 소켓 파일

    with open(os.path.join(BASE_DIR,file_path), encoding='utf-8') as f:
        socket_port = json.load(f)

    HOST = socket_port["HOST"]
    PORT = int(socket_port["PORT"])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    Space = " "*150
    card_num = card_num+"=0000"
    CardData = "37" + card_num + Space[0:127 - 2 - len(card_num)]

    date = datetime.today().strftime("%Y%m%d")[2:]
    time = datetime.today().strftime("%H%M%S")   

    SendData = [
        "S-OILQS"
        + "23933000010112110830"
        + "0200"
        + "10"   
        + "2393300001"
        + Space[0:2]
        + Space[0:2]
        + date
        + time
        + "@"
        + CardData
        + "00"
        + "000000000000"
        + "000000000000"
        + "000000000000"
        + Space[0:16]
        + Space[0:12]
        + Space[0:6]
        + Space[0:1]
        + Space[0:8]
        + Space[0:8]
        + Space[0:1]
        + Space[0:1]
        + Space[0:6]
        + Space[0:12]
        + Space[0:8]
        + Space[0:5]
        + Space[0:1]
        + Space[0:127]
        + Space[0:1]
        + Space[0:12]
        + Space[0:1]
        + Space[0:12]
        + Space[0:3]
        + Space[0:24]
        + "################"
        + "################"
        + Space[0:2]
    ]

    SendData.insert(0, str(len(SendData[0])).zfill(4))

    bytes = (SendData[0]+SendData[1]).encode()

    s.send(bytes)
    data = s.recv(4096)
    s.close()

    recvBuff = data[422:500]

    card_token39 = recvBuff[:39]
    card_token05 = recvBuff[39:]

    return card_token39, card_token05
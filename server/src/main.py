#!/usr/bin/python
import socket
import sys
import pyfcm as fcm

from thread import *
from constants import *
from logger import get_logger

sys.path.append(CONFIG_FILE_PATH)
from config import *

log = get_logger(logFileName="socketServer.log")
con = get_mongo_connection()
db = get_app_db(con)
fcm_service = fcm.FCMNotification(api_key=FCM_SERVER_KEY)


def usage():
    log.info('USAGE: ./server.py port')


def passiveTCP(port):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0",port))
    sock.listen(10)

    return sock


def main():
    port = None
    try:
        port = SOCKET_SERVER_PORT
        if len(sys.argv) == 2:
            port = sys.argv[1]

    except Exception, ex:
        log.error(str(ex))
        usage()
        sys.exit(-1)

    sock = passiveTCP(port)
    while True:
        con, addr = sock.accept()
        start_new_thread(handleClient, (con,))


def handleClient(con):
    alert = get_data_from_peer(con)
    notifyAllUsers(alert["title"], alert["desc"], exclude=alert["token"])


def notifyAllUsers(title, message, exclude=None):
    all_apps = get_all_app_tokens(db)
    if exclude:
        all_apps.remove(exclude)

    fcm_service.notify_multiple_device(registration_ids=all_apps, message_title=title, message_body=message)


if __name__ == '__main__':
    main()

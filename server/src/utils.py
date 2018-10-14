import pymongo
import json
import errno
import socket

from constants import *
sys.path.append(CONFIG_FILE_PATH)
from config import *

def get_mongo_connection():
    return pymongo.MongoClient(MONGO_SERVERS, MONGO_DB_PORT, fsync=True)


def get_app_db(mongo_con):
    return mongo_con[DB_NAME]


def get_alerts_collection(db):
    return db[ALERTS_COLLECTION_NAME]


def get_users_collection(db):
    return db[USERS_COLLECTION_NAME]


def get_all_app_tokens(db):
    users = get_users_collection(db)
    return users.distinct("token")


def get_data_from_peer(con):
    request = None
    try:
        data = con.recv(4096)
        request = json.loads(data)
    except socket.error as se:
        print str(se)
        if se.errno == errno.CONNRESET:
            print "Client died!"
    except Exception, ex:
        print str(ex)
        return None

    return request


def send_data_to_peer(con, data):
    try:
        n = con.send(json.dumps(data))
    except socket.error as se:
        print str(se)
        if se.errno == errno.CONNRESET:
            print "Client died!"
    except Exception, ex:
        print str(ex)
        return -1

    return 0


def get_connection_to_server():
    sock = socket.socket()
    sock.settimeout(3)
    try:
        sock.connect((SOCKET_SERVER_IP, SOCKET_SERVER_PORT))
        sock.settimeout(None)
        return sock
    except socket.error, ex:
        print "Could not connect to %s:%s"%(SOCKET_SERVER_IP, SOCKET_SERVER_PORT)

    return None


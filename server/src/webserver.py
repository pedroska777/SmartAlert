#!/usr/bin/python
import sys
import json
import bottle
import pyfcm as fcm

from bottle import route, abort
#from bson.objectid import ObjectId

from logger import get_logger
from constants import *
from utils import *

sys.path.append(CONFIG_FILE_PATH)
from config import *

log = get_logger(logFileName="webServer.log")
con = get_mongo_connection()
db = get_app_db(con)
fcm_service = fcm.FCMNotification(api_key=FCM_SERVER_KEY)


@route('/register', method='POST')
def user_alert():
    form = None
    try:
        users = get_users_collection(db)
        user = json.load(bottle.request.body)
	
        if "token" not in user:
            raise Exception("App Registration Token missing!")

        fcm_service.notify_single_device(registration_id=user["token"], message_title="Registration Successful!", message_body="Thanks for installing Alert App!")
        users.insert(app)
    except Exception, ex:
        log.error("Exception in create_sessions: %s"%str(ex))
        abort(500, json.dumps({ 'error' : str(ex) }))


@route('/alerts', method='GET')
def get_alerts():
    try:
        alerts = get_alerts_collection(db)
        return {"alerts": alerts.find({})}
    except Exception, ex:
        log.error("Exception in get_alerts: %s"%str(ex))
        abort(500, json.dumps({ 'error' : str(ex) }))


@route('/alerts', method='POST')
def report_alert():
    form = None
    try:
        alerts = get_alerts_collection(db)
        form = json.load(bottle.request.body)
        alert = alerts.insert(form)
        con = get_connection_to_server()
        send_data_to_peer(con, alert)
    except Exception, ex:
        log.error("Exception in report_alert: %s"%str(ex))
        abort(500, json.dumps({ 'error' : str(ex) }))


if __name__ == '__main__':
    bottle.run(host="0.0.0.0", port=WEB_SERVER_PORT, server='twisted')

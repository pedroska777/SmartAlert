#!/usr/bin/python
import sys
import pyfcm as fcm

def get_fcm_service_channel():
   return fcm.FCMNotification(api_key=FCM_SERVER_KEY)
   
def notify_user(user, title, message):
   token = get_app_token_pf_user(user)
   if not token_valid():
       Exception("User token is not valid!")
   
   fcm_service = get_fcm_service_channel()
   fcm_service.notify_single_device(registration_id=token, message_title=title, message_body=message)
   

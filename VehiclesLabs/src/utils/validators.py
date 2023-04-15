import razorpay
import random
from datetime import timedelta
from rest_framework_jwt.settings import api_settings
from django_otp.oath import TOTP
import time

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

def getDate(start, end):
    delta = end - start       # as timedelta
    day = []
    for i in range(delta.days):
        day.append({"date": start + timedelta(days=i), "count": 0})
    return day

def subscriptionCaptured(payment_id, payment_amount):
    client = razorpay.Client(auth=("rzp_test_rdsQVUSPpNkdo3", "jXXxx3WrgbPv1uBTO6agILx6"))
    payment_id = payment_id
    payment_amount = payment_amount
    payment_currency = "INR"
    resp = client.payment.capture(payment_id, payment_amount*100, {"currency":"payment_currency"})
    return resp



def get_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token

def send_otp(phone):
    if phone:
        key = TOTP(key=b'12345678901234567890',
                    step=300,
                    digits=6)
        key = key.token()
        # key = 123456
        return key
    else:
        return False
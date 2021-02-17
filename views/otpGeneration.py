import math
import random
import uuid

from model.model import Otp
from schemas.schema import OtpSchema
from views.mailForNotification import sendNotification


def otpGenreationForUserMail(mailId):
    ob = Otp()
    ob.email = mailId
    ob.uid = uuid.uuid4()
    OTP = ""
    digits = "0123456789"
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    ob.otp = OTP
    ob.save()
    result = OtpSchema().dump(ob)
    print(result.data)
    msg = 'Your OTP Verification for app is '+OTP+' Note..  Please enter otp within 2 minutes and 3 attempts, otherwise it becomes invalid'
    sendNotification(mailId,msg)
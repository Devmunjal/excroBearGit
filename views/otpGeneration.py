import math
import random

from views.mailForNotification import sendNotification


def otpGenreationForUserMail(mailId):
    OTP = ""
    digits = "0123456789"
    filePath = mailId+".txt"
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    msg = 'Your OTP Verification for app is '+OTP+' Note..  Please enter otp within 2 minutes and 3 attempts, otherwise it becomes invalid'
    file2 = open(filePath, "w")
    file2.write(OTP)
    file2.close()
    sendNotification(mailId,msg)
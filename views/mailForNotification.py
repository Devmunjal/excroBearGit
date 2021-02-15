from smtplib import SMTP
# &&&&&&&&&&&&- Your mail id. SENDING OTP FROM mail id
# ************- Your app password. If you do not know how to generate app password for your mail please google.
def sendNotification(mailid,msg):
    # print(mailid,msg)
    s = SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("emailId", "password")
    print(msg)
    s.sendmail('emailId',mailid,msg)

from model.model import *
from app import ma

class UserSchema(ma.ModelSchema):

    class Meta:
        model = User

class KycSchema(ma.ModelSchema):

    class Meta:
        model = Kyc


class OrderSchema(ma.ModelSchema):

    class Meta:
        model = Order


class NotificationSchema(ma.ModelSchema):

    class Meta:
        model = Notification
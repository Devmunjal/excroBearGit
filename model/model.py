from app import db
from model.base import Base
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    country = db.Column(db.String(80))
    metadataForUser = db.Column(db.String(200))
    twoFAtoken = db.Column(db.String(80))
    kycStatus = db.Column(db.BOOLEAN)
    fcmToken = db.Column(db.String(80))
    isAdmin = db.Column(db.BOOLEAN,default=False)

class Order(Base):
    status = db.Column(db.String(80))
    quantity = db.Column(db.Integer)
    demandPrice = db.Column(db.Integer)
    uniqueCode = db.Column(UUID(as_uuid=True))
    currency = db.Column(db.String(80))
    paymentStatus = db.Column(db.String(80))
    buyer = db.Column(UUID(as_uuid=True), db.ForeignKey('user.uid'),nullable=True)
    seller = db.Column(UUID(as_uuid=True), db.ForeignKey('user.uid'))

class Kyc(Base):
    documentName = db.Column(db.String(80))
    documentUrl = db.Column(db.String(200))
    user = db.Column(UUID(as_uuid=True), db.ForeignKey('user.uid'))

class Notification(Base):
    description = db.Column(db.String(200))
    sent_status = db.Column(db.BOOLEAN)
    user = db.Column(UUID(as_uuid=True))
    orderRelated = db.Column(UUID(as_uuid=True), db.ForeignKey('user.uid'))
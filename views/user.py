import os
import uuid
from flask import jsonify, request
from app import app
from model.model import User,Otp
from schemas.schema import UserSchema, OtpSchema
from werkzeug.security import generate_password_hash,check_password_hash
import jwt

from views.mailForNotification import sendNotification
from views.middleWare import token_required
from views.otpGeneration import otpGenreationForUserMail


@app.route("/signup",methods=['POST'])
def createUser():
    if request.method == 'POST':
        try:
            ob = User(**request.json)
            data =  User.query.filter_by(email=ob.email).first()
            if data:
                return jsonify({"error":"Sorry User Exists - 401"})
            else:
                ob.uid = uuid.uuid4()
                ob.password=generate_password_hash(ob.password,method='sha256')
                ob.save()
                result = UserSchema().dump(ob)
                otpGenreationForUserMail(result.data['email'])
                return jsonify(result.data)
        except Exception as error:
            return jsonify({"error": str(error)}), 400

@app.route("/verify",methods=['POST'])
def verifyied():
    try:
        ob = request.json
        user = User.query.filter_by(email=ob['email']).first()
        setattr(user,'verifiedMail',True)
        data = Otp.query.filter_by(email=ob['email']).first()
        res = OtpSchema().dump(data)
        if res.data['otp'] == ob['otp']:
            user.update()
            result = UserSchema().dump(user)
            return jsonify({"data": result.data})
        return jsonify({"error":"Otp does not match"})
    except Exception as error:
        return jsonify({"error": str(error)}), 400

@app.route("/login",methods=['POST'])
def loginUser():
    if request.method =='POST':
        try:
            ob = request.authorization
            data = User.query.filter_by(email=ob.username).first()
            res = UserSchema().dump(data)
            if data :
                if res.data['verifiedMail'] == False:
                    return jsonify({"error":"Please Verify Your Mail"})
                else:
                    if check_password_hash(res.data['password'],ob.password):
                        token=jwt.encode({"userId":res.data['uid'],"password":res.data['password']},key=app.config['SECRET_KEY'],algorithm='HS256')
                        return jsonify({"data": True,"message":"User Exits","token":token})
                    else:
                        return jsonify({"error":True,"message":"Password Does Not match"})
            else:
                return jsonify({"error":True,"message":"User Does Not Exits"})
        except Exception as error:
            return jsonify({"error": str(error)}), 400


@app.route("/generateRefetchUrl",methods=['POST'])
def GenerateRefetchUrl():
    try:
        ob = request.json
        otp = Otp.query.filter_by(email=ob['email']).first()
        if(otp):
            setattr(otp, 'refecthUrl', ob['refetchUrl'])
            setattr(otp,'linkused',False)
            otp.update()
            msg = ob['refetchUrl']+"You can reset your password by click on given link it is only for single use"
            sendNotification(ob['email'],msg)
            result = OtpSchema().dump(otp)
            return jsonify(result.data)
        return jsonify({"error":"You Have No Verified Account"})
    except Exception as error:
        return jsonify({"error": str(error)}), 400

@app.route("/forgetPassword", methods=['POST'])
def forgetPassword():
    try:
        ob = request.json
        otp = Otp.query.filter_by(email=ob['email']).first()
        user = User.query.filter_by(email=ob['email']).first()
        if(otp.linkused!=True and otp.refecthUrl == ob['refetchUrl']):
            setattr(otp, 'linkused', True)
            setattr(user, 'password', generate_password_hash(ob['password'], method='sha256'))
            user.update()
            otp.update()
            result = UserSchema().dump(user)
            return jsonify(result.data)
        else :
            return jsonify({"error":"Forget Password Link Not Found 404"})
    except Exception as error:
        return jsonify({"error": str(error)}), 400

@app.route("/user",methods=['GET','POST','DELETE'])
@token_required
def user_by_id(current_user):
    try:
        user = UserSchema().dump(current_user)
        if request.method == 'GET':
            data = User.query.filter_by(uid=user.data['uid']).first()
            if data:
                data = UserSchema().dump(data).data
                response = jsonify({"result": data})
                return response
            return jsonify({'error': "No User found with id ({})".format(id)}), 400
        if request.method == 'POST':
            ob = User.query.filter_by(uid=user.data['uid']).first()
            if ob:
                for key in request.json:
                    if key=="password":
                        password=generate_password_hash(request.json[key],method='sha256')
                        setattr(ob,key,password)
                    if key=="isAdmin":
                        setattr(ob,key,False)
                    if key!="password" and key!="isAdmin" and key!="email" and key!="verifiedMail":
                        setattr(ob, key, request.json[key])
                ob.update()
                result = UserSchema().dump(ob)
                return jsonify(result.data)
            return jsonify({'error': "No User found with id ({})".format(id)}), 400
        if request.method == 'DELETE':
            ob = User.query.filter_by(uid=user.data['uid']).first()
            if ob:
                ob.delete()
                return jsonify({'id': ob.uid})
            return jsonify({'error': "No User found with id ({})".format(id)}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 400
import uuid
from flask import jsonify, request
from app import app
from model.model import User
from schemas.schema import UserSchema
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from views.middleWare import token_required


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
                return jsonify(result.data)
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
                if check_password_hash(res.data['password'],ob.password):
                    token=jwt.encode({"userId":res.data['uid'],"password":res.data['password']},key=app.config['SECRET_KEY'],algorithm='HS256')
                    return jsonify({"data": True,"message":"User Exits","token":token})
                else:
                    return jsonify({"data":False,"message":"Password Does Not match"})
            else:
                return jsonify({"data":False,"message":"User Does Not Exits"})
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
                    if key!="password" and key!="isAdmin":
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
import jwt
from flask import request,jsonify
from functools import wraps
from app import app
from model.model import User

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token= request.headers['x-access-token']
        if not token:
            return jsonify({"message":"Access Denied! 404"})

        try:
            data = jwt.decode(token,key=app.config['SECRET_KEY'],algorithms=['HS256'])
            current_user = User.query.filter_by(uid=data['userId']).first()
        except Exception as error:
            return jsonify({"error": str(error)}), 400

        return f(current_user,*args,**kwargs)
    return decorated
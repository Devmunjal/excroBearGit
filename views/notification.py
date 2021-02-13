import uuid
from flask import jsonify,request
from app import app
from model.model import Notification
from schemas.schema import NotificationSchema, UserSchema
from views.middleWare import token_required


@app.route("/notification",methods=['POST'])
@token_required
def createNotification(current_user):
    if request.method == 'POST':
        try:
            user = UserSchema().dump(current_user)
            ob = Notification(**request.json)
            ob.uid = uuid.uuid4()
            ob.user = user.data['uid']
            ob.save()
            result = NotificationSchema().dump(ob)
            return jsonify(result.data)
        except Exception as error:
            return jsonify({"error": str(error)}), 400

@app.route("/allNotification/order/<string:id>",methods=['GET'])
@token_required
def getallNotifiationforOrder(current_user,id):
    try:
        data = Notification.query.filter_by(orderRelated=id).all()
        if data:
            if len(data)>1:
                finalRes = []
                for obj in data:
                    res = NotificationSchema().dump(obj)
                    finalRes.append(res.data)
                return jsonify({"result":finalRes})
            return jsonify({"result":data})
        return jsonify({'error': "No Order found for this User ({})".format(id)})
    except Exception as error:
        return jsonify({"error": str(error)}), 400


@app.route("/allNotification/user",methods=['GET'])
@token_required
def getallNotifiationforUser(current_user):
    try:
        user = UserSchema().dump(current_user)
        data = Notification.query.filter_by(user=user.data['uid']).all()
        if data:
            if len(data)>1:
                finalRes = []
                for obj in data:
                    res = NotificationSchema().dump(obj)
                    finalRes.append(res.data)
                return jsonify({"result":finalRes})
            return jsonify({"result":data})
        return jsonify({'error': "No Order found for this User ({})".format(id)})
    except Exception as error:
        return jsonify({"error": str(error)}), 400
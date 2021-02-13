import uuid
from flask import jsonify,request
from app import app
from model.model import Kyc
from schemas.schema import KycSchema, UserSchema
from views.middleWare import token_required


@app.route("/kyc",methods=["POST"])
@token_required
def createKyc(current_user):
    if request.method == 'POST':
        try:
            user = UserSchema().dump(current_user)
            ob = Kyc(**request.json)
            ob.uid = uuid.uuid4()
            ob.user = user.data['uid']
            ob.save()
            result = KycSchema().dump(ob)
            return jsonify(result.data)
        except Exception as error:
            return jsonify({"error": str(error)}), 400

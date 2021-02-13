import uuid
from flask import jsonify,request
from app import app
from model.model import Order
from schemas.schema import OrderSchema, UserSchema
from views.middleWare import token_required


@app.route("/order",methods=['POST'])
@token_required
def createOrder(current_user):
    if request.method == 'POST':
        try:
            user = UserSchema().dump(current_user)
            ob = Order(**request.json)
            ob.seller = user.data['uid']
            ob.uid = uuid.uuid4()
            ob.uniqueCode = uuid.uuid4()
            ob.save()
            result = OrderSchema().dump(ob)
            return jsonify(result.data)
        except Exception as error:
            return jsonify({"error": str(error)}), 400


@app.route("/user/order/buyer",methods=['GET'])
@token_required
def getallOrders_Buyer(current_user):
    try:
        ob=UserSchema().dump(current_user)
        data = Order.query.filter_by(buyer=ob.data['uid']).all()
        if data:
            if len(data)>0:
                finalRes = []
                for obj in data:
                    res = OrderSchema().dump(obj)
                    finalRes.append(res.data)
                return jsonify({"result":finalRes})
        return jsonify({'error': "No Order found for this User ({})".format(id)})
    except Exception as error:
        return jsonify({"error": str(error)}), 400


@app.route("/user/order/seller",methods=['GET'])
@token_required
def getallOrders_Seller(current_user):
    try:
        ob=UserSchema().dump(current_user)
        data = Order.query.filter_by(seller=ob.data['uid']).all()
        if data:
            if len(data)>0:
                finalRes = []
                for obj in data:
                    res = OrderSchema().dump(obj)
                    finalRes.append(res.data)
                return jsonify({"result":finalRes})
        return jsonify({'error': "No Order found for this User ({})".format(id)})
    except Exception as error:
        return jsonify({"error": str(error)}), 400

@app.route("/all_orders_onStatus",methods=['POST'])
@token_required
def allOrdersOnStatus(current_user):
    try:
        ob = UserSchema().dump(current_user)
        if ob.data['isAdmin'] == True:
            data = Order.query.filter_by(status=request.json['status']).all()
            if data:
                if len(data) > 0:
                    finalRes = []
                    for obj in data:
                        res = OrderSchema().dump(obj)
                        finalRes.append(res.data)
                    return jsonify({"result": finalRes})
            return jsonify({'error': "No Order found"})
        return jsonify({'error': 'You Have No Access'})
    except Exception as error:
        return jsonify({"error": str(error)}), 400

@app.route("/all_orders_onUser",methods=['POST'])
@token_required
def allOrdersOnUser(current_user):
    try:
        ob = UserSchema().dump(current_user)
        if ob.data['isAdmin'] == True:
            data = Order.query.filter_by(user=request.json['user']).all()
            if data:
                if len(data) > 0:
                    finalRes = []
                    for obj in data:
                        res = OrderSchema().dump(obj)
                        finalRes.append(res.data)
                    return jsonify({"result": finalRes})
            return jsonify({'error': "No Order found"})
        return jsonify({'error': 'You Have No Access'})
    except Exception as error:
        return jsonify({"error": str(error)}), 400

@app.route("/all_orders_onPaymentStatus",methods=['POST'])
@token_required
def allOrdersOnPaymentStatus(current_user):
    try:
        ob = UserSchema().dump(current_user)
        if ob.data['isAdmin'] == True:
            data = Order.query.filter_by(paymentStatus=request.json['paymentStatus']).all()
            if data:
                if len(data) > 0:
                    finalRes = []
                    for obj in data:
                        res = OrderSchema().dump(obj)
                        finalRes.append(res.data)
                    return jsonify({"result": finalRes})
            return jsonify({'error': "No Order found"})
        return jsonify({'error': 'You Have No Access'})
    except Exception as error:
        return jsonify({"error": str(error)}), 400

@app.route("/all_orders",methods=["POST"])
@token_required
def allOrders(current_user):
    try:
        ob = UserSchema().dump(current_user)
        if ob.data['isAdmin']== True:
            data = Order.query.all()
            if data:
                if len(data) > 0:
                    finalRes = []
                    for obj in data:
                        res = OrderSchema().dump(obj)
                        finalRes.append(res.data)
                    return jsonify({"result": finalRes})
            return jsonify({'error': "No Order found"})
        return jsonify({'error':'You Have No Access'})
    except Exception as error:
        return jsonify({"error": str(error)}), 400

@app.route("/order/<string:id>",methods=['GET','POST','DELETE'])
@token_required
def Order_by_id(current_user,id):
    try:
        user = UserSchema().dump(current_user)
        if request.method == 'GET':
            data = Order.query.filter_by(uniqueCode=id).first()
            if data:
                data = OrderSchema().dump(data).data
                response = jsonify({"result": data})
                return response
            return jsonify({'error': "No Order found with id ({})".format(id)}), 400
        if request.method == 'POST':
            if user.data['isAdmin']== True:
                ob = Order.query.filter_by(uniqueCode=id).first()
                if ob:
                    for key in request.json:
                        setattr(ob, key, request.json[key])
                    ob.update()
                    result = OrderSchema().dump(ob)
                    return jsonify(result.data)
                return jsonify({'error': "No Order found with id ({})".format(id)}), 400
            return jsonify({"error":"Access Denied"})
        if request.method == 'DELETE':
            ob = Order.query.filter_by(uid=id).first()
            if ob:
                ob.delete()
                return jsonify({'id': ob.uid})
            return jsonify({'error': "No Order found with id ({})".format(id)}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 400
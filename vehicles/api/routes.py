from flask import Blueprint, request, jsonify
from vehicles.helpers import token_required
from vehicles.models import db, User, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': 'value'}


# CREATE CAR ENDPOINT
@api.route('/vehicles', methods = ['POST'])
@token_required
def create_drone(current_user_token):
    make = request.json['model']
    model = request.json['model']
    price = request.json['price']
    horsepower = request.json['horsepower']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(make, model, price, horsepower,user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)




# RETRIEVE ALL DRONEs ENDPOINT
@api.route('/drones', methods = ['GET'])
@token_required
def get_drones(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


# RETRIEVE ONE Drone ENDPOINT
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_drone(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401



# UPDATE DRONE ENDPOINT
@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_drone(current_user_token,id):
    car = Car.query.get(id) # GET DRONE INSTANCE

    car.make = request.json['make']
    car.model = request.json['model']
    car.price = request.json['price']
    car.horsepower = request.json['horsepower']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)


# DELETE DRONE ENDPOINT
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_drone(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)
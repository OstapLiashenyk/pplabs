import datetime

from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError, validate
from flask_bcrypt import Bcrypt
from models import Users, Rooms, booked_room
import db

user_blueprint = Blueprint('user', __name__, url_prefix='/user')
room_blueprint = Blueprint('room', __name__, url_prefix='/room')
bcrypt = Bcrypt()


@user_blueprint.route('', methods=['POST'])
def create_user():
    try:
        class UserToCreate(Schema):
            username = fields.String(required=True)
            first_name = fields.String(required=True)
            last_name = fields.String(required=True)
            email = fields.Email(required=True)
            password = fields.String(required=True)
            phone = fields.Integer(required=True)
            user_status = fields.Integer(required=True)

        UserToCreate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    users = db.session.query(Users).filter_by(username=request.json['username']).all()
    if len(users) > 0:
        return jsonify({"message": "Username is used"}), 400
    if len(request.json['password']) < 8:
        return jsonify({"message": "Password is too short"}), 400
    user = Users(username=request.json['username'], first_name=request.json['first_name'],
                 last_name=request.json['last_name'], email=request.json['email'],
                 password=bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),
                 phone=request.json['phone'], user_status=request.json['user_status'])
    try:
        db.session.add(user)
    except:
        db.session.rollback()
        return jsonify({"message": "Error user create"}), 500
    db.session.commit()
    return get_user(user.id)


@user_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.query(Users).filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    res_json = {'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
                }

    return jsonify(res_json), 200


@user_blueprint.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        class UserToUpdate(Schema):
            username = fields.String()
            first_name = fields.String()
            last_name = fields.String()
            email = fields.Email()
            password = fields.String()
            phone = fields.Integer()

        if not request.json:
            raise ValidationError('No input data provided')
        UserToUpdate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    users = db.session.query(Users).filter_by(username=request.json['username']).all()
    if len(users) > 0 and users[0].id != user_id:
        return jsonify({"message": "Username is used"}), 400

    user = db.session.query(Users).filter(Users.id == user_id).first()

    if user is None:
        return jsonify({'error': 'No users'}), 404

    try:
        if 'username' in request.json:
            user.username = request.json['username']
        if 'first_name' in request.json:
            user.first_name = request.json['first_name']
        if 'last_name' in request.json:
            user.last_name = request.json['last_name']
        if 'email' in request.json:
            user.email = request.json['email']
        if 'password' in request.json:
            user.password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        if 'phone' in request.json:
            user.phone = request.json['phone']
    except:
        db.session.rollback()
        return jsonify({"User Data is not valid"}), 400

    db.session.commit()

    return get_user(user_id)


@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.query(Users).filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': 'No users'}), 404

    try:
        db.session.delete(user)
    except:
        db.session.rollback()
        return jsonify({"User data is not valid"}), 400

    db.session.commit()

    return "", 204


@user_blueprint.route('/login', methods=['GET'])
def login():
    return jsonify("not implemented")


@user_blueprint.route('/logout', methods=['GET'])
def logout():
    return jsonify("not implemented")


@room_blueprint.route('', methods=['POST'])
def create_room():
    try:
        class RoomToCreate(Schema):
            name = fields.String(required=True)
            num_of_seats = fields.Integer(required=True)

        RoomToCreate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    if request.json['num_of_seats'] < 0:
        return ({"message": "num_of_seats < 0"}), 400
    room = Rooms(name=request.json['name'], num_of_seats=request.json['num_of_seats'])

    try:
        db.session.add(room)
    except:
        db.session.rollback()
        return jsonify({"message": "Error room create"}), 500
    db.session.commit()
    return get_room(room.id)


@room_blueprint.route('/<int:room_id>', methods=['GET'])
def get_room(room_id):
    room = db.session.query(Rooms).filter_by(id=room_id).first()
    if room is None:
        return jsonify({'error': 'No rooms'}), 404

    res_json = {'id': room.id,
                'name': room.name,
                'num_of_seats': room.num_of_seats
                }

    return jsonify(res_json), 200


@room_blueprint.route('/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    room = db.session.query(Rooms).filter_by(id=room_id).first()
    if room is None:
        return jsonify({'error': 'No rooms'}), 404
    try:
        db.session.delete(room)
    except:
        db.session.rollback()
        return jsonify({"Room data is not valid"}), 400

    db.session.commit()

    return "", 204


@room_blueprint.route('/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    try:
        class RoomToUpdate(Schema):
            name = fields.String()
            num_of_seats = fields.Integer()

        if not request.json:
            raise ValidationError('No input data provided')
        RoomToUpdate().load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    if request.json['num_of_seats'] < 0:
        return ({"message": "num_of_seats < 0"}), 400
    room = db.session.query(Rooms).filter(Rooms.id == room_id).first()

    if room is None:
        return jsonify({'error': 'No rooms'}), 404

    try:
        if 'name' in request.json:
            room.name = request.json['name']
        if 'num_of_seats' in request.json:
            room.num_of_seats = request.json['num_of_seats']
    except:
        db.session.rollback()
        return jsonify({"Room Data is not valid"}), 400

    db.session.commit()

    return get_room(room_id)


@user_blueprint.route('/book', methods=['POST'])
def create_book():
    try:
        class RoomToBook(Schema):
            room_id = fields.Integer(required=True)
            user_id = fields.Integer(required=True)
            num_of_people = fields.Integer(required=True)
            time_start = fields.DateTime(required=True)
            time_end = fields.DateTime(required=True)

        RoomToBook().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    seats = db.session.query(Rooms).filter_by(id=request.json['room_id']).first()
    if seats is None:
        return ({"message": "No rooms"}), 404
    if request.json['num_of_people'] < 0 or request.json['num_of_people'] > seats.num_of_seats:
        return ({"message": "Room is small for that count of people"}), 400
    books = db.session.query(booked_room).filter_by(room_id=request.json['room_id']).all()

    for check in books:
        if check.time_start <= datetime.datetime.strptime(request.json['time_start'],
                                                          '%Y-%m-%d %H:%M:%S') < check.time_end:
            return ({"message": "Time is booked"}), 400
        if check.time_start < datetime.datetime.strptime(request.json['time_end'],
                                                         '%Y-%m-%d %H:%M:%S') <= check.time_end:
            return ({"message": "Time is booked"}), 400

    if datetime.datetime.strptime(request.json['time_end'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(
            request.json['time_start'], '%Y-%m-%d %H:%M:%S') > datetime.timedelta(days=5) or datetime.datetime.strptime(
        request.json['time_end'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(request.json['time_start'],
                                                                                    '%Y-%m-%d %H:%M:%S') < datetime.timedelta(
        hours=1):
        return ({"message": "Time is too short or too big"}), 400

    book = booked_room(room_id=request.json['room_id'], user_id=request.json['user_id'],
                       num_of_people=request.json['num_of_people'], time_start=request.json['time_start'],
                       time_end=request.json['time_end'])
    try:
        db.session.add(book)
    except:
        db.session.rollback()
        return jsonify({"message": "Error book create"}), 500
    db.session.commit()
    return get_book(book.id)


@user_blueprint.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = db.session.query(booked_room).filter_by(id=book_id).first()
    if book is None:
        return jsonify({'error': 'Book not found'}), 404

    res_json = {'id': book.id,
                'room_id': book.room_id,
                'user_id': book.user_id,
                'num_of_people': book.num_of_people,
                'time_start': book.time_start,
                'time_end': book.time_end
                }

    return jsonify(res_json), 200


@user_blueprint.route('/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = db.session.query(booked_room).filter_by(id=book_id).first()
    if book is None:
        return jsonify({'error': 'No books'}), 404

    try:
        db.session.delete(book)
    except:
        db.session.rollback()
        return jsonify({"Book data is not valid"}), 400

    db.session.commit()

    return "", 204


@user_blueprint.route('/book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        class RoomToBook(Schema):
            room_id = fields.Integer()
            user_id = fields.Integer()
            num_of_people = fields.Integer()
            time_start = fields.DateTime()
            time_end = fields.DateTime()

        if not request.json:
            raise ValidationError('No input data provided')
        RoomToBook().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    book = db.session.query(booked_room).filter(booked_room.id == book_id).first()

    if book is None:
        return jsonify({'error': 'No books'}), 404

    try:
        if 'room_id' in request.json:
            book.room_id = request.json['room_id']
        if 'user_id' in request.json:
            book.user_id = request.json['user_id']
        if 'num_of_people' in request.json:
            seats = db.session.query(Rooms).filter_by(id=request.json['room_id']).first()
            if seats is None:
                return ({"message": "No rooms"}), 404
            if request.json['num_of_people'] < 0 or request.json['num_of_people'] > seats.num_of_seats:
                return ({"message": "Room is small for that count of people"}), 400
            book.num_of_people = request.json['num_of_people']
        if 'time_start' in request.json:
            books = db.session.query(booked_room).filter_by(room_id=request.json['room_id']).all()

            for check in books:
                if check.id != book_id:
                    if check.time_start <= datetime.datetime.strptime(request.json['time_start'], '%Y-%m-%d %H:%M:%S') < check.time_end:
                        return ({"message": "Time is booked"}), 400
            if not 'time_end' in request.json:
                if book.time_end - datetime.datetime.strptime(
                        request.json['time_start'], '%Y-%m-%d %H:%M:%S') > datetime.timedelta( days=5) or book.time_end - datetime.datetime.strptime(request.json['time_start'], '%Y-%m-%d %H:%M:%S') < datetime.timedelta(hours=1):
                    return ({"message": "Time is too short or too big"}), 400
            else:
                if datetime.datetime.strptime(request.json['time_end'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(request.json['time_start'], '%Y-%m-%d %H:%M:%S') > datetime.timedelta(
                    days=5) or datetime.datetime.strptime(request.json['time_end'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(request.json['time_start'],'%Y-%m-%d %H:%M:%S') < datetime.timedelta(hours=1):
                    return ({"message": "Time is too short or too big"}), 400
            book.time_start = request.json['time_start']
        if 'time_end' in request.json:
            books = db.session.query(booked_room).filter_by(room_id=request.json['room_id']).all()

            for check in books:
                if check.id != book_id:
                    if datetime.datetime.strptime(check.time_start, '%Y-%m-%d %H:%M:%S') < datetime.datetime.strptime(request.json['time_end'], '%Y-%m-%d %H:%M:%S') <= check.time_end:
                        return ({"message": "Time is booked"}), 400
            if 'time_start' in request.json:
                if datetime.datetime.strptime(request.json['time_end'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(book.time_start, '%Y-%m-%d %H:%M:%S') > datetime.timedelta(days=5) or datetime.datetime.strptime(request.json['time_end'],'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(book.time_start, '%Y-%m-%d %H:%M:%S') < datetime.timedelta(hours=1):
                    return ({"message": "Time is too short or too big"}), 400
            book.time_end = request.json['time_end']
    except:
        db.session.rollback()
        return jsonify({"Book Data is not valid"}), 400

    db.session.commit()

    return get_book(book_id)

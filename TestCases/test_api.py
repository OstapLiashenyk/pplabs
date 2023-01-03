import base64

from main import app
import pytest
from models import Session, engine, BaseModel, Users, Rooms, booked_room


class TestHello:
    @pytest.fixture()
    def hello_world(self):
        response = app.test_client().get('/hello-world')
        return response.status_code

    def test_hello_world(self, hello_world):
        assert hello_world == 200


class TestHelloStudent:
    @pytest.fixture()
    def hello_student(self):
        response = app.test_client().get('/hello-world-7')
        return response.status_code

    def test_hello_world(self, hello_student):
        assert hello_student == 200


class TestCreateUser:
    @pytest.fixture()
    def norm1(self):
        user = {
            "username": "user1",
            "first_name": "John",
            "last_name": "James",
            "email": "john@email.com",
            "password": "12345678",
            "phone": "12345",
            "user_status": 1
        }
        return user

    @pytest.fixture()
    def norm2(self):
        user = {
            "username": "user2",
            "first_name": "John",
            "last_name": "James",
            "email": "john@email.com",
            "password": "12345678",
            "phone": "12345",
            "user_status": 3
        }
        return user

    @pytest.fixture()
    def without(self):
        user = {
            "username": "user1",
            "first_name": "John",
            "last_name": "James",
            "email": "johnemail.com",
            "password": "12345678",
            "phone": "12345",
            "user_status": 1
        }
        return user

    @pytest.fixture()
    def short(self):
        user = {
            "username": "user1",
            "first_name": "John",
            "last_name": "James",
            "email": "johne@mail.com",
            "password": "123456",
            "phone": "12345",
            "user_status": 1
        }
        return user

    @staticmethod
    def create_tables():
        BaseModel.metadata.drop_all(engine)
        BaseModel.metadata.create_all(engine)

    def test_create_user(self, norm1):
        self.create_tables()
        response = app.test_client().post('/user', json=norm1)
        assert response.status_code == 200

    def test_create_user2(self, norm2):
        response = app.test_client().post('/user', json=norm2)
        assert response.status_code == 200

    def test_fail_create(self, norm1):
        response = app.test_client().post('/user', json=norm1)
        assert response.status_code == 400

    def test_fail_val(self, without):
        response = app.test_client().post('/user', json=without)
        assert response.status_code == 400

    def test_short_pass(self, short):
        response = app.test_client().post('/user', json=short)
        assert response.status_code == 400

    def test_get_none_user(self):
        response = app.test_client().get('/user/100')
        assert response.status_code == 404


class TestLoginUser:
    def test_login_user(self):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().get('/user/login', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 200

    def test_fail_login_user(self):
        valid_credentials = base64.b64encode(b"user1:4645451").decode("utf-8")
        response = app.test_client().get('/user/login', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 401


class TestLogoutUser:
    def test_logout_user(self):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().get('/user/logout', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 200

    def test_fail_logout_user(self):
        valid_credentials = base64.b64encode(b"user1:4645451").decode("utf-8")
        response = app.test_client().get('/user/logout', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 401


class TestUpdateUser:
    @pytest.fixture()
    def norm1(self):
        user = {
            "username": "user1",
            "first_name": "Ostap",
            "last_name": "Ostap",
            "email": "pstap@email.com",
            "password": "12345678",
            "phone": "1111111"
        }
        return user

    @pytest.fixture()
    def without(self):
        user = {
            "username": "user1",
            "first_name": "John",
            "last_name": "James",
            "email": "johnemail.com",
            "password": "12345678",
            "phone": "12345"
        }
        return user

    @pytest.fixture()
    def fail(self):
        user = {
            "username": "user1",
            "first_name": "John",
            "last_name": "James",
            "email": "johne@mail.com",
            "password": "12345678",
            "phone": "12345",
            "user_status": 1
        }
        return user

    def test_update_none_user(self):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().put('/user/111', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 404

    def test_update_not_user(self):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().put('/user/2', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 403

    def test_update_user(self, norm1):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().put('/user/1', headers={'Authorization': 'Basic ' + valid_credentials}, json=norm1)
        assert response.status_code == 200

    def test_fail_user(self, without):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().put('/user/1', headers={'Authorization': 'Basic ' + valid_credentials},
                                         json=without)
        assert response.status_code == 400

    def test_none_json(self):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().put('/user/1', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 400

    def test_none_json_2(self, fail):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().put('/user/1', headers={'Authorization': 'Basic ' + valid_credentials}, json=fail)
        assert response.status_code == 400


class TestCreateRoom:
    @pytest.fixture()
    def norm1(self):
        room = {
            "name": "room1",
            "num_of_seats": 10
        }
        return room

    @pytest.fixture()
    def fail(self):
        room = {
            "name": "room2",
            "num_of_seats": -1
        }
        return room

    @pytest.fixture()
    def val(self):
        room = {
            "name": "room2",
            "num_of_seats": "a"
        }
        return room

    def test_create_room(self, norm1):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().post('/room', headers={'Authorization': 'Basic ' + valid_credentials}, json=norm1)
        assert response.status_code == 200

    def test_fail_create_room(self, fail):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().post('/room', headers={'Authorization': 'Basic ' + valid_credentials}, json=fail)
        assert response.status_code == 400

    def test_without(self, fail):
        valid_credentials = base64.b64encode(b"user2:12345678").decode("utf-8")
        response = app.test_client().post('/room', headers={'Authorization': 'Basic ' + valid_credentials}, json=fail)
        assert response.status_code == 403

    def test_val(self, val):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().post('/room', headers={'Authorization': 'Basic ' + valid_credentials}, json=val)
        assert response.status_code == 400

    def test_get_no_room(self):
        response = app.test_client().get('/room/111')
        assert response.status_code == 404


class TestUpdateRoom:
    @pytest.fixture()
    def norm1(self):
        room = {
            "name": "room1",
            "num_of_seats": 12
        }
        return room

    @pytest.fixture()
    def fail(self):
        room = {
            "name": "room2",
            "num_of_seats": -1
        }
        return room

    @pytest.fixture()
    def val(self):
        room = {
            "name": "room2",
            "num_of_seats": "a"
        }
        return room

    def test_update_room(self, norm1):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().put('/room/1', headers={'Authorization': 'Basic ' + valid_credentials}, json=norm1)
        assert response.status_code == 200

    def test_for_up(self, norm1):
        valid_credentials = base64.b64encode(b"user2:12345678").decode("utf-8")
        response = app.test_client().put('/room/1', headers={'Authorization': 'Basic ' + valid_credentials}, json=norm1)
        assert response.status_code == 403

    def test_val(self, val):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().put('/room/1', headers={'Authorization': 'Basic ' + valid_credentials}, json=val)
        assert response.status_code == 400

    def test_fail_create_room(self, fail):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().put('/room/1', headers={'Authorization': 'Basic ' + valid_credentials}, json=fail)
        assert response.status_code == 400

    def test_without(self, fail):
        valid_credentials = base64.b64encode(b"user2:12345678").decode("utf-8")
        response = app.test_client().put('/room/1', headers={'Authorization': 'Basic ' + valid_credentials}, json=fail)
        assert response.status_code == 403

    def test_no_room(self, norm1):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().put('/room/21', headers={'Authorization': 'Basic ' + valid_credentials}, json=norm1)
        assert response.status_code == 404


class TestBook:
    @pytest.fixture()
    def norm(self):
        book = {
            "room_id": 1,
            "user_id": 1,
            "num_of_people": 10,
            "time_start": "2022-10-15 12:10:00",
            "time_end": "2022-10-15 13:30:00"
        }
        return book

    @pytest.fixture()
    def norm2(self):
        book = {
            "room_id": 1,
            "user_id": 1,
            "num_of_people": 10,
            "time_start": "2022-08-15 12:10:00",
            "time_end": "2022-08-15 13:30:00"
        }
        return book

    @pytest.fixture()
    def norm_time(self):
        book = {
            "room_id": 1,
            "user_id": 1,
            "num_of_people": 10,
            "time_start": "2022-10-15 12:10:00",
            "time_end": "2022-10-15 13:30:00"
        }
        return book

    @pytest.fixture()
    def val(self):
        book = {
            "room_id": "a",
            "user_id": 1,
            "num_of_people": 10,
            "time_start": "2022-12-15 12:10:00",
            "time_end": "2022-12-15 13:30:00"
        }
        return book

    @pytest.fixture()
    def no_rooms(self):
        book = {
            "room_id": 100,
            "user_id": 1,
            "num_of_people": 10,
            "time_start": "2022-10-15 12:10:00",
            "time_end": "2022-10-15 13:30:00"
        }
        return book

    @pytest.fixture()
    def seats(self):
        book = {
            "room_id": 1,
            "user_id": 1,
            "num_of_people": -1,
            "time_start": "2022-11-15 12:10:00",
            "time_end": "2022-11-15 13:30:00"
        }
        return book

    @pytest.fixture()
    def time(self):
        book = {
            "room_id": 1,
            "user_id": 1,
            "num_of_people": 10,
            "time_start": "2022-11-15 12:10:00",
            "time_end": "2022-12-15 13:30:00"
        }
        return book

    def test_book(self, norm):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().post('/user/book', headers={'Authorization': 'Basic ' + valid_credentials}, json=norm)
        assert response.status_code == 200

    def test_book_time(self, norm_time):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().post('/user/book', headers={'Authorization': 'Basic ' + valid_credentials}, json=norm_time)
        assert response.status_code == 400

    def test_val(self, val):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().post('/user/book', headers={'Authorization': 'Basic ' + valid_credentials}, json=val)
        assert response.status_code == 400

    def test_no_rooms(self, no_rooms):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().post('/user/book', headers={'Authorization': 'Basic ' + valid_credentials}, json=no_rooms)
        assert response.status_code == 404

    def test_seats(self, seats):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().post('/user/book', headers={'Authorization': 'Basic ' + valid_credentials}, json=seats)
        assert response.status_code == 400

    def test_time(self, time):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().post('/user/book', headers={'Authorization': 'Basic ' + valid_credentials}, json=time)
        assert response.status_code == 400

    def test_other_user(self, norm2):
        valid_credentials = base64.b64encode(b"user2:12345678").decode("utf-8")
        response = app.test_client().post('/user/book', headers={'Authorization': 'Basic ' + valid_credentials}, json=norm2)
        assert response.status_code == 200

    def test_get_no(self):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().get('/user/book/100', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 404

    def test_forbidden(self):
        valid_credentials = base64.b64encode(b"user2:12345678").decode("utf-8")
        response = app.test_client().get('/user/book/1', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 403


class TestUpdateBook:
    @pytest.fixture()
    def norm(self):
        book = {
            "room_id": 1,
            "user_id": 1,
            "num_of_people": 11,
            "time_start": "2022-10-11 12:10:00",
            "time_end": "2022-10-11 13:30:00"
        }
        return book

    @pytest.fixture()
    def seats(self):
        book = {
            "room_id": 1,
            "user_id": 1,
            "num_of_people": -1,
            "time_start": "2022-11-15 12:10:00",
            "time_end": "2022-11-15 13:30:00"
        }
        return book

    def test_update_book(self, norm):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().put('/user/book/1', headers={'Authorization': 'Basic ' + valid_credentials}, json=norm)
        assert response.status_code == 200

    def test_update_seats(self, seats):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().put('/user/book/1', headers={'Authorization': 'Basic ' + valid_credentials}, json=seats)
        assert response.status_code == 400


class TestDeleteRoom:
    @pytest.fixture()
    def norm(self):
        user = {
            "username": "userroom",
            "first_name": "John",
            "last_name": "James",
            "email": "john@email.com",
            "password": "12345678",
            "phone": "12345",
            "user_status": 1
        }
        return user

    def test_room_delete(self, norm):
        app.test_client().post('/user', json=norm)
        valid_credentials = base64.b64encode(b"userroom:12345678").decode("utf-8")
        response = app.test_client().delete('/room/1', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 204


class TestDeleteUser:
    def test_user_delete(self):
        valid_credentials = base64.b64encode(b"userroom:12345678").decode("utf-8")
        response = app.test_client().delete('/user/3', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 204


class TestDeleteBook:
    def test_book_delete(self):
        valid_credentials = base64.b64encode(b"user1:12345678").decode("utf-8")
        response = app.test_client().delete('/user/book/1', headers={'Authorization': 'Basic ' + valid_credentials})
        assert response.status_code == 204


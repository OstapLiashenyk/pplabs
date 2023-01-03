from models import *

session = Session()

user1 = Users(first_name="Igor", last_name="Leleka", phone='059484855', email="igorlel@gmail.com", username="igorlel", password="20061995il", user_status=0)
user2 = Users(first_name="Kolya", last_name="Dzibiuk",phone='059484855',  email="koldzib@gmail.com", username="koldzib", password="30112002kd", user_status=1)
user3 = Users(first_name="Denys", last_name="Malaniuk",phone='059484855',  email="denmal@gmail.com", username="denmalan", password="12091999dm", user_status=1)

room1 = Rooms(name="room #1", num_of_seats=10)
room2 = Rooms(name="room #2", num_of_seats=20)
room3 = Rooms(name="room #3", num_of_seats=14)

book1 = booked_room(roomToBook=room1, userToBook=user1, num_of_people=4, time_start='2022-10-10 13:10:00', time_end='2022-10-10 14:10:00')
book2 = booked_room(roomToBook=room2, userToBook=user2, num_of_people=12, time_start='2022-12-10 14:10:00', time_end='2022-12-10 16:10:00')
book3 = booked_room(roomToBook=room3, userToBook=user3, num_of_people=14, time_start='2022-10-13 17:10:00', time_end='2022-10-13 21:10:00')

session.add(user1)
session.add(user2)
session.add(user3)

session.add(room1)
session.add(room2)
session.add(room3)

session.add(book1)
session.add(book2)
session.add(book3)

session.commit()

print(session.query(Users).all()[0].first_name, session.query(Users).all()[0].last_name)
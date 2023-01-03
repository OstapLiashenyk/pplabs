CREATE TABLE users(
   id SERIAL NOT NULL PRIMARY KEY,
   username VARCHAR (50) NOT NULL,
   first_name VARCHAR (50) NOT NULL,
   last_name VARCHAR (20) NOT NULL,
   email VARCHAR(100) NOT NULL,
   password VARCHAR (255) NOT NULL,
   phone VARCHAR(100) NOT NULL,
   user_status INT NOT NULL
);

CREATE TABLE rooms(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    num_of_seats INT NOT NULL
);

CREATE TABLE booked_room(
    id SERIAL PRIMARY KEY ,
    room_id  int NOT NULL,
    CONSTRAINT fk_roomId FOREIGN KEY (room_id) REFERENCES rooms (id),
    user_id  int NOT NULL,
    CONSTRAINT fk_userId FOREIGN KEY (user_id) REFERENCES users (id),
    num_of_people INT NOT NULL,
    time_start TIMESTAMP NOT NULL ,
    time_end TIMESTAMP NOT NULL
);
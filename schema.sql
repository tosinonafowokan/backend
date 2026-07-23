CREATE database senior_facility;
USE senior_facility;

CREATE TABLE floor (
floor_id int auto_increment PRIMARY KEY,
floor_level int not null,
floor_name varchar (100) not null
);

CREATE TABLE room (floor
room_id int auto_increment PRIMARY KEY,
room_capacity int not null,
room_number int not null,
room_floor int not null,
FOREIGN KEY (room_floor) references floor(floor_id) on delete cascade
);

CREATE TABLE resident (
res_id int auto_increment PRIMARY KEY,
res_first_name varchar(100) not null,
res_last_name varchar(100) not null,
res_age int not null,
res_room int not null,
FOREIGN KEY (res_room) references room(room_id) on delete cascade
);
   

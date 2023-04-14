#creating the property table
property_table='''create table if not exists property(
property_id varchar(8) not null primary key,
type varchar(20) not null,
description varchar(250) not null,
availability varchar(10) not null,
price float not null
);'''

property_address='''create table if not exists property_address(
property_id varchar(8) not null,
city varchar(30) not null,
state varchar(20) not null,
location varchar(50) not null,
primary key(property_id,city,state,location),
foreign key(property_id) references property
);'''

#creating the user table
users='''create table if not exists users(
user_id varchar(8) not null primary key,
first_name varchar(30) not null,
middle_name varchar(30) not null,
last_name varchar(30) not null,
user_type varchar(20) not null,
address varchar(50) not null,
email_id varchar(40) not null
);'''

#creating the renter table
renter='''create table if not exists renter(
renters_id varchar(8) not null primary key,
user_id varchar(8) not null,
move_in_date DATE,
preferedlocation varchar(20),
budget float,
foreign key(user_id) references users
);'''

#creditcard
credit_card='''create table if not exists credit_card(
creditcard_id varchar(8) primary key,
card_number varchar(30),
renter_id varchar(8),
address varchar(50),
card_expiry_date varchar(8)
);'''

#property_booking
property_booking='''create table if not exists property_booking(
booking_id varchar(8) not null,
property_id varchar(8) not null,
renters_id varchar(8) not null,
booking_date date not null,
creditcard_id varchar(8) not null,
primary key(booking_id,property_id,renters_id),
foreign key(property_id) references property,
foreign key(renters_id) references renter,
foreign key(creditcard_id) references credit_card);'''

#agents
agents='''create table if not exists agents(
agents_id varchar(8) not null primary key,
user_id varchar(8) not null,
realestate_agency varchar(20) not null,
contact varchar(15) not null,
job_title varchar(20) not null,
booking_id varchar(8) not null,
property_id varchar(8) not null,
renters_id varchar(8) not null,
foreign key(booking_id,renters_id,property_id) references property_booking(booking_id,renters_id,property_id) on delete cascade
);'''

#house
house='''create table if not exists house(
house_id varchar(8) not null primary key,
property_id varchar(8) not null,
rooms int not null,
sqt_area float not null,
foreign key (property_id) references property(property_id)
);'''


#apartment
apartment='''create table if not exists apartment(
apts_id varchar(8) not null primary key,
property_id varchar(8) not null,
rooms int not null,
sqt_area float not null,
foreign key (property_id) references property(property_id)
);'''

#commercial_building
commercial_building='''create table if not exists commercial_building(
building_id varchar(8) not null primary key,
property_id varchar(8) not null,
business_type varchar(20) not null,
sqf_area float not null,
foreign key (property_id) references property(property_id)
);'''

#property_credit
property_credit='''create table if not exists property_credit(
booking_id varchar(8) not null,
property_id varchar(8) not null,
renters_id varchar(8) not null,
creditcard_id varchar(8) not null,
primary key(booking_id,property_id,renters_id),
foreign key(booking_id,property_id,renters_id) references property_booking(booking_id,property_id,renters_id)
);'''



#user_renter
user_renter='''create table if not exists user_renter(
renters_id varchar(8) not null,
user_id varchar(8) not null,
primary key(renters_id,user_id),
foreign key(renters_id) references renter(renters_id),
foreign key(user_id) references users(user_id)
);'''

#user_agent
user_agent='''create table if not exists user_agent(
agents_id varchar(8) not null,
user_id varchar(8) not null,
primary key(agents_id,user_id),
foreign key(agents_id) references agents(agents_id),
foreign key(user_id) references users(user_id)
);'''

#searches
searches='''create table searches(
renters_id varchar(8) not null,
property_id varchar(8) not null,
primary key(renters_id, property_id),
foreign key(property_id) references property,
foreign key(renters_id) references renter
);'''

property_house='''create table property_house(
house_id varchar(8) not null,
property_id varchar(8) not null,
primary key(house_id, property_id),
foreign key(property_id) references property,
foreign key(house_id) references house
);'''

property_apts='''create table property_apts(
apts_id varchar(8) not null,
property_id varchar(8) not null,
primary key(apts_id, property_id),
foreign key(property_id) references property,
foreign key(apts_id) references apartment
);'''

property_build='''create table property_build(
building_id varchar(8) not null,
property_id varchar(8) not null,
primary key(building_id, property_id),
foreign key(property_id) references property,
foreign key(building_id) references commercial_building );'''

connection=psycopg2.connect(database='real_estate_db',user='tirumaleshn2000',password='',host='localhost',port='5431')
cursor=connection.cursor()
for table in [property_table,property_address,users,renter,credit_card,
              property_booking,agents,house,apartment,commercial_building,property_credit,
             user_renter,user_agent,searches,property_house,property_apts,property_build]:
    print('----------')
    print(table)
    cursor.execute(table)
connection.commit()
connection.close()

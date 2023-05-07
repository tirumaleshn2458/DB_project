--Relational Schema of Real Estate Management System

create table property(
property_id varchar(8) not null,
type varchar(20),
description varchar(200),
availability varchar(20),
price numeric(10, 2),
primary key(property_id)
);

create table property_address(
property_id varchar(8) not null,
city varchar(30) not null,
state varchar(20) not null,
location decimal(9, 6) not null,
primary key(property_id, city, state, location),
foreign key(property_id) references property,
);

create table users(
user_id varchar(8) not null,
first_name varchar(10),
middle_name varchar(10),
last_name varchar(10),
user_type varchar(10) not null,
address varchar(30),
email_id varchar(50) not null,
primary key(user_id)
);

create table renter(
renters_id varchar(8) not null,
user_id varchar(8) not null,
move_in_date DATE,
prefered_location decimal(9, 6),
budget numeric(10, 2),
primary key(renters_id),
foreign key(user_id) references users
);

create table credit_card(
credit_card_id varchar(8) not null,
card_number integer(10) not null,
renters_id varchar(8) not null,
address varchar(30) not null,
card_expiry_date DATE not null,
primary key(credit_card_id),
foreign key(renters_id) references renter
);

create table property_booking(
booking_id varchar(8) not null,
property_id varchar(8) not null,
renters_id varchar(8) not null,
booking_date DATE not null,
credit_card_id varchar(8),
primary key(booking_id, property_id, renters_id),
foreign key(property_id) references property,
foreign key(renters_id) references renter,
foreign key(credit_card_id) references credit_card
);


create table agents(
agents_id varchar(8) not null,
user_id varchar(8) not null,
real_estate_agency varchar(50),
contact integer(10),
job_title varchar(30),
booking_id varchar(8) not null,
property_id varchar(8) not null,
renters_id varchar(8) not null,
primary key(agents_id),
foreign key(user_id) references users,
foreign key(booking_id) references property_booking,
foreign key(property_id) references property,
foreign key(renters_id) references renter
);

create table house(
house_id varchar(8) not null,
property_id varchar(8) not null,
rooms integer(5),
sqfoot_area numeric(6, 2),
primary key(house_id),
foreign key(property_id) references property,
);

create table apartment(
apts_id varchar(8) not null,
property_id varchar(8) not null,
rooms integer(5),
sqfoot_area numeric(6, 2),
primary key(apts_id),
foreign key(property_id) references property,
);

create table commercial_building(
building_id varchar(8) not null,
property_id varchar(8) not null,
business_type varchar(30),
sqfoot_area numeric(6, 2),
primary key(building_id),
foreign key(property_id) references property,
);


create table property_credit(
booking_id varchar(8) not null,
property_id varchar(8) not null,
credit_card_id varchar(8) not null,
primary key(booking_id, property_id),
foreign key(booking_id) references property_booking,
foreign key(property_id) references property,
foreign key(credit_card_id) references credit_card
);

create table user_renter(
renters_id varchar(8) not null,
user_id varchar(8) not null,
primary key(renters_id, user_id),
foreign key(renters_id) references renter,
foreign key(user_id) references users
);

create table user_agent(
agents_id varchar(8) not null,
user_id varchar(8) not null,
primary key(agents_id, user_id),
foreign key(agents_id) references agents,
foreign key(user_id) references users
);

create table searches(
renters_id varchar(8) not null,
property_id varchar(8) not null,
primary key(renters_id, property_id),
foreign key(property_id) references property,
foreign key(renters_id) references renter
);

create table property_house(
house_id varchar(8) not null,
property_id varchar(8) not null,
primary key(house_id, property_id),
foreign key(property_id) references property,
foreign key(house_id) references house
);

create table property_apts(
apts_id varchar(8) not null,
property_id varchar(8) not null,
primary key(apts_id, property_id),
foreign key(property_id) references property,
foreign key(apts_id) references apartment
);

create table property_build(
building_id varchar(8) not null,
property_id varchar(8) not null,
primary key(building_id, property_id),
foreign key(property_id) references property,
foreign key(building_id) references commercial_building
);

INSERT INTO users ( user_id, first_name, middle_name, last_name, user_type, address, email_id ) VALUES ('00000111', 'Kailash', 'Chandra', 'Shenoy', 'renter', '2951 South King Drive Chicago Illinois-60616', 'kcshenoy2000@gmail.com');
INSERT INTO users ( user_id, first_name, middle_name, last_name, user_type, address, email_id ) VALUES ('00000123', 'Rob', 'Bob', 'White', 'agent', '3001 South King Drive Chicago Illinois-60616', 'robbob@gmail.com');

INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000000', 'house', 'This charming two-story house features a bright and open floor plan with three bedrooms and two and a half bathrooms. The main level boasts a spacious living room with a cozy fireplace, a modern kitchen with stainless steel appliances, and a dining area that leads to a private backyard with a deck for outdoor entertaining.', 'available', 1000000.28 );
INSERT INTO house ( house_id, property_id, rooms, sqfoot_area ) VALUES ( '11122233', '10000000', 5, 5500.99 );


INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000001', 'house', 'This charming two-story house features a bright and open floor plan with three bedrooms and two and a half bathrooms. The main level boasts a spacious living room with a cozy fireplace, a modern kitchen with stainless steel appliances, and a dining area that leads to a private backyard with a deck for outdoor entertaining.', 'available', 2300789.56 );
INSERT INTO house ( house_id, property_id, rooms, sqfoot_area ) VALUES ( '11122234', '10000001', 3, 3500.89 );

INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000002', 'apartment', 'This modern one-bedroom apartment is located in a high-rise building with stunning views of the city. The unit features an open-concept living and dining area with large windows that flood the space with natural light.', 'available', 2345678.90 );
INSERT INTO apartment ( apts_id, property_id, rooms, sqfoot_area ) VALUES ( '10000021','10000002', 3, 3576.89 );

INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000003', 'commercial_building', 'This impressive commercial building is a three-story office complex located in the heart of downtown. The building offers a total of 50,000 square feet of leasable space and features modern architectural design, with a glass and steel facade that provides ample natural light to the interior.', 'available', 56728900.54 );
INSERT INTO commercial_building ( building_id, property_id, business_type, sqfoot_area ) VALUES ( '12356701', '10000003', 'Grocery-Store', 110000.56 );

INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000004', 'house', 'This charming two-story house features a bright and open floor plan with three bedrooms and two and a half bathrooms. The main level boasts a spacious living room with a cozy fireplace, a modern kitchen with stainless steel appliances, and a dining area that leads to a private backyard with a deck for outdoor entertaining.', 'available', 4567890.67 );
INSERT INTO house ( house_id, property_id, rooms, sqfoot_area ) VALUES ( '11122235', '10000004', 4, 4500.70 );

INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000005', 'apartment', 'This modern one-bedroom apartment is located in a high-rise building with stunning views of the city. The unit features an open-concept living and dining area with large windows that flood the space with natural light.', 'not-available', 1542678.90 );
INSERT INTO apartment ( apts_id, property_id, rooms, sqfoot_area ) VALUES ( '10000022', '10000005', 4, 5576.89 );

INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000006', 'commercial_building', 'This impressive commercial building is a three-story office complex located in the heart of downtown. The building offers a total of 50,000 square feet of leasable space and features modern architectural design, with a glass and steel facade that provides ample natural light to the interior.', 'not-available', 99998888.54 );
INSERT INTO commercial_building ( building_id, property_id, business_type, sqfoot_area ) VALUES ( '12356701', '10000006', 'Car-Dealers', 123456.46 );

INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000007', 'house', 'This charming two-story house features a bright and open floor plan with three bedrooms and two and a half bathrooms. The main level boasts a spacious living room with a cozy fireplace, a modern kitchen with stainless steel appliances, and a dining area that leads to a private backyard with a deck for outdoor entertaining.', 'not-available', 1342567.56 );
INSERT INTO house ( house_id, property_id, rooms, sqfoot_area ) VALUES ( '11122236', '10000007', 5, 8500.67 );

INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000008', 'apartment', 'This modern one-bedroom apartment is located in a high-rise building with stunning views of the city. The unit features an open-concept living and dining area with large windows that flood the space with natural light.', 'available', 1567835.90 );
INSERT INTO apartment ( apts_id, property_id, rooms, sqfoot_area ) VALUES ( '10000023', '10000008', 2, 2576.89 );

INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000009', 'apartment', 'This modern one-bedroom apartment is located in a high-rise building with stunning views of the city. The unit features an open-concept living and dining area with large windows that flood the space with natural light.', 'available', 7653427.90 );
INSERT INTO apartment ( apts_id, property_id, rooms, sqfoot_area ) VALUES ( '10000024', '10000009', 3, 4575.79 );

INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000010', 'apartment', 'This modern one-bedroom apartment is located in a high-rise building with stunning views of the city. The unit features an open-concept living and dining area with large windows that flood the space with natural light.', 'available', 2345637.90 );
INSERT INTO apartment ( apts_id, property_id, rooms, sqfoot_area ) VALUES ( '10000025', '10000010', 5, 8576.59 );

INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000011', 'apartment', 'This modern one-bedroom apartment is located in a high-rise building with stunning views of the city. The unit features an open-concept living and dining area with large windows that flood the space with natural light.', 'available', 3452678.89 )
INSERT INTO apartment ( apts_id, property_id, rooms, sqfoot_area ) VALUES ( '10000025', '10000011', 3, 4556.69 );

INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000012', 'house', 'This charming two-story house features a bright and open floor plan with three bedrooms and two and a half bathrooms. The main level boasts a spacious living room with a cozy fireplace, a modern kitchen with stainless steel appliances, and a dining area that leads to a private backyard with a deck for outdoor entertaining.', 'not-available', 1234562.28 );
INSERT INTO house ( house_id, property_id, rooms, sqfoot_area ) VALUES ( '11122237', '10000012', 8, 11000.25 );

INSERT INTO property ( property_id, type, description, availability, price ) VALUES ( '10000013', 'house', 'This charming two-story house features a bright and open floor plan with three bedrooms and two and a half bathrooms. The main level boasts a spacious living room with a cozy fireplace, a modern kitchen with stainless steel appliances, and a dining area that leads to a private backyard with a deck for outdoor entertaining.', 'available', 1244376.56 );
INSERT INTO house ( house_id, property_id, rooms, sqfoot_area ) VALUES ( '11122238', '10000013', 6, 8500.26 );

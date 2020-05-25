CREATE DATABASE dogdata;
GRANT ALL PRIVILEGES ON DATABASE dogdata TO dogdata;
CREATE TABLE dogs (
    id serial PRIMARY KEY,
    humane_id int NOT NULL,
    name varchar(25) NOT NULL,
    age int,
    breed_primary varchar,
    breed_secondary varchar,
    gender varchar(6),
    status varchar(10),
    in_time timestamp NOT NULL,
    out_time timestamp
);

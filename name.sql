CREATE TABLE chair
(chair_id integer PRIMARY KEY, chair_name varchar NOT NULL, dean varchar NOT NULL);

CREATE TABLE student_group 
(numb_id SERIAL PRIMARY KEY,  numb varchar NOT NULL,  fk_chair_id integer REFERENCES chair(chair_id) NOT NULL);   

CREATE TABLE student
(student_id integer PRIMARY KEY, full_name text NOT NULL, passport char(10) NOT NULL, fk_numb_id integer REFERENCES student_group (numb_id) NOT NULL);
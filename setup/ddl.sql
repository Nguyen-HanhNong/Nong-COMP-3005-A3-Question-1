-- Name: Nguyen-Hanh Nong
-- Student Number: 101220611
-- File Name: ddl.sql
-- Purpose: Used to create the tables for Assignment 3 in COMP 3005

-- students Table
CREATE TABLE IF NOT EXISTS students (
    student_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    enrollment_date DATE
);
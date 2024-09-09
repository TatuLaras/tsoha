DROP TABLE IF EXISTS tl_user;
DROP TABLE IF EXISTS tl_course;
DROP TABLE IF EXISTS tl_course_article; 
DROP TABLE IF EXISTS tl_exercise_text;
DROP TABLE IF EXISTS tl_exercise_choice;
DROP TABLE IF EXISTS tl_exercise_choice_option;
DROP TABLE IF EXISTS tl_points;
DROP TABLE IF EXISTS tl_course_user;

CREATE TABLE tl_user (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_teacher BOOLEAN DEFAULT FALSE
);

CREATE TABLE tl_course (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    description TEXT,
    name TEXT NOT NULL
);

CREATE TABLE tl_course_user (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    UNIQUE (user_id, course_id)
);

CREATE TABLE tl_course_article (
    id SERIAL PRIMARY KEY,
    ordering SERIAL NOT NULL,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE tl_exercise_text (
    id SERIAL PRIMARY KEY,
    course_article_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

CREATE TABLE tl_exercise_choice (
    id SERIAL PRIMARY KEY,
    course_article_id INTEGER NOT NULL,
    question TEXT NOT NULL
);

CREATE TABLE tl_exercise_choice_option (
    id SERIAL PRIMARY KEY,
    exercise_choice_id INTEGER NOT NULL,
    label TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE
);

CREATE TABLE tl_points (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    type INTEGER NOT NULL DEFAULT 0, -- 1 = text, 2 = choice
    point INTEGER,
    UNIQUE (point, type, user_id)
);



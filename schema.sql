DROP SCHEMA IF EXISTS tlaras CASCADE;
CREATE SCHEMA tlaras;

CREATE TABLE tlaras.user (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_teacher BOOLEAN DEFAULT FALSE
);

CREATE TABLE tlaras.course (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    description TEXT,
    name TEXT NOT NULL
);

CREATE TABLE tlaras.course_user (
    id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    UNIQUE (user_id, course_id)
);

CREATE TABLE tlaras.course_article (
    id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL,
    ordering INTEGER NOT NULL DEFAULT 0,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE tlaras.exercise_text (
    id SERIAL PRIMARY KEY,
    course_article_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

CREATE TABLE tlaras.exercise_choice (
    id SERIAL PRIMARY KEY,
    course_article_id INTEGER NOT NULL,
    question TEXT NOT NULL
);

CREATE TABLE tlaras.exercise_choice_option (
    id SERIAL PRIMARY KEY,
    exercise_choice_id INTEGER NOT NULL,
    label TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE
);

CREATE TABLE tlaras.points (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    type INTEGER NOT NULL DEFAULT 0, -- 1 = text, 2 = choice
    point INTEGER,
    UNIQUE (point, type, user_id)
);

-- Really helpful, otherwise we would have some CHUNKY queries in the code
-- Use it like SELECT tlaras."percentage"([user_id], [course_id])
CREATE OR REPLACE FUNCTION tlaras.percentage(p_user_id INTEGER, p_course_id INTEGER) RETURNS DECIMAL AS $$
    SELECT CAST(
        (
            SELECT COUNT(*)

            FROM tlaras.points AS p

            LEFT JOIN tlaras.exercise_text AS et
            ON et.id = p.point AND p.type = 1

            LEFT JOIN tlaras.exercise_choice AS ec
            ON ec.id = p.point AND p.type = 2

            LEFT JOIN tlaras.course_article AS ca
            ON ca.id = et.course_article_id
            OR ca.id = ec.course_article_id

            WHERE p.user_id = p_user_id AND ca.course_id = p_course_id
        ) 
        AS DECIMAL
    )
    /
    GREATEST(
        (
            (
                SELECT COUNT(*) 

                FROM tlaras.exercise_choice AS ec

                LEFT JOIN tlaras.course_article AS ca
                ON ca.id = ec.course_article_id

                WHERE ca.course_id = p_course_id
            )
            +
            (
                SELECT COUNT(*) 

                FROM tlaras.exercise_text AS et

                LEFT JOIN tlaras.course_article AS ca
                ON ca.id = et.course_article_id

                WHERE ca.course_id = p_course_id
            )
        )
    , 1)
    ;
$$ LANGUAGE sql;

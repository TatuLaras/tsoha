DROP TABLE IF EXISTS tl_user;
CREATE TABLE tl_user (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_teacher BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS tl_course;
CREATE TABLE tl_course (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    description TEXT,
    name TEXT NOT NULL
);

DROP TABLE IF EXISTS tl_course_user;
CREATE TABLE tl_course_user (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    UNIQUE (user_id, course_id)
);

DROP TABLE IF EXISTS tl_course_article;
CREATE TABLE tl_course_article (
    id SERIAL PRIMARY KEY,
    ordering SERIAL NOT NULL,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

DROP TABLE IF EXISTS tl_exercise_text;
CREATE TABLE tl_exercise_text (
    id SERIAL PRIMARY KEY,
    course_article_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

DROP TABLE IF EXISTS tl_exercise_choice;
CREATE TABLE tl_exercise_choice (
    id SERIAL PRIMARY KEY,
    course_article_id INTEGER NOT NULL,
    question TEXT NOT NULL
);

DROP TABLE IF EXISTS tl_exercise_choice_option;
CREATE TABLE tl_exercise_choice_option (
    id SERIAL PRIMARY KEY,
    exercise_choice_id INTEGER NOT NULL,
    label TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS tl_points;
CREATE TABLE tl_points (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    type INTEGER NOT NULL DEFAULT 0, -- 1 = text, 2 = choice
    point INTEGER,
    UNIQUE (point, type, user_id)
);

-- Really helpful, otherwise we would have some CHUNKY queries in the code
-- Use it like SELECT "percentage"([user_id], [course_id])
CREATE OR REPLACE FUNCTION percentage(p_user_id INTEGER, p_course_id INTEGER) RETURNS DECIMAL AS $$
    SELECT CAST(
        (
            SELECT COUNT(*)

            FROM tl_points AS p

            LEFT JOIN tl_exercise_text AS et
            ON et.id = p.point AND p.type = 1

            LEFT JOIN tl_exercise_choice AS ec
            ON ec.id = p.point AND p.type = 2

            LEFT JOIN tl_course_article AS ca
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

                FROM tl_exercise_choice AS ec

                LEFT JOIN tl_course_article AS ca
                ON ca.id = ec.course_article_id

                WHERE ca.course_id = p_course_id
            )
            +
            (
                SELECT COUNT(*) 

                FROM tl_exercise_text AS et

                LEFT JOIN tl_course_article AS ca
                ON ca.id = et.course_article_id

                WHERE ca.course_id = p_course_id
            )
        )
    , 1)
    ;
$$ LANGUAGE sql;

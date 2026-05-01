-- 1. Wipe the existing slate clean so we don't get duplicates
DELETE FROM game_clue_state;
DELETE FROM clues;
DELETE FROM categories;
DELETE FROM sqlite_sequence WHERE name IN ('categories', 'clues');

-- 2. Insert Three Categories
INSERT INTO categories (title) VALUES ('Python Basics');
INSERT INTO categories (title) VALUES ('Canadian Geography');
INSERT INTO categories (title) VALUES ('Engineering Fundamentals');

-- 3. Insert Clues for Category 1: Python Basics (ID 1)
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (1, 'A mutable array', 'What is a list?', 200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (1, 'An immutable array', 'What is a tuple?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (1, 'The keyword used to define a function', 'What is def?', 600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (1, 'A collection of key-value pairs', 'What is a dictionary?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (1, 'The method used to add an item to the end of a list', 'What is append?', 1000);

-- 4. Insert Clues for Category 2: Canadian Geography (ID 2)
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (2, 'The capital city of the country', 'What is Ottawa?', 200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (2, 'This province is home to the oil sands and the majestic Rocky Mountains', 'What is Alberta?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (2, 'The largest city in British Columbia', 'What is Vancouver?', 600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (2, 'This easternmost province is known for its unique time zone', 'What is Newfoundland and Labrador?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (2, 'The enormous bay that dominates the map of northern Canada', 'What is Hudson Bay?', 1000);

-- 5. Insert Clues for Category 3: Engineering Fundamentals (ID 3)
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (3, 'The acronym HVAC stands for Heating, Ventilation, and this', 'What is Air Conditioning?', 200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (3, 'This force resists the relative motion of solid surfaces sliding against each other', 'What is friction?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (3, 'In fluid dynamics, this principle explains how airplane wings generate lift', 'What is Bernoulli''s principle?', 600); -- Note: Double single-quote to escape the apostrophe!
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (3, 'The fundamental thermodynamic property that measures a system''s thermal energy per unit temperature', 'What is entropy?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (3, 'A structural element that primarily resists loads applied laterally to its axis', 'What is a beam?', 1000);


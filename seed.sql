-- 1. Wipe the existing slate clean so we don't get duplicates
DELETE FROM game_clue_state;
DELETE FROM clues;
DELETE FROM categories;
DELETE FROM sqlite_sequence WHERE name IN ('categories', 'clues');

-- 2. Insert Five Categories
INSERT INTO categories (title) VALUES ('ROBO-TECH');
INSERT INTO categories (title) VALUES ('MARTIAL ARTS');
INSERT INTO categories (title) VALUES ('MAKING MUSIC');
INSERT INTO categories (title) VALUES ('SCIENCE CLASS');
INSERT INTO categories (title) VALUES ('VIDEO GAMES');

-- 3. Insert Clues for Category 1: ROBO-TECH (ID 1)
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (1, 'This part of a computer or robot acts like its ''brain'', processing all the code and instructions.', 'What is a CPU / Processor?', 200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (1, 'This type of machine is programmed to do tasks automatically, like vacuuming your floor or building cars.', 'What is a robot?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (1, 'These sensors on a robot act like its ''eyes,'' bouncing sound or light to detect walls in front of it.', 'What are ultrasonic/infrared sensors?', 600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (1, 'In computer programming, this is a sequence of instructions that repeats over and over again.', 'What is a loop?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (1, 'This mechanical joint allows a robot arm to bend, operating just like the middle of your own arm.', 'What is a hinge joint (or elbow)?', 1000);

-- 4. Insert Clues for Category 2: MARTIAL ARTS (ID 2)
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (2, 'In many martial arts, this color belt represents a beginner who is just starting to learn.', 'What is a White Belt?', 200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (2, 'This Korean martial art is an Olympic sport famous for its fast, high-flying kicks and spinning strikes.', 'What is Taekwondo?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (2, 'This piece of padded safety gear is worn on your head during sparring to protect against high kicks.', 'What is headgear / a helmet?', 600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (2, 'This is the Japanese word for the training hall or school where you practice martial arts like Karate or Judo.', 'What is a Dojo?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (2, 'When a martial artist breaks a wooden board with their foot, they are demonstrating this specific type of strike.', 'What is a kick?', 1000);

-- 5. Insert Clues for Category 3: MAKING MUSIC (ID 3)
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (3, 'This large instrument has 88 black and white keys.', 'What is a piano?', 200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (3, 'This section of an orchestra includes instruments you hit or shake, like drums, cymbals, and tambourines.', 'What is the percussion section?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (3, 'Plucking the four strings of this small, guitar-like instrument from Hawaii creates a happy, bouncy sound.', 'What is a ukulele?', 600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (3, 'This symbol at the beginning of a staff of music tells you what notes the lines represent; the ''Treble'' one is very common.', 'What is a clef?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (3, 'This is the person who stands in front of an orchestra and directs the musicians using a small stick called a baton.', 'What is a conductor?', 1000);

-- 6. Insert Clues for Category 4: SCIENCE CLASS (ID 4)
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (4, 'This is the invisible pull that keeps you on the ground and stops you from floating away into space.', 'What is gravity?', 200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (4, 'Water freezes into ice at this exact temperature in Fahrenheit.', 'What is 32 degrees?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (4, 'This green pigment found in leaves helps plants make their own food from sunlight.', 'What is chlorophyll?', 600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (4, 'Solid, Liquid, and Gas are known as the three main states of this.', 'What is matter?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (4, 'This gas is what humans and animals breathe out, and what plants absorb to live.', 'What is carbon dioxide?', 1000);

-- 7. Insert Clues for Category 5: VIDEO GAMES (ID 5)
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (5, 'In Minecraft, you use your character''s bare hands to punch these natural objects to gather wood.', 'What are trees?', 200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (5, 'This famous plumber wears a red hat and jumps on Goombas to save Princess Peach.', 'Who is Mario?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (5, 'In this battle royale game, players drop from a flying bus and build structures to survive the storm.', 'What is Fortnite?', 600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (5, 'An accidental error or glitch in a video game''s programming code is commonly known by this insect-themed name.', 'What is a bug?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) 
VALUES (5, 'This programming term describes the invisible boxes used by game engines to determine when two characters bump into each other.', 'What is collision detection?', 1000);
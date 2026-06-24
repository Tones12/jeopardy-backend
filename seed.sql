-- Wipe the existing slate clean
DELETE FROM game_clue_state;
DELETE FROM clues;
DELETE FROM categories;
DELETE FROM sqlite_sequence WHERE name IN ('categories', 'clues');

-- ==========================================
-- ROUND 1: SINGLE JEOPARDY
-- ==========================================
INSERT INTO categories (title, round_name) VALUES ('ROBO-TECH', 'Jeopardy');
INSERT INTO categories (title, round_name) VALUES ('MARTIAL ARTS', 'Jeopardy');
INSERT INTO categories (title, round_name) VALUES ('MAKING MUSIC', 'Jeopardy');
INSERT INTO categories (title, round_name) VALUES ('SCIENCE CLASS', 'Jeopardy');
INSERT INTO categories (title, round_name) VALUES ('VIDEO GAMES', 'Jeopardy');

-- Category 1
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (1, 'This part of a computer or robot acts like its ''brain'', processing all the code and instructions.', 'What is a CPU / Processor?', 200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (1, 'This type of machine is programmed to do tasks automatically, like vacuuming your floor or building cars.', 'What is a robot?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (1, 'These sensors on a robot act like its ''eyes,'' bouncing sound or light to detect walls in front of it.', 'What are ultrasonic/infrared sensors?', 600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (1, 'In computer programming, this is a sequence of instructions that repeats over and over again.', 'What is a loop?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (1, 'This mechanical joint allows a robot arm to bend, operating just like the middle of your own arm.', 'What is a hinge joint (or elbow)?', 1000);

-- Category 2
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (2, 'In many martial arts, this color belt represents a beginner who is just starting to learn.', 'What is a White Belt?', 200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (2, 'This Korean martial art is an Olympic sport famous for its fast, high-flying kicks and spinning strikes.', 'What is Taekwondo?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (2, 'This piece of padded safety gear is worn on your head during sparring to protect against high kicks.', 'What is headgear / a helmet?', 600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (2, 'This is the Japanese word for the training hall or school where you practice martial arts like Karate or Judo.', 'What is a Dojo?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (2, 'When a martial artist breaks a wooden board with their foot, they are demonstrating this specific type of strike.', 'What is a kick?', 1000);

-- Category 3
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (3, 'This large instrument has 88 black and white keys.', 'What is a piano?', 200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (3, 'This section of an orchestra includes instruments you hit or shake, like drums, cymbals, and tambourines.', 'What is the percussion section?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (3, 'Plucking the four strings of this small, guitar-like instrument from Hawaii creates a happy, bouncy sound.', 'What is a ukulele?', 600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (3, 'This symbol at the beginning of a staff of music tells you what notes the lines represent; the ''Treble'' one is very common.', 'What is a clef?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (3, 'This is the person who stands in front of an orchestra and directs the musicians using a small stick called a baton.', 'What is a conductor?', 1000);

-- Category 4
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (4, 'This is the invisible pull that keeps you on the ground and stops you from floating away into space.', 'What is gravity?', 200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (4, 'Water freezes into ice at this exact temperature in Fahrenheit.', 'What is 32 degrees?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (4, 'This green pigment found in leaves helps plants make their own food from sunlight.', 'What is chlorophyll?', 600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (4, 'Solid, Liquid, and Gas are known as the three main states of this.', 'What is matter?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (4, 'This gas is what humans and animals breathe out, and what plants absorb to live.', 'What is carbon dioxide?', 1000);

-- Category 5
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (5, 'In Minecraft, you use your character''s bare hands to punch these natural objects to gather wood.', 'What are trees?', 200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (5, 'This famous plumber wears a red hat and jumps on Goombas to save Princess Peach.', 'Who is Mario?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (5, 'In this battle royale game, players drop from a flying bus and build structures to survive the storm.', 'What is Fortnite?', 600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (5, 'An accidental error or glitch in a video game''s programming code is commonly known by this insect-themed name.', 'What is a bug?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (5, 'This programming term describes the invisible boxes used by game engines to determine when two characters bump into each other.', 'What is collision detection?', 1000);

-- ==========================================
-- ROUND 2: DOUBLE JEOPARDY
-- ==========================================
INSERT INTO categories (title, round_name) VALUES ('ANIMAL KINGDOM', 'Double Jeopardy');
INSERT INTO categories (title, round_name) VALUES ('SPACE EXPLORATION', 'Double Jeopardy');
INSERT INTO categories (title, round_name) VALUES ('FAIRY TALES', 'Double Jeopardy');
INSERT INTO categories (title, round_name) VALUES ('SPORTS', 'Double Jeopardy');
INSERT INTO categories (title, round_name) VALUES ('FOOD & DRINK', 'Double Jeopardy');

-- Category 6 (Animal Kingdom)
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (6, 'This is the tallest living land animal in the world.', 'What is a giraffe?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (6, 'This large cat is known for its black stripes and orange fur.', 'What is a tiger?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (6, 'This marine mammal is highly intelligent and is known to travel in pods.', 'What is a dolphin (or whale)?', 1200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (6, 'This bird cannot fly but is an excellent swimmer, native to the Southern Hemisphere.', 'What is a penguin?', 1600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (6, 'This is the only mammal capable of true sustained flight.', 'What is a bat?', 2000);

-- Category 7 (Space Exploration)
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (7, 'This is the planet closest to the sun.', 'What is Mercury?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (7, 'This force keeps the planets in orbit around the sun.', 'What is gravity?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (7, 'This large galaxy, home to our solar system, gets its name from looking like spilled milk.', 'What is the Milky Way?', 1200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (7, 'He was the first human to step foot on the moon in 1969.', 'Who is Neil Armstrong?', 1600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (7, 'This is the name of the largest telescope ever launched into space by NASA, named after an astronomer.', 'What is the Hubble Space Telescope (or James Webb)?', 2000);

-- Category 8 (Fairy Tales)
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (8, 'She leaves behind a glass slipper at the royal ball.', 'Who is Cinderella?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (8, 'This wooden puppet wishes to become a real boy.', 'Who is Pinocchio?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (8, 'He climbs a magical beanstalk and finds a giant''s castle in the clouds.', 'Who is Jack?', 1200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (8, 'This princess bites a poisoned apple and falls into a deep sleep.', 'Who is Snow White?', 1600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (8, 'This clever pig builds his house out of bricks to keep the Big Bad Wolf away.', 'Who is the Third Little Pig?', 2000);

-- Category 9 (Sports)
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (9, 'In this sport, players try to hit a ball over a net using a racket.', 'What is tennis?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (9, 'This track and field event involves jumping over a high bar onto a mat.', 'What is the high jump?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (9, 'A "turkey" in this sport means you rolled three strikes in a row.', 'What is bowling?', 1200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (9, 'This position in soccer is the only one allowed to use their hands on the field.', 'What is the goalie (or goalkeeper)?', 1600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (9, 'In baseball, this is the term for hitting a home run when the bases are fully loaded.', 'What is a Grand Slam?', 2000);

-- Category 10 (Food & Drink)
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (10, 'This sweet treat is made by churning milk, cream, and sugar, and freezing it.', 'What is ice cream?', 400);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (10, 'This fruit is known for keeping the doctor away if you eat one a day.', 'What is an apple?', 800);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (10, 'This classic Italian dish features long, thin noodles often topped with tomato sauce and meatballs.', 'What is spaghetti?', 1200);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (10, 'This crunchy vegetable is famously Bugs Bunny''s favorite snack.', 'What is a carrot?', 1600);
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (10, 'This yellow tropical fruit has a thick, spiky skin and a green crown of leaves on top.', 'What is a pineapple?', 2000);

-- ==========================================
-- ROUND 3: FINAL JEOPARDY
-- ==========================================
INSERT INTO categories (title, round_name) VALUES ('GEOGRAPHY', 'Final Jeopardy');
INSERT INTO clues (category_id, clue_text, correct_response, dollar_value) VALUES (11, 'Spanning over 4,000 miles, this is the longest river in the world, flowing northward through Africa into the Mediterranean Sea.', 'What is the Nile River?', 0);
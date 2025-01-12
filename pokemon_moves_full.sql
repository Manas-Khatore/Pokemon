--DROP TABLE move_details;

CREATE TABLE move_details (
index INT PRIMARY KEY,
name TEXT,
type TEXT,
category TEXT,
contest TEXT,
pp INT,
power TEXT,
accuracy TEXT,
generation INT
);

COPY move_details(index, name, type, category, contest,
pp, power, accuracy, generation)
FROM '/Users/manaskhatore/Projects/Pokemon/move-data.csv'
DELIMITER ','
CSV HEADER;

ALTER TABLE move_pool_moves_unnest
RENAME name TO pokemon_name;

ALTER TABLE move_details
RENAME name TO move_name;

CREATE TABLE pokemon_moves_full AS
SELECT * FROM move_pool_moves_unnest mp
INNER JOIN move_details md ON
mp.move = md.move_name;
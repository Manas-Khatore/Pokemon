CREATE TABLE move_pool_modified AS
SELECT name, 
SUBSTRING(types, 2, LENGTH(types) - 2) AS types,
CASE
	WHEN LENGTH(next_evol) = 2 THEN ''
	ELSE SUBSTRING(next_evol, 2, LENGTH(next_evol) - 2)
END AS next_evol,
SUBSTRING(moves, 2, LENGTH(moves) - 2) AS moves
FROM move_pool;

UPDATE move_pool_modified SET types = replace(types, '''', '');
UPDATE move_pool_modified SET next_evol = replace(next_evol, '''', '');
UPDATE move_pool_modified SET moves = replace(moves, '''', '');
UPDATE move_pool_modified SET moves = replace(moves, '""', '');

UPDATE move_pool_modified SET types = REGEXP_REPLACE(types, ',\s+', ',', 'g');
UPDATE move_pool_modified SET next_evol = REGEXP_REPLACE(next_evol, ',\s+', ',', 'g');
UPDATE move_pool_modified SET moves = REGEXP_REPLACE(moves, ',\s+', ',', 'g');

ALTER TABLE move_pool_modified
ADD COLUMN type1 TEXT,
ADD COLUMN type2 TEXT;

UPDATE move_pool_modified 
SET type1 = SPLIT_PART(types, ',', 1),
type2 = SPLIT_PART(types, ',', 2);

ALTER TABLE move_pool_modified
DROP COLUMN types;

CREATE TABLE move_pool_moves_unnest AS
SELECT name, next_evol, type1, type2, 
unnest(string_to_array(moves, ',')) AS move FROM move_pool_modified;

UPDATE move_pool_moves_unnest SET move = replace(move, '"', '');

SELECT * FROM move_pool_moves_unnest;


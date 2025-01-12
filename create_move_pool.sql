--DROP TABLE move_pool;

CREATE TABLE move_pool (
name text PRIMARY KEY,
types text,
next_evol text,
moves text
);

COPY move_pool(name, types, next_evol, moves)
FROM '/Users/manaskhatore/Projects/Pokemon/move_pool.csv'
DELIMITER ','
CSV HEADER;
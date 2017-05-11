-- Table definitions for the tournament project.
DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament;
drop table players;
-- Put your SQL 'create table' statements in this file;
-- also 'create view' statements if you choose to use it.
create table players (
  player_id serial PRIMARY KEY,
  name text,
  wins integer,
  matches integer
);

-- create table matches (
--   player_id integer references players(player_id),
--   wins integer,
--   matches integer
-- );


-- You can write comments in this
--file by starting them with two dashes, like these lines here.
CREATE VIEW player_count AS SELECT COUNT(player_id) FROM players;

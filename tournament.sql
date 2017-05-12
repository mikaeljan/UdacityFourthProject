-- Database
DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament;
drop table players;

-- Tables
create table players (
  player_id serial PRIMARY KEY,
  name text
);

drop table matches;
create table matches (
  winner_id integer references players(player_id),
  loser_id integer references players(player_id),
  matches serial primary key
);

-- Views
CREATE VIEW player_count AS SELECT COUNT(player_id) FROM players;

CREATE VIEW standings_view AS
SELECT players.player_id, players.name,

            (SELECT COUNT(matches.winner_id)
             FROM matches
             WHERE players.player_id = matches.winner_id)
             AS wins,

            (SELECT COUNT(matches.winner_id)
             FROM matches
             WHERE players.player_id = matches.winner_id
             OR players.player_id = matches.loser_id)
            AS matches

FROM players
ORDER BY wins,matches;

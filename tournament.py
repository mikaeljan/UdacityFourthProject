#!/usr/bin/env python
#
import psycopg2, bleach, itertools

def connect():
    """Connect to the PostgreSQL database. Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM player_count")
    number_players = c.fetchall()
    db.close()
    if not number_players:
        return 0
    else:
        return int(number_players[0][0])

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players (name) values (%s)", (bleach.clean(name),))
    # c.execute("UPDATE matches SET matches = 0")
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute('''SELECT * FROM standings_view ORDER BY wins DESC''')
    result = c.fetchall()
    db.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute('''INSERT INTO matches (winner_id, loser_id)
                 VALUES (%s,%s)''', [(winner,),(loser,)])
    # c.execute("UPDATE matches SET winner_id =  (%s)", (bleach.clean(winner),))
    # c.execute("UPDATE matches SET loser_id =  (%s)", (bleach.clean(loser),))
    # c.execute("UPDATE matches SET matches = matches + 1 where winner_id = (%s)", (bleach.clean(winner),))
    # c.execute("UPDATE matches SET matches = matches + 1 where loser_id = (%s)", (bleach.clean(loser),))
    # c.execute("UPDATE players SET wins = wins + 1 where player_id = (%s)", (bleach.clean(winner),))
    db.commit()
    db.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered,
    each player appears exactly once in the pairings.
    Each player is paired with another
    player with an equal or nearly-equal win record, that is,
    a player adjacent to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    c.execute('SELECT player_id FROM standings_view ORDER BY wins;')
    player_ids = c.fetchall()
    c.execute('SELECT name FROM standings_view ORDER BY wins;')
    names = c.fetchall()
    # This was solution presented in forum by one of my fellow classmates.

    # pair1 = zip(player_ids[0], names[0], player_ids[1], names[1])
    # pair2 = zip(player_ids[2], names[2], player_ids[3], names[3])
    # pair3 = zip(player_ids[4], names[4], player_ids[5], names[5])
    # pair4 = zip(player_ids[6], names[6], player_ids[7], names[7])
    # pairs = pair1 + pair2 + pair3 + pair4
    # return pairs


    # It is specifically used for certain amount of pairs (8) I have decided to find a way to make it more general.
    # in case that there is different amount of teams.
    pair_in_pairs =[aa + bb for (aa, bb) in itertools.izip(player_ids, names)]
    final_pairings = [aa + bb for (aa, bb) in itertools.izip(pair_in_pairs[::2],pair_in_pairs[1::2])]
    db.close()
    return final_pairings

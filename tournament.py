#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random

def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # return psycopg2.connect("dbname=tournament")
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""

    db, cursor = connect()
    cursor. execute("DELETE FROM matches;")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""

    db, cursor = connect()
    cursor. execute("DELETE FROM players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""

    db, cursor = connect()
    cursor. execute("SELECT count(*) FROM players;")
    no_of_players = cursor.fetchone()
    db.close()
    return no_of_players[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()

    cursor. execute("INSERT INTO players(name) values(%s)",(name,))

    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db, cursor = connect()
    query ="""SELECT p.id, p.name,
                                 (SELECT count(*)
                                 FROM matches
                                 WHERE winner = p.id or loser = p.id)
                                 as num_matches,
                                                (SELECT count(*)
                                                 FROM matches
                                                 WHERE winner = p.id)
                                                 as num_wins
             FROM players as p
             ORDER BY num_wins desc"""
    cursor. execute(query)
    standings = cursor.fetchall()
    playerstandings = []
    for row in standings:
        playerstandings.append((row[0], row[1], int(row[3]), int(row[2])))
    db.close()
    return playerstandings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db, cursor = connect()
    cursor. execute("""INSERT INTO matches (winner,loser)
                  VALUES (%s, %s)""",(winner,loser,))
    db.commit()
    db.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []
    standings = playerStandings()

    ids_list = []
    for player in standings:
        ids_list.append(player[0])

    while len(ids_list) > 0:
        player1 = ids_list[0]
        ids_list.remove(player1)
        player2 = ids_list[0]
        ids_list.remove(player2)

        db, cursor = connect()
        cursor. execute("SELECT name FROM players WHERE id = %s;",(player1,))
        player1_name = cursor.fetchone()
        cursor. execute("SELECT name FROM players WHERE id = %s;",(player2,))
        player2_name = cursor.fetchone()
        pairings.append((player1, player1_name[0], player2, player2_name[0]))
        db.close()
    return pairings


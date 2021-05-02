"""functions for interfacing with postgreSQL"""

import psycopg2 as pg2
import psycopg2.extras
import time

def connect_to_postgres():
    """Preconfigured connections to the postgres database"""
    con = pg2.connect(host='this_postgres', user='postgres', database='postgres', password='pw4nick',cursor_factory=psycopg2.extras.DictCursor)
    return con, con.cursor()

def insert_game(game,timeC):
    con, cur = connect_to_postgres()
    query = "insert into games (\"white\",\"black\",\"moves\",\"result\",\"time\") values ('"+game.headers["White"]+"','"+game.headers["Black"]+"','"+str(game.mainline())+"','"+game.headers["Result"]+"',"+str(timeC)+")"
    cur.execute(query)
    con.commit()
       
def insert_match(player_white,player_black,games,dep,score,whiteBookMoves,blackBookMoves):
    con, cur = connect_to_postgres()
    
    cur.execute("select * from matches where white = \'" + str(player_white) + "\' and black = \'" + str(player_black) + "\' and dep = " + str(dep) + "")
    res = cur.fetchall()
    if len(res)==1:
        query = 'update matches set (\"games\",\"score\",\"percent\",\"whitebookmoves\",\"blackbookmoves\") = (' + str(res[0]['games'] + games) + ',' + str(res[0]['score'] + score) + ',' + str(float(res[0]['score'] + score)/(res[0]['games'] + games)) + ',' + str(res[0]['whitebookmoves']+whiteBookMoves) + ',' + str(res[0]['blackbookmoves']+blackBookMoves) + ') where white = \'' + player_white + '\' and black = \'' + player_black + '\' and dep = ' + str(dep) + ''
        cur.execute(query)
        con.commit()
    else:
        query = "insert into matches (\"white\",\"black\",\"games\",\"dep\",\"whitebookmoves\",\"blackbookmoves\",\"score\",\"percent\") values ('"+player_white+"','"+player_black+"',"+str(games)+","+str(dep)+","+str(whiteBookMoves)+","+str(blackBookMoves)+","+str(score)+","+str(float(score/games))+")"
        cur.execute(query)
        con.commit()
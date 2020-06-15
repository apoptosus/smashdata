import sqlite3
from bs4 import BeautifulSoup

# enter tourney data into smash.db
def create_rank_table():
    conn = sqlite3.connect('/home/trentley/smash.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE SSBMRank (
    RID INTEGER PRIMARY KEY,
	Rank INT NOT NULL,
   	Name TEXT NOT NULL,
	Chars TEXT NOT NULL,
    Points FLOAT NOT NULL,
    Change INT,
    Year TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()
    print("SSBMRank table created")

def create_mus_table():
    pass

def tournament_entry(tournament_name, tournament_date, tournament_prize, tournament_participants, tournament_city, tournament_country, winner, runner_up, link):
    conn = sqlite3.connect('/home/trentley/smash.db')
    c = conn.cursor()

    params = tournament_name, tournament_date, tournament_prize, tournament_participants, tournament_city, tournament_country, winner, runner_up, link

    c.executemany("INSERT INTO TOURNAMENTS (NAME, DATE, PRIZE, PARTICIPANTS, CITY, COUNTRY, WINNER, RUNNERUP, LINK) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (params,))
    conn.commit()
    conn.close()

    print('{} data entered'.format(tournament_name))

def raw_character_entry(p1_name, char1, stage, p2_name, char2, tournament_name):
    conn = sqlite3.connect('/home/trentley/smash.db')
    c = conn.cursor()

    params = p1_name, char1, stage, p2_name, char2, tournament_name

    c.executemany("INSERT INTO MUs (P1name, P1char, Stage, P2name, P2char, Tournament) VALUES (?, ?, ?, ?, ?, ?)", (params,))
    conn.commit()
    conn.close
    print("Entered {} vs {} at {}".format(p1_name, p2_name, stage))

def rank_entry(rank, name, chars, points, change, year):
    conn = sqlite3.connect('/home/trentley/smash.db')
    c = conn.cursor()
    params = rank, name, chars, points, change, year
    c.executemany("INSERT INTO SSBMRANK (RANK, NAME, CHARS, POINTS, CHANGE, YEAR) VALUES (?, ?, ?, ?, ?, ?)", (params,))
    conn.commit()
    conn.close()

    print('Entering rank: {}, name: {}, chars: {}, points: {}, change: {}, year: {}'.format(rank, name, chars, points, change, year))

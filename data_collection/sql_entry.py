import sqlite3
from bs4 import BeautifulSoup

# enter tourney data into smash.db
def create_table():
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

def rank_entry(rank, name, chars, points, change, year):
    conn = sqlite3.connect('/home/trentley/smash.db')
    c = conn.cursor()
    params = rank, name, chars, points, change, year
    c.executemany("INSERT INTO SSBMRANK (RANK, NAME, CHARS, POINTS, CHANGE, YEAR) VALUES (?, ?, ?, ?, ?, ?)", (params,))
    conn.commit()
    conn.close()

    print('SSBMRANK data entered')

# class Player:
#     def __init__(self, rank, name, chars, points, change, year):
#         self.rank = rank
#         self.name = name
#         self.chars = chars
#         self.points = points
#         self.change = change
#         self.year = year

#     def __str__(self):
#         print(f'rank: {self.rank}, name: {self.name}, chars: {self.chars}, points: {self.points}, change: {self.change}')


# scrapes ssbm info from txt file holding html of https://liquipedia.net/smash/SSBMRank
# enters the scraped data in sqlite
def ssbmrank_scrape():
    # scrape miom.txt
    # Reading the copied txt file
    miom = open("/home/trentley/PycharmProjects/smashdata/version2/miom.txt", "r")
    txtContent = miom.read()
    miom.close()

    # Creating a bs4 object for scraping
    soup = BeautifulSoup(txtContent, 'lxml')

    # separate tables by year content1-content12 (2013 -2019)
    for table in range(1,12):
        year_list = soup.find("div", {"class": "content{}".format(table)})
        year = year_list.find("span")['id']
        rankings = year_list.find_all("tr")
        players = []

        for line in rankings:
            stats = line.find_all("td")


            try:
                rank = stats[0].get_text()
                
                name = stats[1].get_text()
                name = name[1:]
                if name[-1] == " ":
                    name = name[:-1]
                
                
                char_info = stats[2].find_all("img")
                chars = []
                for char in char_info:
                    chars.append(char['alt'])
                chars = ', '.join(chars)
                
                points = stats[3].get_text()

                if year == '2013':
                    change = None
                    rank_entry(rank, name, chars, points, change, year)
                
                change = stats[4].get_text()[-3:]
                change = change.replace('+', '')
                try:
                    int(change)
                except ValueError:
                    change = None
                print(name, len(name), year, change)

                # run SQLITE ENTRY FUNCTION
                rank_entry(rank, name, chars, points, change, year)
            
            except IndexError:
                pass 

create_table()
ssbmrank_scrape()

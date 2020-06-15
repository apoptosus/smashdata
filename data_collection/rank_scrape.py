import sql_entry

# enters the scraped data in sqlite
def ssbmrank_scrape():
    # scrape stored miom text file
    miom = open("../data/miom.txt", "r")
    txtContent = miom.read()
    miom.close()

    # Creating a bs4 object for scraping
    soup = BeautifulSoup(txtContent, 'lxml')

    # separate tables by year content1-content12 (2013 -2019)
    for table in range(1,13):
        year_list = soup.find("div", {"class": "content{}".format(table)})
        year = year_list.find("span")['id']
        rankings = year_list.find_all("tr")
        players = []

        # each line stores all information on player rank
        for line in rankings:
            stats = line.find_all("td")
            
            try:
                # name of player
                rank = stats[0].get_text()
                name = stats[1].get_text()
                name = name[1:]
                if name[-1] == " ":
                    name = name[:-1]
                
                # chars used
                char_info = stats[2].find_all("img")
                chars = []
                for char in char_info:
                    chars.append(char['alt'])
                chars = ', '.join(chars)
                
                # points associated with player rank
                points = stats[3].get_text()

                # standardization of points upon entry
                if year == '2013':
                    change = None
                    rank_entry(rank, name, chars, points, change, year)
                
                if year == '2017' or year == '2018' or year == '2019':
                    points = float(points)/10

                # change in rank since last ranking
                change = stats[4].get_text()[-3:]
                change = change.replace('+', '')
                
                # Adjust for new players with unknown change data
                try:
                    int(change)
                except ValueError:
                    change = None

                # enter info into sqlite
                sql_entry.rank_entry(rank, name, chars, points, change, year)
            
            except IndexError:
                pass 

if __name__ == '__main__':
    ssbmrank_scrape()
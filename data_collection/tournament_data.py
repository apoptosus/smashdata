
import os


def tournament_links():
    from bs4 import BeautifulSoup
    # Copied the above result to a text file to avoid calling the API for this info in the future

    # Reading the copied txt file
    tourns = open("/home/trentley/PycharmProjects/smashdata/version2/tournaments.txt", "r")
    txtContent = tourns.read()
    tourns.close()
    

    # cleans edge case strings
    def clean_name(string, stop_char):
        if stop_char in string:
            for i in range(0, len(string)-1):
                if string[i] == stop_char:
                    return string[0:i]
            return string
        else:
            return string

    # list of links to tournaments that will be further scraped
    links = []
    endpoints = []

    # Creating a bs4 object for scraping
    soup = BeautifulSoup(txtContent, 'lxml')

    # Finds the code chunk for all tournament information
    tournaments = soup.find_all(class_="divRow")

    # Looks at an individual tournament's html/css in tournament's list
    for tournament in tournaments:

        # LINK to Tournament Single's Bracket
        tournament_header = tournament.find(class_="divCell Tournament Header")
        href = tournament_header.find('b').find('a')['href']
        link = 'https://liquipedia.net' + href
        endpoint = href[7:]
        endpoints.append(endpoint)
        links.append(link)

        # TOURNAMENT NAME
        tournament_name = tournament_header.find('b').string

        # TOURNAMENT DATE
        tournament_date = tournament.find(class_='divCell EventDetails-Left-55 Header').string


        # WINNER of each tournament
        try:
            first_place = tournament.find(class_="divCell Placement FirstPlace")
            first_place = first_place.find_all('a')
            first_place = first_place[-1]['title']
            winner = clean_name(first_place, '(')
            # Skip future tourns
            if first_place[0:3] == 'TBD':
                continue
        # Skip tourns without winner information
        except IndexError:
            continue
        
        # RUNNER UP
        try:
            second_place = tournament.find(class_="divCell Placement SecondPlace")
            second_place = second_place.find_all('a')
            second_place = second_place[-1]['title']
            runner_up = clean_name(second_place, '(')
        except IndexError:
            continue

        # PRIZE MONEY
        tournament_prize = tournament.find(class_="divCell EventDetails-Right-45 Header").string
        if tournament_prize is not None:
            tournament_prize = tournament_prize.replace("$", "").replace(",", "")
        try:
            int(tournament_prize)
        except ValueError:
            tournament_prize = None


        # NUMB PARTICIPANTS
        try:
            tournament_participants = tournament.find(class_='divCell EventDetails-Left-40 Header').find('span').string
        except AttributeError:
            tournament_participants = None


        # LOCATION
        try:
            # country
            tournament_country = tournament.find(class_="divCell EventDetails-Right-60 Header").find('a')['title']
            # city
            tournament_city = tournament.find(class_="divCell EventDetails-Right-60 Header").get_text()
            tournament_city = tournament_city[1::]
            if tournament_city == "":
                tournament_city = None
        
        except AttributeError:
            print('att err')
            tournament_city = None

        # print(f"winner: {winner}, runnerup:{runner_up}, prize:{tournament_prize}, part:{tournament_participants}, loc: {tournament_country}")
        # tournament_entry(tournament_name, tournament_date, tournament_prize, tournament_participants, tournament_city, tournament_country, winner, runner_up, link)
    return links, endpoints
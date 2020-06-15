import api_request
import tournament_data
import sql_entry
import time
from bs4 import BeautifulSoup

# simple cleaning function
def parser(string, stop_char):
    if string is not None:
        for i in range(0, len(string) - 1):
            if string[i] == stop_char:
                return string[i + 1::]


# data = raw json text
def scrape_characters(data, tournament_name):
    soup = BeautifulSoup(data, 'lxml')
    # find all instances of game divisions
    all_sets = soup.find_all(class_="bracket-game")

    # Separate code by bracket-game divisions
    # Character data exists outside of this bracket class
    # and requires a different method to obtain and map to players
    for i in all_sets:
        try:
            # find name of player1
            p1 = i.find(class_="bracket-player-top")
            name = str(p1.find_all('span')[1])
            name = name[0:-7]
            p1_name = parser(name, '>')
            # find score of player 1
            p1_score = p1.find(class_="bracket-score").get_text()
        except IndexError:
            p1_name = 'BYE'
        except AttributeError:
            pass

        try:
            int(p1_score)
        except ValueError:
            p1_score = 'N/A'
        except UnboundLocalError:
            p1_score = 'N/A'

        # find name of player2
        try:
            p2 = i.find(class_="bracket-player-bottom")
            name = str(p2.find_all('span')[1])
            name = name[0:-7]
            p2_name = parser(name, '>')
            # find score of player 2
            p2_score = p2.find(class_="bracket-score").get_text()
        except IndexError:
            p2_name = 'BYE'
        except AttributeError:
            continue
        
        # Correct for unknown p2 score values
        try:
            int(p2_score)
        except ValueError:
            p2_score = 'N/A'
        except UnboundLocalError:
            p2_score = 'N/A'

        # find character and stage info of a match
        match = i.find_all(class_="bracket-popup-body-match")
        p1_chars_used = set()
        p2_chars_used = set()
        stages = []

        # game is a list of all divs in a single match display, unsorted
        for game in match:

            # section is a single div in the div line of results display
            # it contains unparsed information about:
            # both player characters, the stage, and the winner of the game
            for section in game:

                # child is an isolated line of information about player1, stage, player2, repeat
                count = 1
                for child in section.children:

                    # collect player1 info
                    if count == 1:
                        try:
                            img = child.find('img')
                            src = img['src'][0:-8]
                            char1 = parser(src, '-')
                            p1_chars_used.add(char1)

                            try:
                                child['class']
                                char1 += '(W)'
                            except:
                                char1 += '(L)'
                        except TypeError:
                            char1 = ""

                    # collect stage info
                    elif count == 2:
                        stage = child.string
                        stages.append(stage)
                        if stage == None:
                            continue

                    # collect player2 info
                    elif count == 3:
                        try:
                            img = child.find('img')
                            src = img['src'][0:-8]
                            char2 = parser(src, '-')
                            p2_chars_used.add(char2)
                            count = 0
                        except TypeError:
                            char2 = ""

                        try:
                            child['class']
                            char2 += '(W)'
                        except:
                            char2 += '(L)'
                    count += 1
                    
                try:
                    sql_entry.raw_character_entry(p1_name, char1, stage, p2_name, char2, tournament_name)
                except UnboundLocalError:
                    pass

        p1_character = '/'.join(p1_chars_used)
        p2_character = '/'.join(p2_chars_used)
        
        print(f"{p1_name}({p1_character}):{p1_score} vs. {p2_name}({p2_character}):{p2_score} \n")


if __name__ == '__main__':
    # running this program directly will proceed to scrape all known character matchups from liquipedia's site. Make sure to respect the rate limit.
    pages, tournament_names = tournament_data.links()

    user_agent = input('Enter name of the user agent the API will see (i.e. Live Score Tracker or Scrapebot 1.0)')
    email = input('Enter email to send with requests for any problems')
    for i in range(0, len(pages)-1):
    # do not lower
    time.sleep(60)
    
    try:    
        data = api_request.make_request(action='parse', page=pages[i], save_txt=False, user_agent=user_agent, email=email)
    except KeyError:
        continue
    
    print(f"tournament list number: {i}")
    scrape_characters(data, tournament_names[i])

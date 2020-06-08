
def make_request(action='parse', page=None, email="treesus14@hotmail.com"):
    import requests
    from bs4 import BeautifulSoup
    # THIS CHUNK IS USED TO CALL LIQUIPEDIA TO GET MELEE TOURNAMENTS PAGE JSON
    ###########################################################################################
    sesh = requests.Session()

    PARAMS = {
        "action": "{}".format(action),
        "page": "{}".format(page),
        "format": "json",

        "User-Agent": "Test Scraper",
        "From": "{}".format(email),  # This is another valid field
        "Accept-Encoding": "gzip"
    }

    url = "https://liquipedia.net/smash/api.php"

    response = sesh.get(url=url, params=PARAMS)
    print(response)

    data = response.json()

    print(data["parse"]["text"]["*"])
    data = data["parse"]["text"]["*"]

    name = input("what would you like to name your .txt output file (___.txt)")
    f = open("{}.txt".format(name), "w+")

    f.write(data)
    f.close()

    ################################################################################################
make_request(action="parse", page="SSBMRank")
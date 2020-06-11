
# example: make_request(action="parse", page='Low_Tier_City/6/Melee', text=False)

def make_request(action='parse', page=None, email="treesus14@hotmail.com", save_txt=False):
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
    print(response.text)

    data = response.json()
    data = data["parse"]["text"]["*"]

    if save_txt is True:
        name = raw_input('Enter a file name: (_____.txt)')
        path = "/home/trentley/PycharmProjects/smashdata/version2/{}.txt".format(name)
        f = open("{}".format(path), "w+")

        f.write(data)
        f.close()
    else:
        return data

    ################################################################################################

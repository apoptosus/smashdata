def make_request(action='parse', page=None, user_agent=None, email=None, save_txt=False):
    import requests
    from bs4 import BeautifulSoup

    sesh = requests.Session()

    # make adjustments to information you send via your request
    PARAMS = {
        "action": "{}".format(action),
        "page": "{}".format(page),
        "format": "json",
        "User-Agent": "{}".format(user_agent),
        "From": "{}".format(email), 
        "Accept-Encoding": "gzip"
    }

    url = "https://liquipedia.net/smash/api.php"

    response = sesh.get(url=url, params=PARAMS)

    data = response.json()
    data = data["parse"]["text"]["*"]

    # optionally create and store a text file at 
    if save_txt is True:
        path = raw_input('Enter a path for the file to be stored in, ending with the name of the file')
        with open("{}".format(path), "w+") as file:
            file.write(data)
            
    else:
        return data

if __name__ == '__main__':
    pass
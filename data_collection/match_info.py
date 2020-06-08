from tournament_data import tournament_links
from api_request import make_request

endpoints, hrefs = tournament_links()



def test(word):
    l = str(word) + 'goobla'
    return l


y = map(test, endpoints)

# map(make_request, 

print(list(y))
import requests


def getNews():
    url = "https://newsapi.org/v2/top-headlines?"
    secret = "134699841f36440c876edf8fb2ba6653"
    parameters = {
        # "q": "news",  # query phrase
        "pageSize": 5,  # maximum is 100
        "apiKey": secret,  # your own API key
        "searchIn": "description",
        "sortBy": "publishedAt",
        "language": "en",
        "country": "in",
    }
    response = requests.get(url, params=parameters)
    response_json = response.json()
    news = []
    articles = response_json["articles"]
    i = 1
    for article in articles:
        news.append(f"{i}. " + article["description"])
        i=i+1

    return news


# print(getNews())

# # Make the request
# response = requests.get(url, params=parameters)

# # Convert the response to
# # JSON format and pretty print it
# response_json = response.json()
# # pprint.pprint(response_json)

# news = []
# articles = response_json["articles"]
# for article in articles:
#     news.append(article["description"])

# # for i in news:
# #     print(i)

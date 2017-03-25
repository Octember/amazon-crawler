from html.parser import HTMLParser
import requests

# This URL will surely not work forever, but at the time of writing it works
AUTOCOMPLETE_URL = "https://completion.amazon.com/search/complete?method=completion&mkt=1&r=QHW0T16FVMD8GWM2WWM4&s=161-1591289-5903765&c=AWJECJG5N87M8&p=Detail&l=en_US&sv=desktop&client=amazon-search-ui&search-alias=aps&qs=&cf=1&fb=1&sc=1&q={}"

def get_autocomplete_url(keyword):
    return AUTOCOMPLETE_URL.format(keyword)


def parse_response(response):
    return response.text

def get_suggestions(keyword):
    url = get_autocomplete_url(keyword)

    response = requests.get(url)

    return parse_response(response)





print(get_suggestions('hello'))

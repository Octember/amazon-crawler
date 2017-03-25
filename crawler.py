from html.parser import HTMLParser
import requests

import pdb


# This URL will surely not work forever, but at the time of writing it works
AUTOCOMPLETE_URL = "https://completion.amazon.com/search/complete?method=completion&mkt=1&r=QHW0T16FVMD8GWM2WWM4&s=161-1591289-5903765&c=AWJECJG5N87M8&p=Detail&l=en_US&sv=desktop&client=amazon-search-ui&search-alias=aps&qs=&cf=1&fb=1&sc=1&q={}"

'''
Response payload seems to be as follows:

Array of length 3
[
    index 0 => original query string
    index 1 => Suggestions
    index 2 => List of categories (can be used for more searches) corresponding to suggestions array
]
'''

QUERY_STRING_INDEX = 0
SUGGESTIONS_INDEX  = 1
CATEGORIES_INDEX   = 2

def get_autocomplete_url(keyword):
    return AUTOCOMPLETE_URL.format( keyword)


def parse_response(response):
    if response.status_code != 200:
        print("Warning: got status code {}").format(response.status_code)
        return []

    json = response.json()

    query, suggestions, catgory_data = json[QUERY_STRING_INDEX : CATEGORIES_INDEX + 1]

    suggestions_with_categories = {}

    # pdb.set_trace()

    # Temporary assert to validate my assumptions
    assert(len(json[SUGGESTIONS_INDEX]) == len(json[CATEGORIES_INDEX]))

    for i, suggestion in enumerate(json[SUGGESTIONS_INDEX]):
        suggestions_with_categories[suggestion] = json[CATEGORIES_INDEX][i]

    return suggestions_with_categories


def get_suggestions(keyword):
    url = get_autocomplete_url(keyword)

    response = requests.get(url)

    return parse_response(response)


print(get_suggestions('hello'))

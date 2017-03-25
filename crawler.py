import requests   # HTTP requests
from collections import deque
import pdb        # debugger
import pickle     # For saving / dumping data
import signal     # For catching control+c
import sys        # handling control+c
import argparse   # Parsing arguments
import os.path

DATA_FILE_PATH = "./suggestion_data.p"
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

    query, suggestions, category_data = json[QUERY_STRING_INDEX : CATEGORIES_INDEX + 1]

    suggestions_with_categories = {}

    # pdb.set_trace()

    # Temporary assert to validate my assumptions
    assert(len(suggestions) == len(category_data))

    for i, suggestion in enumerate(suggestions):
        suggestions_with_categories[suggestion] = category_data[i]

    return suggestions_with_categories


def get_suggestions(keyword):
    url = get_autocomplete_url(keyword)

    response = requests.get(url)

    return parse_response(response)


def save_crawl_data(keyword_suggestions, tagged_categories):

    saved_data = {
        'keyword_sugggestions': keyword_suggestions,
        'tagged_categories': tagged_categories
    }

    print("Saving {} suggestions to {}".format(len(keyword_suggestions), DATA_FILE_PATH))
    pickle.dump( saved_data, open( DATA_FILE_PATH, "wb" ) )


def crawl_amazon(limit):

    keyword_suggestions = {}
    tagged_categories   = {}

    # Handler to catch control+C and save our progress anyway
    def signal_handler(signal, frame):
        print('Saving your data and quitting')
        save_crawl_data(keyword_suggestions, tagged_categories)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print('Welcome -- About to crawl {} keywords from amazon suggestions'.format(limit))
    print('Press Ctrl+C whenever, your data will be saved\n')

    words_to_use = set()
    for line in open('./simple_words.txt', 'r'):
        words_to_use.add(line.strip())

    keyword_queue = deque(words_to_use)

    while len(keyword_queue) != 0 and len(keyword_suggestions) < limit:

        keyword = keyword_queue.popleft()

        suggestions_and_categories = get_suggestions(keyword)

        suggestion_list = set(suggestions_and_categories.keys())

        keyword_suggestions[keyword] = suggestion_list

        # Now enqueue new potential keywords
        for suggestion in suggestion_list:
            if suggestion not in words_to_use:
                words_to_use.add(suggestion)
                keyword_queue.append(suggestion)
                # print("Enqueued '{}'".format(suggestion))

        print("Queue size: {}\t\t{}:\t{} suggestions".format(len(keyword_queue), keyword, len(suggestion_list)))

    save_crawl_data(keyword_suggestions, tagged_categories)


def query_data():
    if not os.path.isfile(DATA_FILE_PATH):
        raise ValueError("Data file not ready; run `python crawler.py crawl` before querying")




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="'crawl' to crawl amazon, 'query' to enter interactive CLI based on previous crawl")
    parser.add_argument("--limit", type=int, help="Limit total number of suggestions to query. Defaults to 100", default=100)
    args = parser.parse_args()

    if args.action == 'crawl':
        limit = args.limit
        crawl_amazon(limit)
    elif args.action == 'query':
        query_data()
    else:
        raise ValueError("Invalid action, use 'crawl' or 'query'")

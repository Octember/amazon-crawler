

Write a simple web crawler that grabs search suggestion data from the amazon.com search bar


## Installation

```
# Install python v > 3.0 https://www.python.org/downloads/release/python-361/

pip install requests
```

## Usage

There are two steps to using the crawler:

1. Run the script to save a dump of from amazon.com suggestion data

```
python crawler.py crawl
```

The script will continue to run until it has exhausted a huge (dynamically increasing)
list of keywords, so feel free to stop it using control+C at any point. The script
will save the crawled data at that point. The data will be saved to `suggestion_data.p`

2. Reading the data
python3 crawler.py query

## Planning

### Generating list of keywords to search on

* Use simple dictionary
* Supplement list of keywords with returned results as known things to search for
** Worth noting that this strategy quickly explodes the number of searches.
This is ideal for a comprehensive crawler, but very slow for a quick script
* Use random letters


### Data storage scheme

Map of keyword => list of suggestions

Separate map of category -> suggestions in that category



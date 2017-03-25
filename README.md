

## Write a simple web crawler that grabs search suggestion data from the amazon.com search bar


### Installation

```
# Install python v > 3.0

pip install requests

python crawler.py

```

### Generating list of keywords to search on

* Use simple dictionary
* Supplement list of keywords with returned results as known things to search for
** Worth noting that this strategy quickly explodes the number of searches.
This is ideal for a comprehensive crawler, but very slow for a quick script
* Use random letters


### Data storage scheme

Map of keyword => list of suggestions

Separate map of category -> suggestions in that category

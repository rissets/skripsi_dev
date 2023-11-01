# filename: arxiv_search.py
import requests

def search_arxiv(query):
    url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': query,
        'start': 0,
        'max_results': 5,
        'sortBy': 'relevance',
        'sortOrder': 'descending'
    }
    response = requests.get(url, params=params)
    return response.text

query = 'fine-tuning large language model bahasa alami'
response = search_arxiv(query)
print(response)
from hestia_earth.schema import Bibliography
import requests

from hestia_earth.extend_bibliography.bibliography_apis.utils import ORINGAL_FIELD, extend_bibliography


API_URL = 'https://api.clarivate.com/api/pubmatch'
API_FIELDS = ['title', 'isbn', 'doi', 'issn', 'issue', 'volume', 'year']


class RestClient():
    def __init__(self, api_key):
        self.api_key = api_key

    def __enter__(self):
        return self.api_key

    def __exit__(self, _a, _b, _c):
        return False


def int_value(x): return int(x) if x and int(x) > 0 else None


def api_url(): return f"{API_URL}?fields={','.join(API_FIELDS)}"


def api_headers(api_key=''):
    return {
        'Content-type': 'application/json',
        'X-ApiKey': api_key
    }


def item_to_bibliography(item: dict):
    page_start = item.get('startPage')
    page_end = item.get('endPage')

    return {
        'title': item.get('title'),
        'year': item.get('year'),
        'documentDOI': item.get('doi'),
        'volume': int_value(item.get('volume')),
        'issue': item.get('issue', '0').split('-')[0],
        'pages': f"{page_start}-{page_end}" if page_start and page_end else None
    }


def create_biblio(title: str, item: dict):
    biblio = Bibliography()
    # save title here since closest item might differ
    biblio.fields[ORINGAL_FIELD + 'title'] = title
    biblio.fields['title'] = title
    bibliography = item_to_bibliography(item) if item else {}
    (extended_biblio, _a) = extend_bibliography([], bibliography['year']) if item else ({}, [])
    return (
        {**biblio.to_dict(), **bibliography, **extended_biblio},
        []
    ) if item else (biblio.to_dict(), [])


def exec_search(api_key: str):
    def search(title: str):
        data = {'matchRequest': [{'title': title}]}
        response = requests.post(API_URL, data=data, headers=api_headers(api_key)).json().get('data')
        items = response.get('matchResponse')[0].get('matches') if response else []
        return list(map(lambda x: {'title': x['title'], 'item': x}, items))
    return search


def get_client(**kwargs): return RestClient(kwargs.get('wos_api_key'))

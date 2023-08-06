from wos import WosClient
import wos.utils
import xmltodict
import re
from hestia_earth.schema import Bibliography

from hestia_earth.extend_bibliography.bibliography_apis.utils import ORINGAL_FIELD, extend_bibliography


def int_value(x): return int(x) if x and int(x) > 0 else None


def author_to_actor(author: str):
    [last, first] = author.split(', ')
    return {
        'firstName': first,
        'lastName': last
    }


def item_to_bibliography(item: dict):
    values = item['source'] + item['other']

    def label_value(label: str, default=None):
        return next((x['value'] for x in values if x['label'] == label), default)

    return {
        'title': item['title']['value'],
        'year': int_value(label_value('Published.BiblioYear', 0)),
        'documentDOI': label_value('Identifier.Doi'),
        'volume': int_value(label_value('Volume')),
        'issue': label_value('Issue', '0').split('-')[0],
        'pages': label_value('Pages'),
        'outlet': label_value('SourceTitle')
    }


def create_biblio(title: str, item: dict):
    biblio = Bibliography()
    # save title here since closest item might differ
    biblio.fields[ORINGAL_FIELD + 'title'] = title
    biblio.fields['title'] = title
    authors = list(map(author_to_actor, item.get('authors')['value'] if item else []))
    bibliography = item_to_bibliography(item) if item else {}
    (extended_biblio, actors) = extend_bibliography(authors, bibliography['year']) if item else ({}, [])
    return (
        {**biblio.to_dict(), **bibliography, **extended_biblio},
        actors
    ) if item else (biblio.to_dict(), [])


def search_query(title: str): return f"TI=({re.sub(r'[(:]{1}.*', '', title)[:50].rstrip()})"


def exec_search(client: WosClient):
    def search(title: str):
        result = xmltodict.parse(wos.utils.query(client, search_query(title)))['return']
        items = result['records'] if 'records' in result else []
        items = [items] if isinstance(items, dict) else items
        return list(map(lambda x: {'title': x['title']['value'], 'item': x}, items))
    return search


def get_client(**kwargs):
    api_user = kwargs.get('wos_api_user')
    api_password = kwargs.get('wos_api_pwd')
    return WosClient(user=api_user, password=api_password, lite=True)

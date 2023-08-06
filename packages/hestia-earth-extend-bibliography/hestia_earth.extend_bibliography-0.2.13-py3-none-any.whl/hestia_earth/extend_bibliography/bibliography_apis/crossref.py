import traceback
from concurrent.futures import ThreadPoolExecutor
from hestia_earth.schema import Bibliography, BibliographyDocumentType
import habanero

from .utils import ORINGAL_FIELD, current_time, MAXIMUM_DISTANCE, find_closest_result, extend_bibliography, \
    remove_empty_values


TYPE_TO_DOCUMENT_TYPE = {
    'journal-article': BibliographyDocumentType.JOURNAL.value
}


def author_to_actor(author):
    return {
        'firstName': author['given'],
        'lastName': author['family']
    }


def clean_abstract(abstract: str):
    return abstract.replace('<jats:p>', '').replace('</jats:p>', '').strip() if abstract else None


def item_to_bibliography(item):
    document_type = item.get('type')
    document_type = TYPE_TO_DOCUMENT_TYPE.get(document_type) if document_type else document_type
    outlet = item.get('short-container-title')
    return {
        'title': item.get('title')[0],
        'year': item.get('issued').get('date-parts')[0][0],
        'documentType': document_type,
        'outlet': outlet[0] if outlet and len(outlet) > 0 else None,
        'abstract': clean_abstract(item.get('abstract')),
        'documentDOI': item.get('DOI')
    }


def create_biblio(title: str, item: dict):
    biblio = Bibliography()
    # save title here since closest item might differ
    biblio.fields[ORINGAL_FIELD + 'title'] = title
    biblio.fields['title'] = title
    authors = list(map(author_to_actor, item['author'] if item else []))
    bibliography = item_to_bibliography(item) if item else {}
    (extended_biblio, actors) = extend_bibliography(authors, bibliography['year']) if item else ({}, [])
    return (
        {**biblio.to_dict(), **bibliography, **extended_biblio},
        actors
    ) if item else (biblio.to_dict(), [])


def exec_search(cr):
    def search(title: str):
        items = cr.works(query=title)['message']['items']
        return list(map(lambda x: {'title': x['title'][0], 'item': x}, items))
    return search


def search(cr, title):
    [item, distance] = find_closest_result(title, exec_search(cr))
    return create_biblio(title, item if distance <= MAXIMUM_DISTANCE else None)


def extend_title(cr, bibliographies, actors):
    def extend(title: str):
        now = current_time()
        (biblio, authors) = search(cr, title)
        bibliographies.extend([] if biblio is None else [biblio])
        actors.extend([] if authors is None else authors)
        print('crossref', 'find title', current_time() - now, title)
    return extend


def extend_crossref(titles, **kwargs):
    try:
        cr = habanero.Crossref()

        bibliographies = []
        actors = []

        max_workers = kwargs.get('max_workers', 1)
        extender = extend_title(cr, bibliographies, actors)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(extender, titles)

        return (remove_empty_values(actors), remove_empty_values(bibliographies))
    except Exception:
        print(traceback.format_exc())
        return ([], [])

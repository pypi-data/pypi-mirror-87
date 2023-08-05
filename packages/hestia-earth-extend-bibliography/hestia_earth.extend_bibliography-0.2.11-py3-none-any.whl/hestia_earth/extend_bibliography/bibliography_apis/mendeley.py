import traceback
from concurrent.futures import ThreadPoolExecutor
from hestia_earth.schema import Bibliography
from mendeley import Mendeley

from .utils import ORINGAL_FIELD, current_time, MAXIMUM_DISTANCE, find_closest_result, remove_empty_values, \
    extend_bibliography


def author_to_actor(author):
    return {
        'firstName': author.first_name,
        'lastName': author.last_name,
        'scopusID': author.scopus_author_id
    }


def citation_to_bibliography(citation):
    has_identifiers = citation and citation.identifiers is not None
    doi = citation.identifiers['doi'] if has_identifiers and 'doi' in citation.identifiers else None
    scopus = citation.identifiers['scopus'] if has_identifiers and 'scopus' in citation.identifiers else None
    return {
        'title': citation.title,
        'year': citation.year,
        'documentType': citation.type,
        'outlet': citation.source,
        'mendeleyID': citation.id,
        'abstract': citation.abstract,
        'documentDOI': doi,
        'scopus': scopus
    }


def create_biblio(citation, key: str, value: str):
    biblio = Bibliography()
    # save title here since closest citation might differ
    biblio.fields[ORINGAL_FIELD + key] = value if citation else None
    biblio.fields[key] = value
    authors = list(map(author_to_actor, citation.authors if citation else []))
    bibliography = citation_to_bibliography(citation) if citation else {}
    (extended_biblio, actors) = extend_bibliography(authors, citation.year) if citation else ({}, [])
    return (
        {**biblio.to_dict(), **bibliography, **extended_biblio},
        actors
    ) if citation else (biblio.to_dict(), [])


def exec_search_by_title(session, title: str):
    def search(value: str):
        items = session.catalog.search(value.rstrip(), view='all').list(50).items
        # try a search with shorter value if no results found
        items = items if len(items) > 0 else session.catalog.search(value[:100].rstrip(), view='all').list(50).items
        return list(map(lambda x: {'title': x.title, 'item': x}, items))

    [citation, distance] = find_closest_result(title, search)
    return create_biblio(citation if distance <= MAXIMUM_DISTANCE else None, 'title', title)


def exec_search_by_id(session, value: str):
    item = session.catalog.get(value.rstrip(), view='all')
    return create_biblio(item, 'mendeleyID', value)


def exec_search_by_documentDOI(session, value: str):
    item = session.catalog.by_identifier(doi=value.rstrip(), view='all')
    return create_biblio(item, 'documentDOI', value)


def exec_search_by_scopus(session, value: str):
    item = session.catalog.by_identifier(scopus=value.rstrip(), view='all')
    return create_biblio(item, 'scopus', value)


SEARCH_BY_KEY = {
    'title': exec_search_by_title,
    'mendeleyID': exec_search_by_id,
    'documentDOI': exec_search_by_documentDOI,
    'scopus': exec_search_by_scopus
}


def exec_extend(session, key: str, bibliographies, actors):
    def extend(value: str):
        now = current_time()
        (biblio, authors) = SEARCH_BY_KEY[key](session, value)
        print('mendeley', 'find by', key, current_time() - now, value)
        bibliographies.extend([] if biblio is None else [biblio])
        actors.extend([] if authors is None else authors)
    return extend


def extend_mendeley(values, key='title', **kwargs):
    try:
        mendel = Mendeley(client_id=int(kwargs.get('mendeley_username')), client_secret=kwargs.get('mendeley_password'))
        auth = mendel.start_client_credentials_flow()
        session = auth.authenticate()

        bibliographies = []
        actors = []

        max_workers = kwargs.get('max_workers', 1)
        extender = exec_extend(session, key, bibliographies, actors)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(extender, values)

        return (remove_empty_values(actors), remove_empty_values(bibliographies))
    except Exception:
        print(traceback.format_exc())
        return ([], [])

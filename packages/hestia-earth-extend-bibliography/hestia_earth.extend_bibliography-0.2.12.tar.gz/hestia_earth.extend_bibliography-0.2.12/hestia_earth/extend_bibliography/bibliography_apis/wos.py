import traceback
from concurrent.futures import ThreadPoolExecutor

from .utils import current_time, has_key, MAXIMUM_DISTANCE, find_closest_result, remove_empty_values
import hestia_earth.extend_bibliography.bibliography_apis.wos_rest.client as wos_rest_client
import hestia_earth.extend_bibliography.bibliography_apis.wos_soap.client as wos_soap_client


def extend_title(wos_client, searcher, bibliographies, actors):
    def extend(title: str):
        now = current_time()
        [item, distance] = find_closest_result(title, searcher)
        print('wos', 'find title', current_time() - now, title)
        (biblio, authors) = wos_client.create_biblio(title, item if distance <= MAXIMUM_DISTANCE else None)
        bibliographies.extend([] if biblio is None else [biblio])
        actors.extend([] if authors is None else authors)
    return extend


def extend_wos(titles, **kwargs):
    try:
        wos_client = wos_rest_client if has_key('wos_api_key', **kwargs) else wos_soap_client
        max_workers = kwargs.get('max_workers', 1)

        bibliographies = []
        actors = []

        with wos_client.get_client(**kwargs) as client:
            extender = extend_title(wos_client, wos_client.exec_search(client), bibliographies, actors)
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                executor.map(extender, titles)

        return (remove_empty_values(actors), remove_empty_values(bibliographies))
    except Exception:
        print(traceback.format_exc())
        return ([], [])

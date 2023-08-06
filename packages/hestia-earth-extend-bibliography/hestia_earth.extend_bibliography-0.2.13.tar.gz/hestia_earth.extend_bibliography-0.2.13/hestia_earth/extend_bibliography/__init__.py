from pkgutil import extend_path
from functools import reduce
from hestia_earth.schema import SchemaType, Bibliography

from .bibliography_apis.utils import ORINGAL_FIELD, has_key, is_enabled, unique_values, biblio_name, actor_name
from .bibliography_apis.crossref import extend_crossref
from .bibliography_apis.mendeley import extend_mendeley
from .bibliography_apis.wos import extend_wos


__path__ = extend_path(__path__, __name__)

DEFAULT_KEY = 'title'


def is_node_of(node_type: SchemaType): return lambda node: node.get('type') == node_type.value


def source_name_from_biblio(biblio: dict):
    name = biblio.get('name', '')
    return name if name is not None and len(name) > 0 else biblio.get('title', '')


def update_source_from_biblios(source: dict, bibliographies: list, nkey=DEFAULT_KEY):
    def update_key(key: str):
        value = source.get(key)
        biblio = next((x for x in bibliographies if value and value.get(nkey, '') == x.get(ORINGAL_FIELD + nkey)), None)
        if biblio:
            source[key] = {**source[key], **biblio}
            del source[key][ORINGAL_FIELD + nkey]

            name = source_name_from_biblio(biblio)
            if key == 'bibliography' and len(name) > 0:
                source['name'] = name

    update_key('bibliography')
    update_key('metaAnalysisBibliography')
    return source


def need_update_source(node: dict, nkey=DEFAULT_KEY):
    def has_nkey(key: str): return key in node and nkey in node.get(key)

    return has_nkey('bibliography') or has_nkey('metaAnalysisBibliography')


def update_sources(bibliographies: list, key=DEFAULT_KEY):
    def update_single_source(source: dict):
        return update_source_from_biblios(source, bibliographies, key) if need_update_source(source, key) else source
    return update_single_source


def map_author_from_nodes(authors: list):
    def map_author(actor: dict):
        actor_name = actor.get('firstName')
        return actor if actor_name else next((x for x in authors if x.get('id', '-1') == actor.get('id', '0')), actor)
    return map_author


def update_biblio(node: dict, authors: list):
    # authors might be in bibliography or in top-level authors
    authors = list(map(map_author_from_nodes(authors), node.get('authors')))
    name = biblio_name(authors, node.get('year'))
    return {**node, **{'name': name if name else node.get('name')}}


def update_actor(node: dict, *args):
    name = actor_name(node)
    if name:
        node['name'] = name
    return node


def update_source(node: dict, *args):
    biblio = node.get('bibliography')
    if biblio:
        name = source_name_from_biblio(biblio)
        if len(name) > 0:
            node['name'] = name
    return node


UPDATE_NODE_TYPE = {
    SchemaType.ACTOR.value: update_actor,
    SchemaType.BIBLIOGRAPHY.value: update_biblio,
    SchemaType.SOURCE.value: update_source,
}


def update_node_list(authors, node: list): return list(reduce(lambda p, x: p + [update_node(authors)(x)], node, []))


def update_node_dict(authors, node: dict):
    node_type = node.get('type')
    node = UPDATE_NODE_TYPE[node_type](node, authors) if node_type in UPDATE_NODE_TYPE else node
    for key, value in node.items():
        node[key] = update_node(authors)(value)
    return node


def update_node(authors: list):
    def update(node):
        if isinstance(node, list):
            return update_node_list(authors, node)
        elif isinstance(node, dict):
            return update_node_dict(authors, node)
        return node
    return update


def has_node_value(node: dict):
    def has_value(key: str):
        value = node.get(key)
        if isinstance(value, str) or isinstance(value, list):
            return len(value) > 0
        if isinstance(value, int):
            return value > 0
        return value is not None
    return has_value


def get_biblio_value(node: dict, key: str):
    # name can be created from authors, therefore if authors not empty name can be skipped
    def can_compute_name(): return len(node.get('name', '')) > 0 or len(node.get('authors', [])) > 0

    required = Bibliography().required
    required_values = list(filter(has_node_value(node), required))
    required_values.extend(['name'] if 'name' not in required_values and can_compute_name() else [])
    value = node.get(key, '')
    return value if len(value) > 0 and len(required_values) != len(required) else None


def get_values_from_node(node: dict, key: str):
    value = get_biblio_value(node, key) if is_node_of(SchemaType.BIBLIOGRAPHY)(node) else None
    return list(set(reduce(lambda x, y: x + get_node_values(y, key), node.values(), [] if value is None else [value])))


def get_node_values(nodes, key=DEFAULT_KEY):
    if isinstance(nodes, list):
        return list(set(reduce(lambda p, x: p + get_node_values(x, key), nodes, [])))
    elif isinstance(nodes, dict):
        return get_values_from_node(nodes, key)
    else:
        return []


def extend(content, **kwargs):
    nodes = content.get('nodes') if 'nodes' in content else []

    actors = []
    sources = list(filter(is_node_of(SchemaType.SOURCE), nodes))

    if has_key('mendeley_username', **kwargs):
        key = DEFAULT_KEY
        (authors, bibliographies) = extend_mendeley(sorted(get_node_values(sources, key)), key, **kwargs)
        actors.extend([] if authors is None else authors)
        list(map(update_sources(bibliographies, key), sources))

        key = 'mendeleyID'
        (authors, bibliographies) = extend_mendeley(sorted(get_node_values(sources, key)), key, **kwargs)
        actors.extend([] if authors is None else authors)
        list(map(update_sources(bibliographies, key), sources))

        key = 'documentDOI'
        (authors, bibliographies) = extend_mendeley(sorted(get_node_values(sources, key)), key, **kwargs)
        actors.extend([] if authors is None else authors)
        list(map(update_sources(bibliographies, key), sources))

        key = 'scopus'
        (authors, bibliographies) = extend_mendeley(sorted(get_node_values(sources, key)), key, **kwargs)
        actors.extend([] if authors is None else authors)
        list(map(update_sources(bibliographies, key), sources))

    if has_key('wos_api_key', **kwargs) or (has_key('wos_api_user', **kwargs) and has_key('wos_api_pwd', **kwargs)):
        (authors, bibliographies) = extend_wos(sorted(get_node_values(sources)), **kwargs)
        actors.extend([] if authors is None else authors)
        list(map(update_sources(bibliographies), sources))

    if is_enabled('enable_crossref', **kwargs):
        (authors, bibliographies) = extend_crossref(sorted(get_node_values(sources)), **kwargs)
        actors.extend([] if authors is None else authors)
        list(map(update_sources(bibliographies), sources))

    authors = list(filter(is_node_of(SchemaType.ACTOR), nodes))
    # update all nodes except sources
    nodes = list(map(update_node(authors), nodes))
    # TODO: find a better way, because of children we need to run twice for parents to have correct values
    nodes = list(map(update_node(authors), nodes))

    return {'nodes': unique_values(actors) + nodes}

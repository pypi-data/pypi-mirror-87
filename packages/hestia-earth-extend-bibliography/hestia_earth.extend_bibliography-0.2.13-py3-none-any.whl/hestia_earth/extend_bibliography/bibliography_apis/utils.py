from random import randint
import Levenshtein
import time
from hestia_earth.schema import Actor


MAXIMUM_DISTANCE = 10
ORINGAL_FIELD = 'original'


def current_time(): return int(round(time.time() * 1000))


def has_key(key: str, **kwargs): return kwargs.get(key, None) is not None


def is_enabled(key: str, **kwargs): return kwargs.get(key, False) is True


def join_list_string(values): return ' '.join(list(filter(non_empty_value, values))).strip()


def non_empty_value(value): return value != '' and value is not None and value != []


def remove_empty_values(values): return list(map(lambda x: {k: v for k, v in x.items() if non_empty_value(v)}, values))


def unique_values(values: list, key='id'): return list({v[key]: v for v in values}.values())


def actor_id(author):
    return author.get('scopusID') if 'scopusID' in author and author.get('scopusID') \
        else f"H-{str(randint(10**9, 10**10-1))}"


def actor_name(actor: dict):
    name = actor.get('name', '')
    first_name = actor.get('firstName')
    last_name = actor.get('lastName')
    computed_name = join_list_string([
        first_name[0] if first_name else None, last_name, actor.get('primaryInstitution')
    ]) if last_name else ''
    return name if len(name) > 0 else computed_name


def biblio_name(authors: list, year=None):
    if authors and len(authors) > 0 and authors[0].get('lastName'):
        author_suffix = ''

        if len(authors) == 2 and authors[1].get('lastName'):
            author_suffix = f"& {authors[1].get('lastName')}"
        elif len(authors) >= 3:
            author_suffix = 'et al'

        return join_list_string([authors[0].get('lastName'), author_suffix, f"({str(year)})" if year else None])
    return ''


def create_actors(actors):
    def create_actor(author):
        actor = Actor()
        actor.fields = {**actor.fields, **author}
        actor.fields['id'] = actor_id(author)
        actor.fields['name'] = actor_name(actor.fields)
        actors.append(actor.to_dict())

        author = Actor()
        author.fields['id'] = actor.fields.get('id')
        return remove_empty_values([author.to_dict()])[0]
    return create_actor


def extend_bibliography(authors=[], year=None):
    biblio = {}
    actors = []
    biblio['authors'] = list(map(create_actors(actors), authors))
    biblio['name'] = biblio_name(authors, year)
    return (biblio, actors)


def get_distance(str1: str, str2: str):
    return Levenshtein.distance(str1.rstrip().lower(), str2.rstrip().lower())


def find_closest_result(title: str, fetch_items):
    items = fetch_items(title)
    distances = list(map(lambda i: get_distance(title, i['title']), items))
    distance = min(distances) if len(distances) else 1000
    closest_title = items[distances.index(distance)]['item'] if len(distances) else None
    return [closest_title, distance]

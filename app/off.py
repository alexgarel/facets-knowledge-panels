from collections import namedtuple
from urllib.parse import urljoin

import requests

from .i18n import DEFAULT_LANGUAGE, get_current_lang
from .i18n import translate as _
from .wikidata_utils import get_wikidata_entity, wikidata_props


def data_quality(url, path):
    """
    Helper function to return issues for data-quality
    """
    source_url = urljoin(url, path)
    quality_url = f"{source_url}/data-quality.json"
    response_API = requests.get(quality_url)
    data = response_API.json()
    total_issues = data["count"]
    tags = data["tags"]
    html = []
    for tag in tags[0:3]:
        info = {
            "products": tag["products"],
            "name": tag["name"],
        }
        html.append(f'<li><a href={tag["url"]}>')
        html.append(_("{products} products with {name}").format(**info))
        html.append("</a></li>")

    html = (
        [
            "<ul><p>",
            _("The total number of issues are {total_issues}").format(total_issues=total_issues),
            "</p>",
        ]
        + html
        + ["</ul>"]
    )
    text = "".join(html)
    description = _("Data-quality issues related to")
    title = _("Data-quality issues")

    return text, source_url, description, title


def last_edit(url, query):
    """
    Helper function to return data for last-edits
    """
    search_url = f"{url}/api/v2/search"
    response_API = requests.get(search_url, params=query)
    data = response_API.json()
    counts = data["count"]
    tags = data["products"]

    html = []
    for tag in tags[0:10]:
        info = {
            "product_name": tag.get("product_name", ""),
            "code": tag["code"],
            "last_editor": tag.get("last_editor", ""),
            "edit_date": tag["last_edit_dates_tags"][0],
        }
        html.append("<li>")
        html.append(
            _("{product_name} ({code}) edited by {last_editor} on {edit_date}").format(**info)
        )
        html.append("</li>")
    html = (
        [
            "<ul><p>",
            _("Total number of edits {counts}").format(counts=counts),
            "</p>",
        ]
        + html
        + ["</ul>"]
    )
    text = "".join(html)
    description = _("last-edits issues related to")
    title = _("Last-edits")
    return text, description, title


Entities = namedtuple(
    "Entities",
    [
        "label_tag",
        "description_tag",
        "image_url",
        "entity_id",
        "OSM_relation",
        "INAO_relation",
        "wikipedia_relation",
    ],
)


def in_lang(data, lang, suffix=""):
    """retrieve an entry where key is lang + suffix
    with an eventual fallback to DEFAULT_LANGUAGE
    """
    try:
        return data[lang + suffix]
    except KeyError:
        if lang == DEFAULT_LANGUAGE:
            raise
        return data[DEFAULT_LANGUAGE + suffix]


def wikidata_helper(query, value):
    """
    Helper function to return wikidata eg:label,description,image_url
    """
    lang = get_current_lang()
    url = "https://world.openfoodfacts.org/api/v2/taxonomy"
    response_API = requests.get(url, params=query)
    data = response_API.json()
    tag = data[value]
    entity_id = in_lang(tag["wikidata"], lang)
    entity = get_wikidata_entity(entity_id=entity_id)
    if wikidata_props.image_prop in entity:
        image = entity[wikidata_props.image_prop]
        image_url = image.image_url
    else:
        image_url = ""
    wiki_links = in_lang(entity.attributes["sitelinks"], lang, "wiki")
    wikipedia_relation = wiki_links.get("url")
    if wikidata_props.INAO_prop in entity:
        INAO = entity[wikidata_props.INAO_prop]
        INAO_relation = "https://www.inao.gouv.fr/produit/{}".format(INAO)
    else:
        INAO_relation = ""
    if wikidata_props.OSM_prop in entity:
        osm = entity[wikidata_props.OSM_prop]
        OSM_relation = "https://www.openstreetmap.org/relation/{}".format(osm)
    else:
        OSM_relation = ""
    entities = Entities(
        in_lang(entity.label, lang),
        in_lang(entity.description, lang),
        image_url,
        entity_id,
        OSM_relation,
        INAO_relation,
        wikipedia_relation,
    )
    return entities


def hungergame():
    """Helper function for making Translation easy"""
    description = _("Answer robotoff questions about")
    return description

from typing import Union
from urllib.parse import urlencode
from .models import HungerGameFilter, country_to_ISO_code, facet_plural
from .off import data_quality, last_edit, wikidata


def hunger_game_kp(
    hunger_game_filter: HungerGameFilter,
    value: Union[str, None] = None,
    country: Union[str, None] = None,
):
    query = {}
    description = ""
    if hunger_game_filter == "country":
        country = value
        hunger_game_filter = value = None
    if country is not None:
        query["country"] = country
        description = country
    if hunger_game_filter is not None:
        query["type"] = f"{hunger_game_filter}"
        description = f"{hunger_game_filter}"
    if value is not None:
        query["value_tag"] = value
        description = f"{value} {hunger_game_filter}"
    questions_url = "https://hunger.openfoodfacts.org/questions"
    if query:
        questions_url += f"?{urlencode(query)}"
    description = f"Answer robotoff questions about {description}"
    html = f"<p><a href='{questions_url}'>{description}</a></p>\n"
    return {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {"html": str(html)},
                },
            ],
        },
    }


def data_quality_kp(
    facet,
    value: Union[str, None] = None,
    country: Union[str, None] = None,
):
    """
    Get data corresponding to differnet facet
    """
    path = ""
    description = ""
    if facet == "country":
        country = value
        country_code = country_to_ISO_code(value=value)
        url = f"https://{country_code}-en.openfoodfacts.org"
        path = ""
        facet = value = None
    if country is not None:
        country_code = country_to_ISO_code(value=country)
        url = f"https://{country_code}-en.openfoodfacts.org"
        path = ""
        description += country
    if country is None:
        url = "https://world.openfoodfacts.org/"
    if facet is not None:
        path += facet
        description += f"{facet}"
    if value is not None:
        path += f"/{value}"
        description += f" {value}"
    description = f"Data-quality issues related to {description}"
    (quality_html, source_url) = data_quality(url=url, path=path)

    return {
        "Quality": {
            "title": "Data-quality issues",
            "subtitle": f"{description}",
            "source_url": f"{source_url}/data-quality",
            "elements": [
                {
                    "element_type": "text",
                    "text_element": quality_html,
                }
            ],
        },
    }


def last_edits_kp(
    facet: str,
    value: Union[str, None] = None,
    country: Union[str, None] = None,
):
    """
    Return knowledge panel for last-edits corresponding to different facet
    """
    query = {
        "fields": "product_name,code,last_editor,last_edit_dates_tags",
        "sort_by": "last_modified_t",
    }
    description = ""
    if facet == "country":
        country = value
        country_code = country_to_ISO_code(value=value)
        url = f"https://{country_code}-en.openfoodfacts.org"
        facet = value = None
    if country is not None:
        country_code = country_to_ISO_code(value=country)
        url = f"https://{country_code}-en.openfoodfacts.org"
        description += country
    if country is None:
        url = "https://world.openfoodfacts.org"
    if facet is not None:
        description += f" {facet}"
    if value is not None:
        query[f"{facet_plural(facet=facet)}_tags_en"] = value
        description += f" {value}"
    description = f"last-edits issues related to {description}"
    expected_html = last_edit(url=url, query=query)

    return {
        "LastEdits": {
            "title": "Last-edites",
            "subtitle": f"{description}",
            "source_url": f"{url}/{facet}/{value}?sort_by=last_modified_t",
            "elements": [
                {
                    "element_type": "text",
                    "text_element": expected_html,
                },
            ],
        },
    }


def wikidata_kp(facet: str, value: str):
    query = {}
    if value:
        query["tagtype"] = facet
        query["fields"] = "name,parents,wikidata,origins"
        query["tags"] = value
    wiki = wikidata(query=query, value=value)

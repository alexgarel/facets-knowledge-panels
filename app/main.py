from typing import Union
import logging
from fastapi import FastAPI, HTTPException

from .knowledge_panels import hunger_game_kp, last_edits_kp
from .models import FacetName, HungerGameFilter

app = FastAPI()


@app.get("/")
def hello():
    return {
        "message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"
    }


@app.get("/knowledge_panel")
def knowledge_panel(
    facet_name: FacetName,
    facet_value: Union[str, None] = None,
    country: Union[str, None] = None,
):
    # FacetName is the model that have list of values
    # facet_value are the list of values connecting to FacetName eg:- category/beer, here beer is the value
    panels = []
    """
    Appending hunger-game-knowledge-panel
    """
    if facet_name in HungerGameFilter.list():
        panels.append(
            hunger_game_kp(
                hunger_game_filter=facet_name, value=facet_value, country=country
            )
        )

    """Appending last-edits-knowledge-panel"""
    try:
        panels.append(
            last_edits_kp(facet=facet_name, value=facet_value, country=country)
        )
    except Exception as Argument:
        logging.exception("error occued while appending last-edits-kp")

    return {"knowledge_panels": panels}

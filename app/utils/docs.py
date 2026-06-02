# region Docs
"""
FastAPI doc variables

Decluttering main.py by moving mappings to dedicated module

Variables:
    DESCRIPTION (str): Description of FastAPI definitions.
    TAGS (str): Mapping of endpoints by tag

"""
# endregion

DESCRIPTION = """
# Sections
## Integrations
The first set of tags are around interacting with the integrations.

## Operational
This set of tags is split by actions. Get, Upsert, or Delete

## Core
This set is for the core functionality of the app.
"""

TAGS = [
    {
        "name": "traggo",
        "description": "Endpoints for Traggo logging",
        "externalDocs": {
            "description": "Traggo docs",
            "url": "https://traggo.net/terminology/",
        },
    },
    {
        "name": "super-productivity",
        "description": "Endpoints for Super Productivity automation",
    },
    {
        "name": "anytype",
        "description": "Endpoints for anytype interaction",
        "externalDocs": {
            "description": "Anytype API docs",
            "url": "https://developers.anytype.io/docs/reference",
        },
    },
    {
        "name": "get",
        "description": "Endpoints for fetching objects",
    },
    {
        "name": "upsert",
        "description": "Endpoints for creating or updating objects",
    },
    {
        "name": "delete",
        "description": "Endpoints for deleting objects",
    },
    {
        "name": "data",
        "description": "Endpoints for interacting with the mongo database",
    },
    {"name": "general", "description": "Endpoints for general use"},
    {"name": "scheduled", "description": "Which endpoints are also scheduled jobs"},
]

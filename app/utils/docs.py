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
### Sections
"""

TAGS = [
    {"name": "general", "description": "Endpoints for general use"},
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
    {"name": "scheduled", "description": "Which endpoints are also scheduled jobs"},
    {
        "name": "anytype",
        "description": "Endpoints for anytype interaction",
        "externalDocs": {
            "description": "Anytype API docs",
            "url": "https://developers.anytype.io/docs/reference",
        },
    },
]

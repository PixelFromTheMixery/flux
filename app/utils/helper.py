# region Docs
"""
Module for managing non-specific methods

Helper can be called by anything due to no dependencies

Classes:
    Helper: Encapsulating class

TODO: Move deeplink to anytype utils when ready
"""
# endregion


def transformer(model) -> dict:
    # region Docs
    """
    Gets an pydantic object and transforms it into a dict

    Args:
        model (pydanticObject): self explanatory

    Returns:
        dict: full matching entry from model
    """
    # endregion

    result = model.model_dump()
    result["id"] = str(result["id"])
    return result

"""
Module for managing non-specific methods

Helper can be called by anything due to no dependencies

Classes:
    Helper: Encapsulating class

TODO: Move deeplink to anytype utils when ready
"""


class Helper:
    """
    Shared methods dump
    """

    def make_deeplink(self, space_id: str, object_id: str):
        """Builds deeplinks for link purposes"""
        return f"anytype://object?objectId={object_id}&spaceId={space_id}"

# region Docs
"""
Module for managing non-specific methods

Helper can be called by anything due to no dependencies

Classes:
    Helper: Encapsulating class

TODO: Move deeplink to anytype utils when ready
"""
# endregion


class Helper:
    # region Docs
    """
    Shared methods dump
    """

    # endregion

    def make_deeplink(self, space_id: str, object_id: str):
        # region Docs
        """
        Generates an anytype link that brings you directly to the app

        Args:
            space_id (str): Anytype Space ID
            object_id (str): Anytype Object ID within a space

        Returns:
            str: A url that will take you to said object inside said space, if access or exists
        """
        # endregion

        return f"anytype://object?objectId={object_id}&spaceId={space_id}"

"""
Module for managing non-specific methods

Helper can be called by anything due to no dependencies

Classes:
    Helper: Encapsulating class

TODO: Move deeplink to anytype utils when ready
"""

import yaml


class Helper:
    """
    Shared methods dump

    Features:
    - File read and write combo for json sync to local instance
    """

    @staticmethod
    def read_write(path, method, data=None):
        """
        File read and write combo for yaml sync to local instance.

        Args:
            path (str): path to file to interact with.
            method (str): "r" or "w" for with open.
            data (dict): data to store into yaml.

        Returns:
            dict: from data if provided
        """

        with open(path, method, encoding="utf-8") as f:
            if data:
                f.write(yaml.safe_dump(data, sort_keys=False))
            return yaml.safe_load(f)

    def make_deeplink(self, space_id: str, object_id: str):
        """Builds deeplinks for link purposes"""
        return f"https://object.any.coop/{object_id}?spaceId={space_id}"

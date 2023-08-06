"""
BaseProvider
Subclassed by every *real* provider
"""


class BaseProvider:
    def __init__(self, client):
        """
        Initialize an the BaseProvider
        Args:
            client (:class:`GraphApiClient`): Instance of GraphApiClient
        """
        self.client = client
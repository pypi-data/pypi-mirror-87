"""
Microsoft Graph API Client
"""
import logging

from .provider.presence import PresenceProvider
from .auth.manager import AbstractAuth

log = logging.getLogger("microsoft.graph.api")

class GraphApiClient:
    def __init__(
        self,
        auth_mgr: AbstractAuth,
    ):
        self.session = auth_mgr

        self.presence = PresenceProvider(self)

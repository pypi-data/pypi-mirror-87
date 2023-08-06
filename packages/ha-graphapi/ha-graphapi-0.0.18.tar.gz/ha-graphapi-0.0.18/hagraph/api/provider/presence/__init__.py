"""
Presence
Get user presence for authenticated user or a specified user by ID
"""
from aiohttp.client import ClientResponse

from ..baseprovider import BaseProvider
from .models import PresenceResponse


class PresenceProvider(BaseProvider):
    BASE_URL = "https://graph.microsoft.com/beta"

    async def get_presence(self) -> PresenceResponse:
        """
        Get presence info for the current user
        Returns:
            :class:`PresenceResponse`: Presence Response
        """
        url = f"{self.BASE_URL}/me/presence"
        resp = await self.client.session.get(url)
        resp.raise_for_status()
        return PresenceResponse.parse_raw(await resp.text())

    async def get_presence_by_id(self, target_id: str) -> PresenceResponse:
        """
        Get Userpresence by User ID
        Args:
            target_id: User ID to get presence for
        Returns:
            :class:`PresenceResponse`: Presence Response
        """
        # https://graph.microsoft.com/beta/users/{user-id}/presence
        url = f"{self.BASE_URL}/users/{target_id}/presence"
        resp = await self.client.session.get(url)
        resp.raise_for_status()
        return PresenceResponse.parse_raw(await resp.text())

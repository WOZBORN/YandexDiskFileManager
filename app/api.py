"""
This module provides functionality for interacting with the Yandex Disk API.

It includes methods for fetching files and metadata from a public Yandex Disk
resource.
"""

from typing import Any, Dict

import aiohttp
from flask import current_app


class APIRequestError(Exception):
    """Custom exception for API request failures."""


class YandexDiskAPI:
    """
    A utility class for working with the Yandex Disk API.

    This class is designed to be static and provides helper methods for API
    interactions.
    """

    @staticmethod
    async def get_files(public_key: str, path: str = "/") -> Dict[str, Any]:
        """Fetch a list of files and their metadata from the Yandex Disk API.

        Args:
            public_key (str): Public key for accessing the Yandex Disk API.
            path (str, optional): Path to the directory in Yandex Disk.
                Defaults to "/".

        Returns:
            Dict[str, Any]: JSON response from the API containing a list of
            files and their metadata.

        Raises:
            Exception: If the API request fails.
        """
        base_url = current_app.config["YANDEX_API_BASE_URL"]
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": (
                f"OAuth {current_app.config['YANDEX_OAUTH_TOKEN']}"
            ),
        }

        params = {
            "public_key": public_key,
            "path": path,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    base_url, headers=headers, params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                error_message = await response.text()
                raise APIRequestError(
                    f"API error: {response.status} - {error_message}"
                )

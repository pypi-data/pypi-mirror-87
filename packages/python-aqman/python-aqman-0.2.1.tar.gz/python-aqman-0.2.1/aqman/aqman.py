"""Asynchronous Python client for AQMAN101 from RadonFTLabs"""
import asyncio
import socket
from typing import Any, Optional, List

import aiohttp
import async_timeout
from yarl import URL

from .__version__ import __version__
from .exceptions import AqmanError, AqmanConnectionError
from .models import Device, UserInfo
from .const import BASE_URL


class AqmanUser:
    """Main class for handling connections with an AQMAN101"""

    def __init__(
            self,
            id: str = None,
            password: str = None,
            host: str = BASE_URL,
            request_timeout: int = 10,
            session: aiohttp.ClientSession = None):
        """Initialize the AqmanUser class"""
        self._session = session

        self._id = id
        self._password = password
        self._host = host
        self._request_timeout = request_timeout
        self._token = None

    async def _request(self, uri: str, data: Optional[dict] = None,) -> Any:
        """Handle a request to a Aqman101"""
        url = URL.build(scheme="https", host=self._host, path=f"/{uri}")

        if uri == "login":
            method = "POST"
        else:
            method = "GET"
            headers = {
                "Token": f"{self._token}"
            }

        if self._session is None:
            self._session = aiohttp.ClientSession()

        try:
            with async_timeout.timeout(self._request_timeout):
                if method == "POST":
                    response = await self._session.request(
                        method, str(url), json=data,
                    )
                elif method == "GET":
                    response = await self._session.request(
                        method, str(url), params=data, headers=headers
                    )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise AqmanConnectionError(
                "Timeout occurred while connecting to Aqman 101"
            ) from exception
        except (
            aiohttp.ClientError,
            aiohttp.ClientResponseError,
            socket.gaierror,
        ) as exception:
            raise AqmanConnectionError(
                "Error occurred while communicating with Aqman 101"
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise AqmanError(
                "Unexpected response from the Aqman 101",
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def token(self) -> str:
        """Get the token for current session of Aqman101"""
        data = await self._request("login", data={"id": self._id, "password": self._password})
        web_token = data['tokenWeb']
        self._token = web_token
        return web_token

    async def devices_info(self) -> List[str]:
        """Get the list of serial numbers for current user of Aqman101"""
        if self._token == None:
            await self.token()
        data = await self._request("devices", data={"customerId": self._id})
        return UserInfo.from_list(self._id, self._password, data)

    async def close(self) -> None:
        """Close open client session."""
        if self._session:
            await self._session.close()

    async def __aenter__(self) -> "Aqman":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()


class AqmanDevice:
    """Class for handling single connection with an AQMAN101"""

    def __init__(
            self,
            id: str = None,
            password: str = None,
            deviceid: str = None,
            host: str = BASE_URL,
            request_timeout: int = 10,
            session: aiohttp.ClientSession = None) -> None:
        """Initialize Connection with AQMAN101"""
        self._session = session

        self._id = id
        self._password = password
        self._deviceid = deviceid
        self._host = host
        self._request_timeout = request_timeout
        self._token = None

    async def _request(self, uri: str, data: Optional[dict] = None,) -> Any:
        """Handle a request to a Aqman101"""
        url = URL.build(scheme="https", host=self._host, path=f"/{uri}")

        if uri == "login":
            method = "POST"
        else:
            method = "GET"
            headers = {
                "Token": f"{self._token}"
            }

        if self._session is None:
            self._session = aiohttp.ClientSession()

        try:
            with async_timeout.timeout(self._request_timeout):
                if method == "POST":
                    response = await self._session.request(
                        method, str(url), json=data,
                    )
                elif method == "GET":
                    response = await self._session.request(
                        method, str(url), params=data, headers=headers
                    )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise AqmanConnectionError(
                "Timeout occurred while connecting to Aqman 101"
            ) from exception
        except (
            aiohttp.ClientError,
            aiohttp.ClientResponseError,
            socket.gaierror,
        ) as exception:
            raise AqmanConnectionError(
                "Error occurred while communicating with Aqman 101"
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise AqmanError(
                "Unexpected response from the Aqman 101",
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def token(self) -> str:
        """Get the token for current session of Aqman101"""
        data = await self._request("login", data={"id": self._id, "password": self._password})
        web_token = data['tokenWeb']
        self._token = web_token
        return web_token

    async def state(self) -> Device:
        """Get the current state of Aqman101"""
        if self._token is None:
            await self.token()
        data = await self._request("devices", data={"sn": self._deviceid})
        return Device.from_dict(data)

    async def close(self) -> None:
        """Close open client session."""
        if self._session:
            await self._session.close()

    async def __aenter__(self) -> "Aqman":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()

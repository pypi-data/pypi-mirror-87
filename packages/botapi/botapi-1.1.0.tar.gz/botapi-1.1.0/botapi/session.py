import asyncio
from typing import Optional

import aiohttp


class BotSession:
    """
    Inherit this class if you want work with aiohttp.ClientSession in your class
    """

    _event_loop: Optional[asyncio.AbstractEventLoop] = None
    _session_kwargs: dict = {}
    _request_kwargs: dict = {}
    _session: Optional[aiohttp.ClientSession] = None

    @property
    def session(self) -> aiohttp.ClientSession:
        """
        Returns current aiohttp.ClientSession.
        If _session was closed returns new session.

        :return: aiohttp.ClientSession
        """
        if self._session is None:
            raise RuntimeError(f'{type(self)} session not created')
        if self._session.closed:
            self._session = self._get_new_session()
        return self._session

    def __init__(
        self,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
        headers: Optional[dict] = None,
        **kwargs
    ):
        self._set_event_loop(event_loop)
        self._session_kwargs['headers'] = headers
        self._request_kwargs.update(kwargs)

    def _set_event_loop(self, event_loop: Optional[asyncio.AbstractEventLoop] = None):
        """
        Saving asyncio.AbstractEventLoop for passing in aiohttp.ClientSession

        :param event_loop: asyncio.AbstractEventLoop or None
        :return: None
        """
        self._event_loop = event_loop

    def _get_new_session(self) -> aiohttp.ClientSession:
        """
        Creates and returns new aiohttp.ClientSession with self._session_kwargs

        :return: aiohttp.ClientSession
        """
        return aiohttp.ClientSession(
            **self._session_kwargs,
            loop=self._event_loop
        )

    async def create_session(self) -> aiohttp.ClientSession:
        """
        This is coroutine.

        Creates or recreates current aiohttp.ClientSession

        :return: aiohttp.ClientSession
        """
        await self.close_session()
        self._session = self._get_new_session()
        return self._session

    async def close_session(self) -> None:
        """
        This is coroutine.

        If current session was set and not closed it closed current session.

        :return: None
        """
        if self._session is not None and self._session.closed is False:
            await self._session.close()

    async def __aenter__(self):
        """
        This is coroutine.

        Creates session for using in context manager scope

        :return: object
        """
        await self.create_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        This is coroutine.

        Closing session after exit context manager scope
        """
        await self.close_session()

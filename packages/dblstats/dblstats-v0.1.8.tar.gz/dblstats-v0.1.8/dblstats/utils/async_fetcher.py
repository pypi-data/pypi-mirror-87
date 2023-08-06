# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2020 Arthur
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from json import loads

import aiohttp

from .endpoints import BASE_URL
from ..objects.exceptions import UnknownException, InvalidAuthorizationToken, InvalidTarget


class AsyncFetcher:
    """Handles all dblstats async events"""

    def __init__(self, auth: str):
        self.__auth = auth
        self.__header = {"Authorization": auth}

    @staticmethod
    async def process_response(res: aiohttp.ClientResponse):
        message = loads(await res.text())
        if res.status == 200 or message.get("status") == 200:
            return message
        if res.status == 400 or message.get("status") == 400:
            raise InvalidAuthorizationToken(message.get("message") or "No token has been provided!")
        elif res.status == 401 or message.get("status") == 401:
            raise InvalidAuthorizationToken(message.get("message") or "An invalid token has been provided!")
        elif res.status == 404 or message.get("status") == 404:
            raise InvalidTarget(message.get("message") or "Could not find the requested target!")
        raise UnknownException("Oops, an unknown exception got raised. Please report this to our github page "
                               "(https://github.com/Arthurdw/dblstats/issues) and provide the following content:"
                               f"Unhandled response code: {res.status or message.get('status')} "
                               f"({message.get('message')})")

    async def get(self, endpoint):
        """Sends an asynchronous get request to an endpoint"""
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL + endpoint, headers=self.__header) as response:
                return await self.process_response(response)

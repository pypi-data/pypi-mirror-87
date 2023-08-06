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
from datetime import datetime
from typing import List, Dict, Union

from .user import UserBase
from ..utils import represents, endpoints, AsyncFetcher


class AuctionTag:
    """Represents a dblstats tag object."""

    def __init__(self, bot: List[str], server: List[str]):
        self.bot = bot
        self.server = server

    def __repr__(self):
        return represents(self)


class AuctionUser(UserBase):
    """Represents a Top.gg auction user."""

    def __init__(self, id: str, user_tag: str, avatar: str, default_avatar: str, product: str, tag: str, list: str,
                 amount: int, outbid: bool, timestamp: datetime, is_fake: bool):
        """Creates a Top.gg auction user."""
        super().__init__(id, user_tag, avatar, default_avatar)
        self.product = product
        self.tag = tag
        self.list = list
        self.amount = amount
        self.outbid = outbid
        self.timestamp = timestamp
        self.is_fake = is_fake

    def __repr__(self):
        return represents(self)


class AuctionCurrent:
    """Represents all current betters."""

    def __init__(self, bot: Dict[str, List[AuctionUser]], server: Dict[str, List[AuctionUser]]):
        """Creates a new auction current object."""
        self.bot = bot
        self.server = server

    def __repr__(self):
        return represents(self)


class Auctions:
    """An object that can fetch the current Top.gg auctions"""

    def __init__(self, fetcher: AsyncFetcher):
        self.__fetcher = fetcher

    def __repr__(self):
        return represents(self)

    async def get_tags(self) -> AuctionTag:
        """Returns a collection of bot and server tags."""
        tags = await self.__fetcher.get(endpoints.GET_AUCTIONS_TAGS)
        return AuctionTag(tags["bot"], tags["server"])

    @staticmethod
    def parse_user_base_obj(data: Dict[str, Union[Dict[str, str], str, bool]]) -> AuctionUser:
        return AuctionUser(data["user"].get("id"), data["user"].get("tag"), data["user"].get("avatar"),
                           data["user"].get("def_avatar"), data.get("product"), data.get("tag"),
                           data.get("list"), data.get("amount"), data.get("outbid"),
                           datetime.strptime(data.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ"),
                           data.get("is_fake"))

    def parse_auction_users(self, database: Dict[str, List[Dict[str, Union[bool, int, Dict[str, str]]]]]) -> \
            Dict[str, List[AuctionUser]]:
        data = {}
        for key, collection in database:
            data[key] = list(map(self.parse_user_base_obj, collection))
        return data

    async def get_current(self) -> AuctionCurrent:
        """Returns a dictionary of all current betters."""
        data = await self.__fetcher.get(endpoints.GET_AUCTIONS_CURRENT)
        return AuctionCurrent(self.parse_auction_users(data["bot"].items()),
                              self.parse_auction_users(data["server"].items()))

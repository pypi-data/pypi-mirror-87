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
from enum import Enum
from typing import Union, List

from .bot import Bot, BotHistory
from .dblstats_auctions import Auctions
from .user import UserBots
from ..utils import represents, AsyncFetcher, endpoints
from ..utils.convertors import parse_bot_base_object, parse_bot_object, parse_user_base_object


class Sorter(Enum):
    """
    :attr votes: Sorts by most voted
    :attr monthly_votes: Sorts by most voted from this month
    :attr servers: Sorts by most servers
    :attr shards: Sorts by most shards
    """
    votes = "votes"
    monthly_votes = "monthly votes"
    servers = "servers"
    shards = "shards"


class Client:
    """
    Represents your dblstatistics.com client.

    This interacts with the api, so it allows you to fetch data.
    """

    def __init__(self, token: str):
        self.__fetcher = AsyncFetcher(token)
        self.auctions = Auctions(self.__fetcher)

    def __repr__(self):
        return represents(self)

    async def get_bot(self, id: Union[int, str]) -> Bot:
        """
        Fetch a bot from the dblstatistics website.

        :param id: The id of the bot that must be fetched.
        """
        bot = await self.__fetcher.get(endpoints.GET_BOT_URL.format(id=id))
        return parse_bot_object(bot)

    async def get_bot_history(self, id: Union[int, str]) -> BotHistory:
        """
        Fetch a bot its history from the dblstatistics website.

        :param id: The id of the bot that must be fetched.
        """
        history = await self.__fetcher.get(endpoints.GET_BOT_HISTORY_URL.format(id=id))
        return BotHistory(history.get("id"), list(map(parse_bot_base_object, history.get("data"))))

    async def get_top_bots(self, sort_by: Sorter = Sorter.votes) -> List[Bot]:
        """
        Returns a collection of sorted dblstats Bot objects.

        :param sort_by: The way the bots should get sorted, default is by votes.
        """
        if not isinstance(sort_by, Sorter):
            raise TypeError(f"Can not use type `{type(sort_by)}` to sort bots. Please use the `dblstats.Sorter` enum!")

        bots = await self.__fetcher.get(endpoints.GET_TOP_BOTS.format(value=sort_by.value))
        return list(map(parse_bot_object, bots))

    async def get_user_bots(self, id: Union[int, str]) -> UserBots:
        """
        Returns all bots from a user. (As a UserBots object)

        :param id: The user from which the bots should be fetched.
        """
        user_bots = await self.__fetcher.get(endpoints.GET_USER_BOTS.format(id=id))
        print(user_bots)
        return UserBots(parse_user_base_object(user_bots["user"]), list(map(parse_bot_object, user_bots["bots"])))

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
from typing import List

from ..utils import represents


class BotBase:
    """A bot helper function that contains the basic bot values"""

    def __init__(self, owners: List[int], monthly_votes: int, server_count: int, total_votes: int,
                 shard_count: int, monthly_votes_rank: int, server_count_rank: int, total_votes_rank: int,
                 shard_count_rank: int, updated_at: datetime):
        """
        Creates a dblstats BotBase object, which contains the basic bot values.

        :param owners: A collection of the bot owner(s) their discord IDs
        :param monthly_votes: The amount of votes that the bot has received this month
        :param server_count: The amount of servers the bot is in (self reported)
        :param total_votes: The total amount of votes that the bot has
        :param shard_count: The amount of shards that the bot is running on (self reported)
        :param monthly_votes_rank: The position that the bot is in relative to the other bots registered on Top.gg qua votes from this month
        :param server_count_rank: The position that the bot is in relative to the other bots registered on Top.gg qua servers
        :param total_votes_rank: The position that the bot is in relative to the other bots registered on Top.gg qua votes
        :param shard_count_rank: The position that the bot is in relative to the other bots registered on Top.gg qua shards
        :param updated_at: The timestamp that this was updated on
        """
        self.owners = owners
        self.monthly_votes = monthly_votes
        self.server_count = server_count
        self.total_votes = total_votes
        self.shard_count = shard_count
        self.monthly_votes_rank = monthly_votes_rank
        self.server_count_rank = server_count_rank
        self.total_votes_rank = total_votes_rank
        self.shard_count_rank = shard_count_rank
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return represents(self)


class Bot(BotBase):
    """The object that represents a bot in Top.gg"""

    def __init__(self, certified: bool, owners: List[int], deleted: bool, id: str, name: str, default_avatar: str,
                 avatar: str, short_description: str, library: str, prefix: str, website: str, approved_at: datetime,
                 monthly_votes: int, server_count: int, total_votes: int, shard_count: int, monthly_votes_rank: int,
                 server_count_rank: int, total_votes_rank: int, shard_count_rank: int, updated_at: datetime):
        """
        Create a dblstats Bot object. (which represents a bot in Top.gg)

        :param certified: Whether or not the bot is certified on Top.gg
        :param deleted: Whether or not the bot has been removed from Top.gg
        :param id: The bot its user id
        :param name: The bot its username
        :param default_avatar: The default assigned avatar that has been given to the bot (Decided by discriminator)
        :param avatar: The bot avatar url
        :param short_description: A short text that describes the bot
        :param library: The library that the bot uses
        :param prefix: The default bot prefix
        :param website: The website that is associated with the bot
        :param approved_at: The datetime from when the bot got added to Top.gg
        """
        super().__init__(owners, monthly_votes, server_count, total_votes, shard_count, monthly_votes_rank,
                         server_count_rank, total_votes_rank, shard_count_rank, updated_at)
        self.certified = certified
        self.deleted = deleted
        self.id = id
        self.name = name
        self.default_avatar = f"https://discord.com/assets/{default_avatar}.png"
        self.avatar = f"https://cdn.discordapp.com/avatars/{id}/{avatar}.webp"
        self.short_description = short_description
        self.library = library
        self.prefix = prefix
        self.website = website
        self.approved_at = approved_at

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return represents(self)


class BotHistory:
    """
    An object that contains a collection of `BotBase` objects.
    Each item differs one hour with the previous item.

    The maximum collection size is 500
    """

    def __init__(self, id: str, history: List[BotBase]):
        """
        Creates a dblstats BotHistory object.
        In this object you can see/find the previous bot data for that bot.

        :param id: The bot its id from which the history is shown
        :param history: A collection of `BotBase` objects that can be used to see the bot its history.
        """
        self.id = id
        self.history = history

    def __iter__(self) -> List[BotBase]:
        return self.history

    def __repr__(self) -> str:
        return represents(self)

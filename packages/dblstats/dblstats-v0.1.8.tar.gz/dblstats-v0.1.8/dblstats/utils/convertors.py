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
from typing import Dict, Union, List

from ..objects import Bot, BotBase, UserBase


def parse_bot_object(data: Dict[str, Union[bool, List[str], str, int]]):
    return Bot(data["certified"], list(map(lambda i: int(i), data.get("owners"))), data.get("deleted"),
               data.get("id"),
               data.get("name"), data.get("def_avatar"), data.get("avatar"), data.get("short_desc"),
               data.get("lib"),
               data.get("prefix"), data.get("website"),
               datetime.strptime(data.get("approved_at"), "%Y-%m-%dT%H:%M:%S.%fZ"), data.get("monthly_votes"),
               data.get("server_count"), data.get("total_votes"), data.get("shard_count"),
               data.get("monthly_votes_rank"), data.get("server_count_rank"), data.get("total_votes_rank"),
               data.get("shard_count_rank"), datetime.strptime(data.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ"))


def parse_bot_base_object(data: Dict[str, Union[List[str], int, str]]) -> BotBase:
    return BotBase(list(map(lambda owner: int(owner), data.get("owners"))), data.get("monthly_votes"),
                   data.get("server_count"), data.get("total_votes"), data.get("shard_count"),
                   data.get("monthly_votes_rank"), data.get("server_count_rank"), data.get("total_votes_rank"),
                   data.get("shard_count_rank"),
                   datetime.strptime(data.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ"))


def parse_user_base_object(data: Dict[str, str]) -> UserBase:
    return UserBase(data.get("id"), data.get("tag"), data.get("avatar"), data.get("def_avatar"))

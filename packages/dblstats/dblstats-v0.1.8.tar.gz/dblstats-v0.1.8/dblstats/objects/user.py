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
from typing import List

from .bot import Bot
from ..utils import represents


class UserBase:
    """Represents the base of a top.gg user."""

    def __init__(self, id: str, tag: str, avatar: str, default_avatar: str):
        """
        Creates a new Top.gg user base.

        :param id: The user their discord id
        :param tag: The user their discord tag (username#discriminator)
        :param avatar: The user their discord avatar url
        :param default_avatar: The user their default discord avatar url (calculated by discriminator)
        """
        self.id = id
        self.tag = tag
        self.avatar = f"https://cdn.discordapp.com/avatars/{id}/{avatar}.webp"
        self.default_avatar = default_avatar

    def __repr__(self):
        return represents(self)


class UserBots:
    """Represents a user with their corresponding bots."""

    def __init__(self, user: UserBase, bots: List[Bot]):
        """
        Creates a new UserBot.

        :param user: The user that owns the bots.
        :param bots: A collection of bots that are owned by the user.
        """
        self.user = user
        self.bots = bots

    def __repr__(self):
        return represents(self)

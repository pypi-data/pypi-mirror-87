#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2018 Christoph Fink, University of Helsinki
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 3
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.


"""
Downloads the latest list of UTF emoji characters from
unicode.org and returns them as a concatenated str
(like string.letters)
"""


import datetime
import os
import os.path
import re
import string
import sys

import requests


__all__ = ["EMOJIS"]


class CacheExpiredException(BaseException):
    """custom local exception to handle cache expiration"""


def _get_emoji_unicode_values():
    """
    Return a set of all unicode values
    that represent emojis
    """
    emoji_unicode_values = []

    re_pattern = re.compile(
        "^(?P<min_val>[0-9A-F]{4,5})(?:..(?P<max_val>[0-9A-F]{4,5}))?"
    )

    for line in _download_emoji_list().splitlines():
        re_match = re_pattern.match(line)

        if re_match:
            min_val = int(re_match["min_val"], 16)
            try:
                max_val = int(re_match["max_val"], 16)
            except TypeError:
                max_val = None

            if min_val > 128:  # unicode also lists 0…9 as emojis
                if max_val is None:
                    emoji_unicode_values.append(min_val)
                else:
                    emoji_unicode_values += list(range(min_val, max_val + 1))

    emoji_unicode_values = set(emoji_unicode_values)
    return emoji_unicode_values


def _download_emoji_list():
    """
    Check local cache whether we have a recent (<1 week old) version
    of unicode.org’s list of emojis, otherwise download it

    Args:
        none

    Returns:
        content of emoji-data.txt (str)
    """
    cache_filename = os.path.join(
        (
            os.environ.get("LOCALAPPDATA")
            or os.environ.get("XDG_CACHE_HOME")
            or os.path.join(os.environ["HOME"], ".cache")
        ),
        __name__,
        "emoji-data.txt",
    )

    try:
        cache_age = (
            datetime.datetime.now().timestamp() - os.stat(cache_filename).st_mtime
        )

        if cache_age > (60 * 60 * 24 * 7):
            raise CacheExpiredException

        with open(cache_filename) as cache_file:
            emojidata = cache_file.read()

    except (FileNotFoundError, CacheExpiredException):
        emojidata = requests.get(
            "https://unicode.org/Public/emoji/latest/emoji-sequences.txt"
        ).text

        os.makedirs(os.path.dirname(cache_filename), exist_ok=True)
        with open(cache_filename, "w") as cache_file:
            cache_file.write(emojidata)

    return emojidata


EMOJIS = "".join([chr(char) for char in _get_emoji_unicode_values()])

string.emojis = EMOJIS
sys.modules.update({"string": string})

if __name__ == "__main__":
    pass

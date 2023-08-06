"""LICENSE
Copyright 2020 Hermann Krumrey <hermann@krumreyh.com>

This file is part of otaku-info.

otaku-info is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

otaku-info is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with otaku-info.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import json
import requests
from typing import Optional
from requests.exceptions import ConnectionError
from otaku_info.external.entities.MangadexItem import MangadexItem


def fetch_mangadex_item(mangadex_id: int) -> Optional[MangadexItem]:
    """
    Fetches information for a mangadex
    """
    endpoint = "https://mangadex.org/api/manga/{}".format(mangadex_id)
    try:
        with requests.get(endpoint) as response:
            data = json.loads(response.text)
            if data["status"] == "OK":
                return MangadexItem.from_json(mangadex_id, data)
            else:
                return None
    except (json.JSONDecodeError, ConnectionError):
        return None

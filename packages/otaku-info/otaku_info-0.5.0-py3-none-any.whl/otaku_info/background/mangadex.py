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

import time
from typing import Optional
from jerrycan.base import app
from otaku_info.db.MediaId import MediaId
from otaku_info.enums import ListService, MediaType, MediaSubType
from otaku_info.external.entities.AnimeListItem import AnimeListItem
from otaku_info.external.mangadex import fetch_mangadex_item
from otaku_info.external.anilist import load_anilist_info
from otaku_info.external.myanimelist import load_myanimelist_item
from otaku_info.background.db_inserter import queue_media_item_insert


def update_mangadex_data(
        start: int = 1,
        end: Optional[int] = None,
        refresh: bool = False
):
    """
    Goes through mangadex IDs sequentially and stores ID mappings for
    these entries if found.
    Stops once 100 consecutive entries didn't return any results
    :param start: Optionally specifies a starting index
    :param end: Optionally specifies an ending index
    :param refresh: If true, will update existing mangadex info
    :return: None
    """
    start_time = time.time()
    app.logger.info("Starting Mangadex Update")

    endcounter = 0
    mangadex_id = start - 1

    existing_ids = [
        int(x.service_id)
        for x in MediaId.query.filter_by(service=ListService.MANGADEX).all()
    ]

    while True:
        mangadex_id += 1

        if mangadex_id == end or endcounter > 100:
            break
        elif str(mangadex_id) in existing_ids and not refresh:
            endcounter = 0
            continue

        app.logger.debug(f"Probing mangadex id {mangadex_id}")
        mangadex_item = fetch_mangadex_item(mangadex_id)
        if mangadex_item is None:
            endcounter += 1
            app.logger.debug(f"Couldn't load mangadex info ({mangadex_id})")
            continue
        else:
            endcounter = 0

        media_item_params = {
            "media_type": MediaType.MANGA,
            "media_subtype": MediaSubType.MANGA,
            "english_title": mangadex_item.title,
            "romaji_title": mangadex_item.title,
            "cover_url": mangadex_item.cover_url,
            "latest_release": mangadex_item.total_chapters,
            "releasing_state": mangadex_item.releasing_state
        }
        service_ids = mangadex_item.external_ids
        service_ids[ListService.MANGADEX] = str(mangadex_id)

        better_item: Optional[AnimeListItem] = None
        if ListService.ANILIST in service_ids:
            better_item = load_anilist_info(
                int(service_ids[ListService.ANILIST]),
                MediaType.MANGA
            )
        elif ListService.MYANIMELIST in service_ids:
            better_item = load_myanimelist_item(
                int(service_ids[ListService.MYANIMELIST]),
                MediaType.MANGA
            )

        if better_item is not None:
            media_item_params["media_subtype"] = better_item.media_subtype
            media_item_params["english_title"] = better_item.english_title
            media_item_params["romaji_title"] = better_item.romaji_title
            media_item_params["releasing_state"] = better_item.releasing_state
            media_item_params["cover_url"] = better_item.cover_url
            media_item_params["latest_release"] = better_item.latest_release

        queue_media_item_insert(
            media_item_params, ListService.MANGADEX, service_ids
        )

    app.logger.info(f"Finished Mangadex Update in "
                    f"{time.time() - start_time}s.")

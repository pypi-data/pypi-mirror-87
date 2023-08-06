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

from typing import Tuple
from jerrycan.base import db
from sqlalchemy.exc import IntegrityError
from otaku_info.db.MediaItem import MediaItem
from otaku_info.db.MediaId import MediaId
from otaku_info.enums import ListService, MediaType, MediaSubType, \
    ReleasingState
from otaku_info.test.TestFramework import _TestFramework


class TestMediaId(_TestFramework):
    """
    Class that tests the MediaId database model
    """

    @staticmethod
    def generate_sample_media_id() -> Tuple[MediaItem, MediaId]:
        """
        Generates a media id
        :return: The media item and media id
        """
        media_item = MediaItem(
            media_type=MediaType.MANGA,
            media_subtype=MediaSubType.MANGA,
            english_title="Fly Me to the Moon",
            romaji_title="Tonikaku Cawaii",
            cover_url="https://s4.anilist.co/file/anilistcdn/media/manga/"
                      "cover/medium/nx101177-FjjD5UWB3C3t.png",
            latest_release=None,
            releasing_state=ReleasingState.RELEASING
        )
        media_id = MediaId(
            media_item=media_item,
            service_id="101177",
            service=ListService.ANILIST,
            media_type=media_item.media_type,
            media_subtype=media_item.media_subtype
        )
        db.session.add(media_item)
        db.session.add(media_id)
        db.session.commit()
        return media_item, media_id

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        media_item, media_id = self.generate_sample_media_id()

        self.assertEqual(
            media_id.__json__(False),
            {
                "id": media_id.id,
                "media_item_id": media_item.id,
                "service": media_id.service.name,
                "service_id": media_id.service_id,
                "media_type": media_id.media_type.name,
                "media_subtype": media_id.media_subtype.name
            }
        )
        self.assertEqual(
            media_id.__json__(True),
            {
                "id": media_id.id,
                "media_item": media_item.__json__(True, ["media_ids"]),
                "media_item_id": media_item.id,
                "service": media_id.service.name,
                "service_id": media_id.service_id,
                "media_type": media_id.media_type.name,
                "media_subtype": media_id.media_subtype.name,
                "media_user_states": [],
                "chapter_guess": None
            }
        )

    def test_string_representation(self):
        """
        Tests the string representation of the model
        :return: None
        """
        media_item, media_id = self.generate_sample_media_id()
        data = media_id.__json__()
        data.pop("id")
        self.assertEqual(
            str(media_id),
            "MediaId:{} <{}>".format(media_id.id, data)
        )

    def test_repr(self):
        """
        Tests the __repr__ method of the model class
        :return: None
        """
        media_item, media_id = self.generate_sample_media_id()
        generated = {"value": media_id}
        code = repr(media_id)

        exec("generated['value'] = " + code)
        self.assertEqual(generated["value"], media_id)
        self.assertFalse(generated["value"] is media_id)

    def test_hashing(self):
        """
        Tests using the model objects as keys in a dictionary
        :return: None
        """
        media_item, media_id = self.generate_sample_media_id()
        media_id_2 = MediaId(
            media_item=media_item,
            service_id="101178",
            service=ListService.KITSU
        )
        db.session.add(media_id_2)
        db.session.commit()
        mapping = {
            media_id: 100,
            media_id_2: 200
        }
        self.assertEqual(mapping[media_id], 100)
        self.assertEqual(mapping[media_id_2], 200)

    def test_equality(self):
        """
        Tests checking equality for model objects
        :return: None
        """
        media_item, media_id = self.generate_sample_media_id()
        media_id_2 = MediaId(
            media_item=media_item,
            service_id="101178",
            service=ListService.KITSU
        )
        db.session.add(media_id_2)
        db.session.commit()
        self.assertEqual(media_id, media_id)
        self.assertNotEqual(media_id, media_id_2)
        self.assertNotEqual(media_id, 100)

    def test_generating_service_url(self):
        """
        Tests generating the generating of service URLs
        :return: None
        """
        _, media_id = self.generate_sample_media_id()
        urls = {
            ListService.ANILIST: "https://anilist.co/manga/101177",
            ListService.MYANIMELIST: "https://myanimelist.net/manga/101177",
            ListService.MANGADEX: "https://mangadex.org/title/101177",
            ListService.MANGAUPDATES: "https://www.mangaupdates.com/"
                                      "series.html?id=101177",
            ListService.ANIMEPLANET: "https://www.anime-planet.com/"
                                     "manga/101177",
            ListService.KITSU: "https://kitsu.io/anime/101177"
        }
        for service in ListService:
            expected = urls[service]
            media_id.service = service
            self.assertEqual(media_id.service_url, expected)

    def test_uniqueness(self):
        """
        Tests if the uniqueness of the model is handled properly
        :return: None
        """
        media_item, media_id = self.generate_sample_media_id()
        media_item_two = MediaItem(
            media_type=MediaType.MANGA,
            media_subtype=MediaSubType.MANGA,
            english_title="Don't Fly Me to the Moon",
            romaji_title="ATonikaku Cawaii",
            cover_url="https://s4.anilist.co/file/anilistcdn/media/manga/"
                      "cover/medium/nx101177-FjjD5UWB3C3t.png",
            latest_release=None,
            releasing_state=ReleasingState.RELEASING
        )
        db.session.add(media_item_two)
        db.session.commit()

        standard_kwargs = media_id.__json__(False)
        standard_kwargs.pop("id")
        standard_kwargs["service"] = media_id.service
        standard_kwargs["media_type"] = media_id.media_type
        standard_kwargs["media_subtype"] = media_id.media_subtype

        try:
            duplicate = MediaId(**standard_kwargs)
            db.session.add(duplicate)
            db.session.commit()
            self.fail()
        except IntegrityError:
            db.session.rollback()

        for key, value, error_expected in [
            ("media_item_id", media_item_two.id, True),
            ("service", ListService.KITSU, False),
            ("service_id", "100", True)
        ]:
            kwargs = dict(standard_kwargs)
            kwargs[key] = value
            try:
                generated = MediaId(**kwargs)
                db.session.add(generated)
                db.session.commit()
                if error_expected:
                    self.fail()
            except IntegrityError as e:
                db.session.rollback()
                print(key)
                if not error_expected:
                    raise e

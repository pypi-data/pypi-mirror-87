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

from typing import Dict, Any, Tuple
from jerrycan.base import db
from otaku_info.db.ModelMixin import ModelMixin
from otaku_info.db.MediaList import MediaList
from otaku_info.db.MediaUserState import MediaUserState


class MediaListItem(ModelMixin, db.Model):
    """
    Database model for media list items.
    This model maps MediaLists and MediaUserStates
    """

    __tablename__ = "media_list_items"
    """
    The name of the database table
    """

    __table_args__ = (
        db.UniqueConstraint(
            "media_list_id",
            "media_user_state_id",
            name="unique_media_list_item"
        ),
    )
    """
    Makes sure that objects that should be unique are unique
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    media_list_id: int = db.Column(
        db.Integer,
        db.ForeignKey("media_lists.id"),
        nullable=False
    )
    """
    The ID of the media list this list item is a part of
    """

    media_list: MediaList = db.relationship(
        "MediaList",
        back_populates="media_list_items"
    )
    """
    The media list this list item is a part of
    """

    media_user_state_id: int = db.Column(
        db.Integer,
        db.ForeignKey(
            "media_user_states.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False
    )
    """
    The ID of the media user state this list item references
    """

    media_user_state: MediaUserState = db.relationship(
        "MediaUserState",
        backref=db.backref("media_list_items", lazy=True, cascade="all,delete")
    )
    """
    The media user state this list item references
    """

    @property
    def identifier_tuple(self) -> Tuple[int, int]:
        """
        :return: A tuple that uniquely identifies this database entry
        """
        return self.media_list_id, self.media_user_state_id

    def update(self, new_data: "MediaListItem"):
        """
        Updates the data in this record based on another object
        :param new_data: The object from which to use the new values
        :return: None
        """
        self.media_list_id = new_data.media_list_id
        self.media_user_state_id = new_data.media_user_state_id

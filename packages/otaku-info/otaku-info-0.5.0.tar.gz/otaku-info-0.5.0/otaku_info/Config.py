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

import os
from typing import Type
from jerrycan.Config import Config as BaseConfig
from bokkichat.settings.impl.TelegramBotSettings import TelegramBotSettings
from bokkichat.connection.impl.TelegramBotConnection import \
    TelegramBotConnection


class Config(BaseConfig):
    """
    Configuration for the flask application
    """

    TELEGRAM_API_KEY: str
    """
    API Key for the telegram bot used for notification messages
    """

    TELEGRAM_BOT_CONNECTION: TelegramBotConnection
    """
    Single Telegram bot connection used for all telegram communications
    """

    @classmethod
    def _load_extras(cls, parent: Type[BaseConfig]):
        """
        Loads non-standard configuration variables
        :param parent: The base configuration
        :return: None
        """
        from otaku_info.template_extras import profile_extras
        parent.TEMPLATE_EXTRAS.update({
            "profile": profile_extras
        })

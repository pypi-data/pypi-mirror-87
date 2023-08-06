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

from typing import Dict, Any
from flask_login import current_user
from otaku_info.enums import ListService
from otaku_info.db.ServiceUsername import ServiceUsername


def profile_extras() -> Dict[str, Any]:
    """
    Makes sure that the profile page displays service usernames
    :return: The variables to forward to the template
    """
    service_usernames = {}
    for service in ListService:
        service_username = ServiceUsername.query.filter_by(
            user=current_user, service=service
        ).first()
        service_usernames[service] = service_username
    return {
        "service_usernames": service_usernames
    }

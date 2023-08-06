#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2019 Christoph Fink, University of Helsinki
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

""" A class to save a Youtube user to the database and return its ID """


__all__ = [
    "YoutubeUser"
]


from .databaseobject import (
    DatabaseObject
)


class YoutubeUser(DatabaseObject):
    """ A class to save a Youtube user to
        the database and return its ID
    """

    def __init__(
            self,
            username,
            profile_url,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._name = username
        self._id = self._save_to_database(username, profile_url)

    def _save_to_database(self, username, profile_url):
        return self.execute_sql(
            """
                INSERT INTO
                    users (
                        name,
                        profile_url
                    )
                    values (
                        %(name)s,
                        %(profile_url)s
                    )
                ON CONFLICT (profile_url)
                    DO UPDATE
                        set profile_url = EXCLUDED.profile_url
                RETURNING id;
            """,
            {
                "name": username,
                "profile_url": profile_url
            }
        )[0]["id"]

    def _create_tables(self):
        self.execute_sql(
            """
                CREATE TABLE IF NOT EXISTS
                    users (
                        id SERIAL PRIMARY KEY,
                        name TEXT,
                        profile_url TEXT UNIQUE
                    );
            """
        )

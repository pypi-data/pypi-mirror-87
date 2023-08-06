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

""" A class to save a Youtube channel to the database and return its ID """


__all__ = [
    "YoutubeChannel"
]


from .databaseobject import (
    DatabaseObject
)


class YoutubeChannel(DatabaseObject):
    """ A class to save a Youtube channel to
        the database and return its ID
    """

    def __init__(
            self,
            orig_id,
            title,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._name = title
        self._orig_id = orig_id
        self._id = self._save_to_database(orig_id, title)

    def _save_to_database(self, orig_id, title):
        return self.execute_sql(
            """
                INSERT INTO
                    channels (
                        orig_id,
                        title
                    )
                    values (
                        %(orig_id)s,
                        %(title)s
                    )
                ON CONFLICT (orig_id)
                    DO UPDATE
                        set title = EXCLUDED.title
                RETURNING id;
            """,
            {
                "orig_id": orig_id,
                "title": title
            }
        )[0]["id"]

    def _create_tables(self):
        self.execute_sql(
            """
                CREATE TABLE IF NOT EXISTS
                    channels (
                        id SERIAL PRIMARY KEY,
                        orig_id CHAR(24) UNIQUE,
                        title TEXT
                    );
            """
        )

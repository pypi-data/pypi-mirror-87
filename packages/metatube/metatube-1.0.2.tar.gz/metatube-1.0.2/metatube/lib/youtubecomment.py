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

""" A class to save a Youtube comment to the database and return its ID """


__all__ = [
    "YoutubeComment"
]


import dateparser

from .databaseobject import (
    DatabaseObject
)
from .youtubeuser import (
    YoutubeUser
)


#  # EXAMPLE record
#     {
#      "kind": "youtube#comment",
#      "etag": "\"SJZWTG6xR0eGuCOh2bX6w3s4F94/EwwgqCUTedRz4UQ0YrMDealtuec\"",
#      "id": "Ugw1hpNW--cMCwhG-wJ4AaABAg.90k0KongL2A90sDm4BCnYb",
#      "snippet": {
#       "authorDisplayName": "Sugyono Saja",
#       "authorProfileImageUrl": "https://yt3.ggpht.com/a...-mo",
#       "authorChannelUrl": "http://www.you...Fy5nPw",
#       "authorChannelId": {
#        "value": "UCVMHlmXvrgh-SASkqFy5nPw"
#       },
#       "videoId": "wJitjtID0cc",
#       "textDisplay": "Bikin burung laen drop. Suara kasar dan kerras",
#       "textOriginal": "Bikin burung laen drop. Suara kasar dan kerras",
#       "parentId": "Ugw1hpNW--cMCwhG-wJ4AaABAg",
#       "canRate": true,
#       "viewerRating": "none",
#       "likeCount": 1,
#       "publishedAt": "2019-11-03T11:36:28.000Z",
#       "updatedAt": "2019-11-03T11:36:28.000Z"
#      }

class YoutubeComment(DatabaseObject):
    """ A class to save a Youtube comment to
        the database and return its ID
    """

    def __init__(
            self,
            comment,
            comment_thread_id,
            video_id,
            order_in_thread,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._parse_comment_snippet(
            comment,
            comment_thread_id,
            video_id,
            order_in_thread
        )

    def _parse_comment_snippet(
            self,
            comment,
            comment_thread_id,
            video_id,
            order_in_thread
    ):
        text = comment["snippet"]["textOriginal"]
        published = dateparser.parse(
            comment["snippet"]["publishedAt"]
        )
        updated = dateparser.parse(
            comment["snippet"]["updatedAt"]
        )
        author_id = int(
            YoutubeUser(
                comment["snippet"]["authorDisplayName"],
                comment["snippet"]["authorChannelUrl"]
            )
        )

        self._id = self._save_to_database(
            published,
            updated,
            author_id,
            comment_thread_id,
            video_id,
            order_in_thread,
            text
        )
        self._name = f"{text[:10]}..."

    def _save_to_database(
            self,
            published,
            updated,
            author_id,
            comment_thread_id,
            video_id,
            order_in_thread,
            text
    ):
        return self.execute_sql(
            """
                INSERT INTO
                    comments (
                        published,
                        updated,
                        author_id,
                        comment_thread_id,
                        video_id,
                        order_in_thread,
                        text
                    )
                    values (
                        %(published)s,
                        %(updated)s,
                        %(author_id)s,
                        %(comment_thread_id)s,
                        %(video_id)s,
                        %(order_in_thread)s,
                        %(text)s
                    )
                ON CONFLICT (comment_thread_id, order_in_thread)
                    DO UPDATE
                        SET
                            published = EXCLUDED.published,
                            updated = EXCLUDED.updated,
                            author_id = EXCLUDED.author_id,
                            video_id = EXCLUDED.video_id,
                            text = EXCLUDED.text
                RETURNING id;
            """,
            {
                "published": published,
                "updated": updated,
                "author_id": author_id,
                "comment_thread_id": comment_thread_id,
                "video_id": video_id,
                "order_in_thread": order_in_thread,
                "text": text
            }
        )[0]["id"]

    def _create_tables(self):
        self.execute_sql(
            """
                CREATE TABLE
                    comments (
                        id SERIAL PRIMARY KEY,
                        published TIMESTAMP WITH TIME ZONE,
                        updated TIMESTAMP WITH TIME ZONE,
                        author_id INTEGER NOT NULL REFERENCES users(id),
                        comment_thread_id INTEGER NOT NULL
                            REFERENCES comment_threads(id),
                        video_id INTEGER NOT NULL REFERENCES videos(id),
                        order_in_thread INTEGER NOT NULL DEFAULT 0,
                        text TEXT,
                        UNIQUE(comment_thread_id, order_in_thread)
                    );

                CREATE INDEX IF NOT EXISTS
                    comments_published_idx
                ON
                    comments
                        (published);

                CREATE INDEX IF NOT EXISTS
                    comments_author_id_idx
                ON
                    comments
                        (author_id);

                CREATE INDEX IF NOT EXISTS
                    comments_comment_thread_id_idx
                ON
                    comments
                        (comment_thread_id);

                CREATE INDEX IF NOT EXISTS
                    comments_video_id_idx
                ON
                    comments
                        (video_id);

                CREATE INDEX IF NOT EXISTS
                    comments_first_in_thread_idx
                ON
                    comments
                        ((order_in_thread = 0));
            """
        )

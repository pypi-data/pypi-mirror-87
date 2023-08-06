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

""" A class to save a Youtube a comment thread to the database and
    return its ID """


__all__ = [
    "YoutubeCommentThread"
]


import psycopg2

from .databaseobject import (
    DatabaseObject
)
from .youtubecomment import (
    YoutubeComment
)


# # EXAMPLE record
# {
#    "kind": "youtube#commentThread",
#    "etag": "\"SJZWTG6xR0eGuCOh2bX6w3s4F94/N-J1KPYA9h-RBd85_HSEeX3k8sw\"",
#    "id": "Ugw1hpNW--cMCwhG-wJ4AaABAg",
#    "replies": {
#     "comments": [
#      {
#       "kind": "youtube#comment",
#       "etag": "\"SJZWTG6xR0eGuCOh2bX6w3s4F94/uywljaTLRNTc5Xucl-OcyIF5dxs\"",
#       "id": "Ugw1hpNW--cMCwhG-wJ4AaABAg.90k0KongL2A93CeG-oebDs",
#       "snippet": {
#        "authorDisplayName": "Joko Prabowo",
#        "authorProfileImageUrl": "https://yt3.ggpht.com/...no-rj-mo",
#        "authorChannelUrl": "http://www.youtube.com/channel/UCZzay...",
#        "authorChannelId": {
#         "value": "UCZzaynt0Q3s3rEYEvWnCFKg"
#        },
#        "videoId": "wJitjtID0cc",
#        "textDisplay": "@Sugyono Saja betul om",
#        "textOriginal": "@Sugyono Saja betul om",
#        "parentId": "Ugw1hpNW--cMCwhG-wJ4AaABAg",
#        "canRate": true,
#        "viewerRating": "none",
#        "likeCount": 0,
#        "publishedAt": "2019-12-31T12:23:28.000Z",
#        "updatedAt": "2019-12-31T12:23:28.000Z"
#       }
#      },
#      {
#       "kind": "youtube#comment",
#       "etag": "\"SJZWTG6xR0eGuCOh2bX6w3s4F94/EwwgqCUTedRz4UQ0YrMDealtuec\"",
#       "id": "Ugw1hpNW--cMCwhG-wJ4AaABAg.90k0KongL2A90sDm4BCnYb",
#       "snippet": {
#        "authorDisplayName": "Sugyono Saja",
#        "authorProfileImageUrl": "https://yt3.ggpht.com/a/AGF-l7_eYs...j-mo",
#        "authorChannelUrl": "http://www.youtube.com/channel/UCVMHlmXv...",
#        "authorChannelId": {
#         "value": "UCVMHlmXvrgh-SASkqFy5nPw"
#        },
#        "videoId": "wJitjtID0cc",
#        "textDisplay": "Bikin burung laen drop. Suara kasar dan kerras",
#        "textOriginal": "Bikin burung laen drop. Suara kasar dan kerras",
#        "parentId": "Ugw1hpNW--cMCwhG-wJ4AaABAg",
#        "canRate": true,
#        "viewerRating": "none",
#        "likeCount": 1,
#        "publishedAt": "2019-11-03T11:36:28.000Z",
#        "updatedAt": "2019-11-03T11:36:28.000Z"
#       }
#      }
#     ]
#    }
#   }


class YoutubeCommentThread(DatabaseObject):
    """ A class to save a Youtube comment thread to
        the database and return its ID
    """

    def __init__(
            self,
            commentthread,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._parse_commentthread_snippet(
            commentthread
        )

    def _get_video_id(self, orig_id):
        try:
            video_id = self.execute_sql(
                """
                    SELECT
                        id
                    FROM
                        videos
                    WHERE
                        orig_id = %(orig_id)s;
                """,
                {
                    "orig_id": orig_id
                }
            )[0]["id"]
        except (KeyError, psycopg2.Error):
            video_id = None
        return video_id

    def _parse_commentthread_snippet(
            self,
            commentthread
    ):
        orig_id = commentthread["id"]
        video_id = self._get_video_id(
            commentthread["snippet"]["videoId"]
        )

        self._id = self._save_to_database(orig_id, video_id)
        self._name = f"{orig_id[:10]}..."

        # parse comments
        order_in_thread = 0

        try:
            _ = YoutubeComment(
                commentthread["snippet"]["topLevelComment"],
                self._id,
                video_id,
                order_in_thread
            )
            del _
            order_in_thread += 1
        except KeyError as e:
            if e.args[0] in ("snippet", "topLevelComment"):
                pass
            else:
                raise e

        try:
            for comment in commentthread["replies"]["comments"]:
                _ = YoutubeComment(
                    comment,
                    self._id,
                    video_id,
                    order_in_thread
                )
                del _
                order_in_thread += 1
        except KeyError as e:
            if e.args[0] in ("replies",):
                pass
            else:
                raise e

    def _save_to_database(self, orig_id, video_id):
        return self.execute_sql(
            """
                INSERT INTO
                    comment_threads (
                        orig_id,
                        video_id
                    )
                    values (
                        %(orig_id)s,
                        %(video_id)s
                    )
                ON CONFLICT (orig_id)
                    DO UPDATE
                        set video_id = EXCLUDED.video_id
                RETURNING id;
            """,
            {
                "orig_id": orig_id,
                "video_id": video_id
            }
        )[0]["id"]

    def _create_tables(self):
        self.execute_sql(
            """
                CREATE TABLE
                    comment_threads (
                        id SERIAL PRIMARY KEY,
                        orig_id CHAR(26) NOT NULL UNIQUE,
                        video_id INTEGER REFERENCES videos(id)
                    );

                CREATE INDEX IF NOT EXISTS
                    comment_threads_video_id_idx
                ON
                    comment_threads
                        (video_id);
            """
        )

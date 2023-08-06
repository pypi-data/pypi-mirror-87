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

""" A class to save a Youtube video to the database and return its ID """


__all__ = [
    "YoutubeVideo"
]


import dateparser

from .databaseobject import (
    DatabaseObject
)
from .youtubechannel import (
    YoutubeChannel
)


#  # EXAMPLE record
#  {
#   "kind": "youtube#searchResult",
#   "etag": "\"SJZWTG6xR0eGuCOh2bX6w3s4F94/XUIrQ-4pn8OEdWxKzr87gUo0L3U\"",
#   "id": {
#    "kind": "youtube#video",
#    "videoId": "dGqZg2eeFPw"
#   },
#   "snippet": {
#    "publishedAt": "2018-12-26T08:56:17.000Z",
#    "channelId": "UC3YsVCnrtanUqE02uE7Akyw",
#    "title": "Masteran Poksai mandarin,Ngeplong vol keras",
#    "description": "Masteran poksai mandarin langsung nyaut.",
#    "thumbnails": {
#     "default": {
#      "url": "https://i.ytimg.com/vi/dGqZg2eeFPw/default.jpg",
#      "width": 120,
#      "height": 90
#     },
#     "medium": {
#      "url": "https://i.ytimg.com/vi/dGqZg2eeFPw/mqdefault.jpg",
#      "width": 320,
#      "height": 180
#     },
#     "high": {
#      "url": "https://i.ytimg.com/vi/dGqZg2eeFPw/hqdefault.jpg",
#      "width": 480,
#      "height": 360
#     }
#    },
#    "channelTitle": "KICAU NUSANTARA",
#    "liveBroadcastContent": "none"
#   }
#  }

class YoutubeVideo(DatabaseObject):
    """ A class to save a Youtube video to
        the database and return its ID
    """

    def __init__(
            self,
            video,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._name = None
        self._id = None
        self.orig_id = None

        self._parse_video_snippet(video)

    def _parse_video_snippet(self, video):
        orig_id = video["id"]["videoId"]
        channel_id = int(
            YoutubeChannel(
                video["snippet"]["channelId"],
                video["snippet"]["channelTitle"]
            )
        )
        published = dateparser.parse(
            video["snippet"]["publishedAt"]
        )
        title = video["snippet"]["title"]
        description = video["snippet"]["description"]

        self._id = self._save_to_database(
            orig_id,
            channel_id,
            published,
            title,
            description
        )
        self._name = title
        self.orig_id = orig_id

    def _save_to_database(
            self,
            orig_id,
            channel_id,
            published,
            title,
            description
    ):
        return self.execute_sql(
            """
                INSERT INTO
                    videos (
                        orig_id,
                        channel_id,
                        published,
                        title,
                        description
                    )
                    values (
                        %(orig_id)s,
                        %(channel_id)s,
                        %(published)s,
                        %(title)s,
                        %(description)s
                    )
                ON CONFLICT (orig_id)
                    DO UPDATE
                        SET
                            channel_id = EXCLUDED.channel_id,
                            published = EXCLUDED.published,
                            title = EXCLUDED.title,
                            description = EXCLUDED.description
                RETURNING id;
            """,
            {
                "orig_id": orig_id,
                "channel_id": channel_id,
                "published": published,
                "title": title,
                "description": description
            }
        )[0]["id"]

    def _create_tables(self):
        self.execute_sql(
            """
                CREATE TABLE IF NOT EXISTS
                    videos (
                        id SERIAL PRIMARY KEY,
                        orig_id CHAR(11) UNIQUE,
                        channel_id INTEGER REFERENCES channels(id),
                        published TIMESTAMP WITH TIME ZONE,
                        title TEXT,
                        description TEXT
                    );
                CREATE INDEX IF NOT EXISTS
                    videos_channel_id_idx
                ON
                    videos
                        (channel_id);

                CREATE INDEX IF NOT EXISTS
                    videos_published_idx
                ON
                    videos
                        (published);
            """
        )

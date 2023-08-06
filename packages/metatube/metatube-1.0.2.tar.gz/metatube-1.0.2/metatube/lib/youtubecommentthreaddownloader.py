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

""" A base class for downloading comment threads and comments from the
    Youtube Data API v3 """


__all__ = [
    "YoutubeCommentThreadDownloader"
]


from .youtubemetadatadownloader import (
    YoutubeMetadataDownloader
)
from .youtubecommentthread import (
    YoutubeCommentThread
)


class YoutubeCommentThreadDownloader(YoutubeMetadataDownloader):
    """ TODO
    """
    ENDPOINT = "commentThreads"

    def __init__(
            self,
            video_id,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.video_id = video_id
        self._next_page_token = None

    @property
    def _params(self):
        params = {
            "key": self._config["youtube_api_key"],
            "part": "snippet",
            "maxResults": 100,
            "textFormat": "plaintext",
            "videoId": self.video_id
        }
        if self._next_page_token is not None:
            params["pageToken"] = self._next_page_token
        return params

    def download(self, video_id=None):
        """ TODO """
        if video_id is not None:
            self.video_id = video_id

        if self.video_id is None:
            raise AttributeError(
                f"{self.__class__.__name__}.video_id is undefined"
            )

        for item in self.items:
            _ = YoutubeCommentThread(item)
            del _

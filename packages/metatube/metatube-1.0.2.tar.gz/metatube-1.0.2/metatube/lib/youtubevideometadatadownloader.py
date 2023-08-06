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

""" A base class for downloading video metadata from the
    Youtube Data API v3 """


__all__ = [
    "YoutubeVideoMetadataDownloader"
]


import datetime

import dateutil.parser

from .cache import (
    Cache
)
from .databaseobject import (
    DatabaseObject
)
from .timespan import (
    TimeSpan
)
from .youtubecommentthreaddownloader import (
    YoutubeCommentThreadDownloader
)
from .youtubemetadatadownloader import (
    YoutubeMetadataDownloader
)
from .youtubevideo import (
    YoutubeVideo
)


class YoutubeVideoMetadataDownloader(YoutubeMetadataDownloader):
    """ TODO
    """
    ENDPOINT = "search"
    DATE_FORMAT = "{:%Y-%m-%dT%H:%M:%S.000Z}"

    def __init__(
            self,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

        try:
            self.search_terms = self._config["search_terms"]
        except (KeyError, AttributeError):
            self.search_terms = None
        self._published_before = None
        self._current_gap = None

    @property
    def _already_downloaded_periods(self):
        # FIRST: transition from old cache file
        try:
            with Cache() as cache:
                earliest_record = \
                    dateutil.parser.isoparse(
                        cache[self.search_terms]["publishedBefore"]
                    )

                # `published_before` is the earliest record we have,
                # let’s find out about the latest:

                # (yes, this is slighlty dailywtf.net-worthy code,
                # but it is transitionary, after all
                latest_record = DatabaseObject().execute_sql(
                    """
                        SELECT
                            max(
                                published
                            )::TIMESTAMP WITH TIME ZONE AS published
                        FROM
                            videos
                        WHERE
                            title ILIKE %(search_terms)s
                            OR description ILIKE %(search_terms)s;
                    """,
                    {"search_terms": "%{:s}%".format(self.search_terms)}
                )[0][0]

                cache[self.search_terms]["already downloaded periods"] = [
                    TimeSpan(earliest_record, latest_record)
                ]
                del cache[self.search_terms]["publishedBefore"]
        except KeyError:
            pass

        # only THEN: retrieve cached time spans
        try:
            periods = cache[self.search_terms]["already downloaded periods"]
        except KeyError:
            periods = []

        # purge existing 0-length time spans
        periods = [
            period
            for period
            in periods
            if period.duration > datetime.timedelta(0)
        ]

        # add 0-length time periods for
        #   a) the “beginning of time” (https://youtu.be/jNQXAC9IVRw)
        #   b) NOW() (but only if end of last period is more than 10m ago)
        # (it’s the gaps we want to fill
        me_at_the_zoo = datetime.datetime(
            2005, 4, 24,
            3, 31, 52,
            tzinfo=datetime.timezone.utc
        )
        periods.append(TimeSpan(me_at_the_zoo, me_at_the_zoo))

        now = datetime.datetime.now(datetime.timezone.utc)
        if (now - max(periods).end) > datetime.timedelta(minutes=10):
            periods.append(TimeSpan(now, now))

        return sum(periods)  # sum resolves overlaps!

    @_already_downloaded_periods.setter
    def _already_downloaded_periods(self, periods):
        if len(periods) > 1:
            periods = sum(periods)
        with Cache() as cache:
            try:
                cache[self.search_terms]
            except KeyError:
                cache[self.search_terms] = {}
            cache[self.search_terms]["already downloaded periods"] = \
                periods

    @property
    def _params(self):
        periods = self._already_downloaded_periods
        first_gap = TimeSpan(periods[0].end, periods[1].start)
        self._current_gap = first_gap
        params = {
            "key": self._config["youtube_api_key"],
            "part": "snippet",
            "maxResults": 50,
            "order": "date",
            "type": "video",
            "q": self.search_terms,
            "publishedAfter": self.DATE_FORMAT.format(first_gap.start),
            "publishedBefore": self.DATE_FORMAT.format(first_gap.end)
        }
        return params

    def download(self, search_terms=None):
        """ TODO """
        if search_terms is not None:
            self.search_terms = search_terms

        if self.search_terms is None:
            raise AttributeError(
                f"{self.__class__.__name__}.search_terms is undefined"
            )

        while len(self._already_downloaded_periods) > 1:
            # until we’ve caught up completely and there’s
            # no gaps in our data collection history

            published_at = None

            for item in self.items:
                video = YoutubeVideo(item)
                YoutubeCommentThreadDownloader(video.orig_id).download()
                del video

                published_at = dateutil.parser.isoparse(
                    item["snippet"]["publishedAt"]
                )
                self._already_downloaded_periods += \
                    TimeSpan(
                        published_at,
                        self._current_gap.end
                    )

            self._already_downloaded_periods += \
                TimeSpan(
                    self._current_gap.start,
                    self._current_gap.end
                )

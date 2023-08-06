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

""" A base class for downloading metadata from the
    Youtube Data API v3 """


__all__ = [
    "YoutubeMetadataDownloader"
]


import collections
import datetime
import json
import sys
import time

import requests

from .config import (
    Config
)


class YoutubeMetadataDownloader:
    """ Base class

        TODO
    """
    API_BASE_URL = "https://www.googleapis.com/youtube/v3/{endpoint:s}"
    PST = datetime.timezone(datetime.timedelta(hours=-8))
    THUMBNAIL_BASE_URL = \
        "https://img.youtube.com/vi/{video_id:s}/maxresdefault.jpg"

    ENDPOINT = None  # override in inheriting classes

    def __init__(self, config={}):
        self._config = Config(config)
        self.search_terms = None

    @property
    def _params(self):
        raise NotImplementedError("Override self._params in child class")

    @property
    def items(self):
        """ TODO
        """
        while True:
            with requests.get(
                    self.API_BASE_URL.format(endpoint=self.ENDPOINT),
                    params=self._params
            ) as response:
                data = response.json()

                if not response.ok:
                    if (
                            data["error"]["errors"][0]["reason"]
                            in ("dailyLimitExceeded", "quotaExceeded")
                    ):
                        now_pst = datetime.datetime.now(self.PST)
                        midnight_pst = datetime.datetime(
                            year=now_pst.year,
                            month=now_pst.month,
                            day=now_pst.day,
                            tzinfo=self.PST
                        ) + datetime.timedelta(days=1)
                        wait_time_until_quota_renewal = \
                            (midnight_pst - now_pst).total_seconds()

                        print(
                            (
                                "Quota reached, " +
                                "waiting until {:%Y-%m-%d %H:%M}"
                            ).format(
                                midnight_pst.astimezone()
                            ),
                            file=sys.stderr
                        )

                        time.sleep(wait_time_until_quota_renewal + (2 * 60))
                        continue
                    elif (
                            data["error"]["errors"][0]["reason"]
                            in ("commentsDisabled",)
                    ):
                        break

                    elif (
                            data["error"]["errors"][0]["reason"]
                            in ("processingFailure", "backendError")
                    ):
                        print(
                            "API error: processing failure/backend error",
                            file=sys.stderr
                        )

                    else:
                        raise ConnectionError(
                            json.dumps(
                                data,
                                sort_keys=True,
                                indent=4
                            )
                        )

                if (
                        "items" in data
                        and isinstance(data["items"], collections.Iterable)
                        and len(data["items"]) > 1
                ):
                    # testing for len() > 1, because it seems that
                    # publishedBefore is sometimes inclusive, sometimes
                    # exclusive the filter value -> loop at “beginning of time”
                    for item in data["items"]:
                        yield item
                else:
                    # print("No data returned", file=sys.stderr)
                    break

                try:
                    self._next_page_token = data["nextPageToken"]
                except KeyError:
                    # print("Reached last page", file=sys.stderr)
                    self._next_page_token = None
                    break

        # finally, get out of the generator ;)
        return  # ~ raise StopIteration()

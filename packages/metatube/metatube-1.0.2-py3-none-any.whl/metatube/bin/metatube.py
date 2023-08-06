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

""" Search small ad listings on OLX market places """


import argparse

from ..lib.config import (
    Config
)
from ..lib.youtubevideometadatadownloader import (
    YoutubeVideoMetadataDownloader
)


def main():
    """ TODO """
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "-p",
        "--postgresql-connection-string",
        help="""Store the retrieved data in this PostgreSQL data base"""
    )

    argparser.add_argument(
        "-a",
        "--youtube-api-key",
        help="""Use this API key for the YouTube Data API v3"""
    )

    argparser.add_argument(
        "search_terms",
        help="""Query the YouTube API for these search terms"""
    )

    args = argparser.parse_args()

    _config = {}
    if args.postgresql_connection_string is not None:
        _config["connection_string"] = args.postgresql_connection_string
    if args.youtube_api_key is not None:
        _config["youtube_api_key"] = args.youtube_api_key
    if args.search_terms is not None:
        _config["search_terms"] = args.search_terms

    config = Config(_config)
    YoutubeVideoMetadataDownloader().download()
    del config

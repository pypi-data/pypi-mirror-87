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

""" A class to represent a time span, i.e. a period in time
    starting at a datetime and ending at another datetime """


__all__ = [
    "TimeSpan"
]


import datetime

import yaml


class TimeSpan(yaml.YAMLObject):
    """ A class to represent a time span, i.e. a period in time
       starting at a datetime and ending at another datetime """

    def __init__(
            self,
            start,
            end
    ):
        self.start = start
        self.end = end

    def __str__(self):
        return (
            "{:s}" +
            "({:%Y-%m-%dT%H:%M:%S.000Z}-{:%Y-%m-%dT%H:%M:%S.000Z})"
        ).format(
            self.__class__.__name__,
            self.start,
            self.end
        )

    @property
    def start(self):
        """ The start time of this time span """
        return self._start

    @start.setter
    def start(self, start):
        if not isinstance(start, datetime.datetime):
            raise TypeError("Expected datetime.datetime")
        self._start = start

    @property
    def end(self):
        """ The end time of this time span """
        return self._end

    @end.setter
    def end(self, end):
        if not isinstance(end, datetime.datetime):
            raise TypeError("Expected datetime.datetime")
        self._end = end

    @property
    def duration(self):
        """ The time between TimeSpan.start and TimeSpan.end """
        return self._end - self.start

    def __lt__(self, other):
        return self.start < other.start

    def __gt__(self, other):
        return self.end > other.end

    def __eq__(self, other):
        return (
            self.start == other.start
            and self.end == other.end
        )

    def __add__(self, other):
        if not isinstance(other, list):
            other = [other]

        # “recursively” merge all time spans in list
        not_yet_merged = sorted(other + [self])
        merged = [not_yet_merged.pop(0)]

        while not_yet_merged:
            # pop last member of merged time spans
            # and first one of still to be merged time spans
            last = merged.pop()
            new = not_yet_merged.pop(0)

            # check for overlap of the two,
            # then add one or two items to the merged list
            if last.end >= new.start:
                merged.append(
                    TimeSpan(
                        min(last.start, new.start),
                        max(last.end, new.end)
                    )
                )
            else:
                merged += [last, new]

        return merged

    def __radd__(self, other):
        if other == 0:  # default case for calling `sum()`
            return self
        return self.__add__(other)

    yaml_tag = "!TimeSpan"
    yaml_loader = yaml.SafeLoader
    yaml_dumper = yaml.SafeDumper

    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_mapping(node)
        return TimeSpan(data["start"], data["end"])

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_mapping(
            "!TimeSpan",
            (
                ("start", data.start),
                ("end", data.end)
            )
        )

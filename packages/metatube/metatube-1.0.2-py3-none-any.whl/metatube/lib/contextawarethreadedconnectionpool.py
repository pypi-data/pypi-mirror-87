#!/usr/bin/env python
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


""" A psycopg2.ThreadedConnectionPool providing a `connection()` context. """


import contextlib

import psycopg2.pool


class ContextAwareThreadedConnectionPool(psycopg2.pool.ThreadedConnectionPool):
    """ ContextAwareThreadedConnectionPool

    A psycopg2.ThreadedConnectionPool providing a `connection()` context

    Example::

        connectionPool = ContextAwareThreadedConnectionPool(
            minconn=0,
            maxconn=100,
            "dbname=foobar"
        )
        with connectionPool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                        SELECT
                            field1
                        FROM
                            table1;
                    '''
                )
                result = cursor.fetchall()
        print(result)

    """
    @contextlib.contextmanager
    def connection(self):
        """
            returns a psycopg2.connection object,
            can be used as a context manager
        """
        connection = self.getconn()
        try:
            yield connection
        finally:
            self.putconn(connection)

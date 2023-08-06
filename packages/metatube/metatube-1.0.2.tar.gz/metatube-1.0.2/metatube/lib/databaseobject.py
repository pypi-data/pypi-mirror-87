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

""" A base class for self-aware database objects """


__all__ = [
    "DatabaseObject"
]


import psycopg2
import psycopg2.errors
import psycopg2.extensions
import psycopg2.extras

from .config import (
    Config
)
from .contextawarethreadedconnectionpool import (
    ContextAwareThreadedConnectionPool
)


class DatabaseObject:
    """ Base class for “self-aware” database objects such as e.g. social
        media posts. Instances share a common (class-level) psycopg2
        connectionPool, and a common config dict (currently only
        `config["connectionString"]` is used).

        Attributes:
            _connection_pool (private, class-wide):
                holds a psycopg2.pool.ConnectionPool instance which is shared
                across all class instances
            _config (private, class-wide):
                configuration dictionary, currently only `connectionString` is
                in use

        Args:
            config (dict): configuration dictionary.
                Specify `config["connectionString"]`, has to be set
                before first call to `connection_pool()`
    """
    _connection_pool = None
    _config = None

    def __init__(self, config={}):
        super().__init__()
        self.__class__._config = Config(config)

        self._id = None
        self._name = None

        try:
            # try to access table (creates tables if they don’t exist)
            self.execute_sql(
                psycopg2.sql.SQL(
                    """
                        SELECT
                            1
                        FROM
                            {table}
                        LIMIT 1;
                    """
                ).format(
                    table=psycopg2.sql.Identifier(self._table)
                )
            )
        except AttributeError:
            pass

    def __eq__(self, other):
        try:
            own_hash = self.__hash__()
        except AttributeError:
            own_hash = hash(self)
        try:
            other_hash = other.__hash__()
        except AttributeError:
            other_hash = hash(other)
        return own_hash == other_hash

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self._name

    def __int__(self):
        try:
            _int = int(self._id)
        except TypeError:
            _int = -9999
        return _int

    def __repr__(self):
        _repr = f"<{self.__class__.__name__} ({self._name}: {self._id})>"
        return _repr

    @classmethod
    def connection_pool(cls):
        """ Returns a psycopg2.pool.ConnectionPool() object
            which is shared between instances (it’s created upon
            first call)

            Args:
                (none)
            Returns:
                :obj:`psycopg2.pool.ThreadedConnectionPool`
        """
        if cls._connection_pool is None:
            try:
                cls._connection_pool = \
                    ContextAwareThreadedConnectionPool(
                        0,
                        200,
                        cls._config["connection_string"]
                    )
            except AttributeError:
                raise AttributeError("No connection string defined")
        return cls._connection_pool

    def execute_sql(self, sql, sql_vars=(), commit=None):
        """ Runs the given SQL query

            Convenience function around getting a connection from
            connection_pool, creating a cursor and fetching results

            Args:
                sql (str): SQL query
                sql_vars (list or dict): variables to pass to
                    psycopg2.cursor().execute()

            Returns:
                mixed: results of SQL query as returned by
                    psycopg2.cursor().fetchall()
        """

        if commit is None:
            # if not specified whether query should be committed,
            # guess from the sql command

            # default: commit (safe choice, plus there’s so many more
            #          writing SQL commands to match than read-only)
            commit = True
            try:
                if sql.strip().split()[0].upper() in ("SELECT", "FETCH"):
                    commit = False
            except (KeyError, AttributeError, psycopg2.Error):
                pass

        with self.connection_pool().connection() as connection:
            with connection.cursor(
                    cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                try:
                    cursor.execute(sql, sql_vars)
                except psycopg2.errors.UndefinedTable:
                    connection.rollback()
                    self._create_tables()
                    cursor.execute(sql, sql_vars)
                try:
                    results = cursor.fetchall()
                except psycopg2.ProgrammingError as e:
                    if str(e) == "no results to fetch":
                        results = None
                    else:
                        raise e

            if commit:
                connection.commit()

        return results

    def _create_tables(self):
        raise NotImplementedError(
            "Define `self._create_tables()` to create required tables."
        ) from None

    def adapt(self):
        """ adapts self’s integer representation to be used in DB """
        return psycopg2.extensions.adapt(self.id)


psycopg2.extensions.register_adapter(
    DatabaseObject,
    DatabaseObject.adapt
)

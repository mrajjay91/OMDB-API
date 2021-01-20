#!/usr/bin/env python
# -- coding: utf-8 --
"""
Connection manager for postgresdb
"""

from sqlalchemy.pool import NullPool
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class PostgresDB:
    def _init_(self, host, port, username, password, db):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db = db

    def get_engine(self):
        """
        create sqlalchemy postgres engine
        :return:
        """
        engine = create_engine("postgresql://{}:{}@{}/{}".format(self.username, self.password, self.host, self.db),
                               poolclass=NullPool, pool_pre_ping=False)
        return engine

    def get_session(self):
        """
        create the postgres session object.
        :return: db session
        """
        engine = self.get_engine()
        session = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False, autocommit=False)()
        return session

    def get_client(self):
        """
        client to connect with postgres
        :return: postgres client
        """
        connection = psycopg2.connect(user=self.username, password=self.password, host=self.host, port=self.port,
                                      database=self.db)

        client = connection.cursor()
        return client

    def create_table(self, table):
        """
        Create table if not exists
        :param table:
        :return:
        """
        engine = self.get_engine()
        table._table_.create(bind=engine, checkfirst=True)

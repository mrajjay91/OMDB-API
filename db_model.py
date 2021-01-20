#!/usr/bin/env python
# -- coding: utf-8 --

from sqlalchemy import Column, Integer, JSON, Sequence, VARCHAR, DATE, String
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()


class Entertainment(Base):
    """
    This is a entertainment staging table base schema
    """
    _tablename_ = 'entertainment_staging'

    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    title = Column(VARCHAR(150), nullable=False)
    year = Column(VARCHAR(10), nullable=False)
    released = Column(DATE, nullable=False)
    runtime = Column(VARCHAR(25), nullable=False)
    plot = Column(String)
    poster = Column(String)
    genre = Column(VARCHAR(500), nullable=False)
    director = Column(VARCHAR(500), nullable=False)
    actors = Column(String)
    writer = Column(String)
    language = Column(VARCHAR(500), nullable=False)
    country = Column(VARCHAR(500), nullable=False)
    production = Column(VARCHAR(250), nullable=False)
    ratings = Column(JSON)
    rated = Column(VARCHAR(20), nullable=False)
    type = Column(VARCHAR(10), nullable=False)
    awards = Column(VARCHAR(250))
    metascore = Column(VARCHAR(20))
    imdb_rating = Column(VARCHAR(5))
    imdb_votes = Column(VARCHAR(25))
    imdb_id = Column(VARCHAR(10))
    box_office = Column(VARCHAR(25))
    website = Column(VARCHAR(25))
    dvd = Column(VARCHAR(25))
    total_seasons = Column(VARCHAR(10))

    def _repr_(self):
        """
        returns a entertainment object
        :return: str: db records
        """
        return json.dumps({
            "id": str(self.id),
            "title": self.title,
        })

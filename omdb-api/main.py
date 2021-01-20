from base_api import BaseAPI
from postgres import PostgresDB
import os
import sys
import argparse
import logging
from sqlalchemy import exc
from requests.exceptions import HTTPError
from db_model import Entertainment

logging.basicConfig(level=logging.INFO)


def get_env(key):
    """
    Get value of environment variable
    :param key:
    :return:
    """
    try:
        env_var = os.environ[key]
    except KeyError:
        logging.error("Please set the environment variable {}".format(key))
        sys.exit(1)
    return env_var


def insert_data(sql_db, response):
    """
    Insert data into staging table
    :param sql_db:
    :param response:
    :return:
    """
    try:
        # Insert data into the staging table
        session = sql_db.get_session()

        entertainment = Entertainment(title=response['Title'], year=response['Year'], rated=response['Rated'],
                                      released=response['Released'], runtime=response['Runtime'], genre=response['Genre'],
                                      director=response['Director'], actors=response['Actors'], writer=response['Writer'],
                                      plot=response['Plot'], language=response['Language'], country=response['Country'],
                                      awards=response['Awards'], poster=response['Poster'], ratings=response['Ratings'],
                                      metascore=response['Metascore'], imdb_rating=response['imdbRating'],
                                      imdb_votes=response['imdbVotes'], imdb_id=response['imdbID'], type=response['Type'],
                                      dvd=response.get('DVD', ''), box_office=response.get('BoxOffice', ''),
                                      production=response.get('Production', ''), website=response.get('Website', ''),
                                      total_seasons=response.get('totalSeasons', ''))

        # Add it to the table if it does not exist
        result = session.query(Entertainment).filter_by(title=response['Title']).first()
        if not result:
            logging.info(
                'Information for {} does not exist in the staging table, hence adding it'.format(response['Title']))
            session.add(entertainment)
            session.commit()
        else:
            logging.info('Information already exists in the staging table for {}'.format(response['Title']))
        # close session
        session.close()

    except exc.SQLAlchemyError as e:
        logging.error("Failed to insert data into staging table {}".format(e))
        sys.exit(1)
    except:
        logging.error("Unexpected exception, failed to insert data into staging table")
        sys.exit(1)


def create_staging_table(sql_db):
    """
    Create staging table if it does not exist
    :param sql_db:
    :return:
    """
    try:
        sql_db.create_table(Entertainment)
        logging.info('Created staging table')
    except exc.SQLAlchemyError as e:
        logging.error("Failed to create staging table {}".format(e))
        sys.exit(1)
    except:
        logging.error("Unexpected exception, failed to create staging table")
        sys.exit(1)


def main(movie_series_name):
    """
    Main method to request data from the API and insert into staging table
    :param movie_series_name:
    :return:
    """
    logging.info("Accessing OMDB API for {}".format(movie_series_name))

    # Get API KEY
    api_key = get_env('API_KEY')

    params = dict(t=movie_series_name, apikey=api_key)
    url = 'http://www.omdbapi.com/'

    # Get request
    try:
        api = BaseAPI(url=url, params=params)
        response = api.get_request()
    except HTTPError as http_err:
        logging.error(http_err)
    except Exception as err:
        logging.error(err)

    if response['Response'] == 'True':
        logging.info("Response from the API is {}".format(response))
        # Get DB connection information
        db_host = get_env('DB_HOST')
        db_port = get_env('DB_PORT')
        db_username = get_env('DB_USERNAME')
        db_password = get_env('DB_PASSWORD')
        db_name = get_env('DB_NAME')

        sql_db = PostgresDB(host=db_host, port=db_port, username=db_username, password=db_password, db=db_name)

        # Create staging table if it does not exist
        create_staging_table(sql_db)

        # Insert data to staging table
        insert_data(sql_db, response)

    else:
        logging.info(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve and store information about movies/series')
    parser.add_argument('--name', type=str, help='The name of the movie/series whose information is to be '
                                                 'retrieved and stored')
    args = parser.parse_args()
    if args.name:
        main(args.name)
    else:
        logging.error("Expected one argument --name. Please specify a movie/series name whose information you would "
                      "like to retrieve and store")

#OMDB API

Information about the API - http://www.omdbapi.com/

This application only supports retrieving information by movie/series name.

Generate API key here - http://www.omdbapi.com/apikey.aspx

Send all data requests to:

>http://www.omdbapi.com/?t=[name]&apikey=[yourkey]

## Usage
Set the following environment variables, we can also use a secret store like vault to store the below.

> API_KEY
>
> DB_HOST
>
> DB_PORT
>
> DB_USERNAME
>
> DB_PASSWORD
>
> DB_NAME
>

## Options

> python main.py --h

usage: main.py [-h] [--name NAME]

Retrieve and store information about movies/series

optional arguments:
  -h, --help   show this help message and exit
  --name NAME  The name of the movie/series whose information is to be
               retrieved and stored


> python main.py --name='the black swan'

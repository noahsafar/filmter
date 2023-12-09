import os
import requests
import numpy as np

from flask import redirect, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def fetch_movies(keywords):
    base_url = "https://api.themoviedb.org/3/search/movie"
    api_key = "d100489f1424caa88885c6a59ec7caec"

    params = {
        "api_key": api_key,
        "query": keywords,
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        movies = response.json()["results"]

        # Filter through movie database based on the appearance of the user's keywords in the movie title and/or overview
        filtered_movies = []
        for movie in movies:
            if (
                keywords.lower() in movie["title"].lower()
                or keywords.lower() in movie["overview"].lower()
            ):
                filtered_movies.append(movie)

        # Sort filtered movies alphabetically based on movie titles
        filtered_movies.sort(key=lambda x: x["title"].lower())

        return filtered_movies
    else:
        # Handle request failure
        return None

# tmp libraries
from pprint import pprint
# end tmp libraries

import os
from .modules import TmdbMovie
from .models import Movie
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import requests
from dotenv import load_dotenv, dotenv_values


def get_all_movies_from_tmdb(request):
    load_dotenv()
    tmdb_api_key = os.getenv('TMDB_API_KEY')

    for id in range(11, 12):
        URL = f'https://api.themoviedb.org/3/movie/{id}?api_key=fd99d2b1c23f6f04fe6697ee24cbabc9&language=ko&region=KR'
        res = requests.get(URL)

        # existed movies only
        if res.status_code == 200:
            data = res.json()
            movie = TmdbMovie(data)
            movie.create_movie()
            print(f'{movie.id} 생성 완료')

    data = {
        'title': 1,
        'name': 2,
    }
    return JsonResponse(data)
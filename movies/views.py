# tmp libraries
from pprint import pprint
# end tmp libraries

import os

from .modules import TmdbMovie
from .models import Movie, Movie_User
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django_seed import Seed

import random
import requests
from dotenv import load_dotenv, dotenv_values

def get_all_movies_from_tmdb(request):
    load_dotenv()
    tmdb_api_key = os.getenv('TMDB_API_KEY')

    for id in range(50):
        URL = f'https://api.themoviedb.org/3/movie/{id}?api_key=fd99d2b1c23f6f04fe6697ee24cbabc9&language=ko&region=KR'
        res = requests.get(URL)

        # existed movies only
        if res.status_code == 200:
            data = res.json()
            movie = TmdbMovie(data)
            movie.create_movie()
            print(f'{movie.id} 생성 완료')

    data = {
        'success': True,
    }
    return JsonResponse(data)


def get_seed_rating(request):
    rate_numbers = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    movie_ids = [2,3,5,6,8,9,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,30,31,32,33,35,38]

    seeder = Seed.seeder()
    
    seeder.add_entity(Movie_User, 400, {
        'user': lambda x: get_object_or_404(get_user_model(), pk=random.randint(1, 100)),
        'movie': lambda x: get_object_or_404(Movie, pk=movie_ids[random.randint(0, 28)]),
        'rating': lambda x: rate_numbers[random.randint(0, 9)],
    })
    seeder.execute()

    data = {
        'success': True
    }
    return JsonResponse(data)
    
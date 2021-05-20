import sys
sys.path.append('..')

from movies.models import Genre_User, Genre
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


class UserSupport():
    
    def __init__(self, user):
        self.user = user

    def set_genre_user(self):
        genre_id_list = [12, 14, 16, 18, 27, 35, 36, 37, 53, 80, 99, 878, 9648, 10402, 10749, 10751, 10752]
        for genre_id in genre_id_list:
            genre = get_object_or_404(Genre, pk=genre_id)
            
            genre_user, created = Genre_User.objects.get_or_create(
                user = self.user,
                genre = genre,
            )
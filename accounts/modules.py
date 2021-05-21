import sys
sys.path.append('..')

from movies.models import Genre_User, Genre
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404


class UserSupport():
    
    def __init__(self):
        pass

    def set_genre_user(self, user):
        genre_ids = [12, 14, 16, 18, 27, 28, 35, 36, 37, 53, 80, 99, 878, 9648, 10402, 10749, 10751, 10752]
        for genre_id in genre_ids:
            genre = get_object_or_404(Genre, pk=genre_id)
            
            genre_user, created = Genre_User.objects.get_or_create(
                user = user,
                genre = genre,
            )

    def set_ranking(self):
        users = get_user_model().objects.all().order_by('-point')

        tmp_i = 0
        tmp_p = 0
        for i in range(len(users)):
            user = users[i]
            p = user.point
            if i == 0:
                user.ranking = i+1
                user.save()
                tmp_i = i+1
                tmp_p = p
            else:
                if p == tmp_p:
                    user.ranking = tmp_i
                    user.save()
                else:
                    user.ranking = i+1
                    user.save()
                    tmp_i = i+1
                    tmp_p = p

        users = get_user_model().objects.all().order_by('ranking')  
        return users
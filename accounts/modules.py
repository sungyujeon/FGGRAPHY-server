import sys
sys.path.append("..")

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
from movies.models import Genre, Genre_User


class UserSupport():
    
    def __init__(self):
        pass

    def calc_tier(self, r, tier1, tier2, tier3, tier4):
        if 1 < r <= tier1:
            return 1
        elif r <= tier2:
            return 2
        elif r <= tier3:
            return 3
        elif r <= tier4:
            return 4
        else:
            return 5

    def set_ranking(self):
        users = get_user_model().objects.all().order_by('-point')

        # tier 계산
        total_users = len(users)
        tier_1 = int(total_users * 0.15)
        tier_2 = int(total_users * 0.3)
        tier_3 = int(total_users * 0.45)
        tier_4 = int(total_users * 0.6)

        tmp_i = 0
        tmp_p = 0
        for i in range(len(users)):
            user = users[i]
            p = user.point
            if i == 0:
                user.ranking = i+1
                user.tier = i
                user.save()
                tmp_i = i+1
                tmp_p = p
            else:
                if p == tmp_p:
                    user.ranking = tmp_i
                    t = self.calc_tier(tmp_i, tier_1, tier_2, tier_3, tier_4)
                    user.tier = t
                    user.save()
                else:
                    user.ranking = i+1
                    t = self.calc_tier(i+1, tier_1, tier_2, tier_3, tier_4)
                    user.tier = t
                    user.save()
                    tmp_i = i+1
                    tmp_p = p

        users = get_user_model().objects.all().order_by('ranking')  
        return users

    
    def set_genre_user(self, user):
        genre_ids = [12, 14, 16, 18, 27, 28, 35, 36, 37, 53, 80, 99, 878, 9648, 10402, 10749, 10751, 10752]
        for genre_id in genre_ids:
            genre = get_object_or_404(Genre, pk=genre_id)
            
            genre_user, created = Genre_User.objects.get_or_create(
                user = user,
                genre = genre,
            )
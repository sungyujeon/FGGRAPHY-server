from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


urlpatterns = [
    path('signup/', views.signup),
    path('api-token-auth/', obtain_jwt_token),
    path('api-toekn-refresh/', refresh_jwt_token),
    path('top-ranked/', views.get_top_ranked_users),
    path('api-token-verify', verify_jwt_token),
    
    # admin
    path('calc-ranking/', views.calc_ranking),

    # user-profile
    path('profile/<str:username>/', views.get_or_update_or_delete_user),
    path('profile/<str:username>/follow/', views.follow),
    
]
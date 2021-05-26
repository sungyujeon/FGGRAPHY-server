from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password',)

class UserDataSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(source='review_set.count', read_only=True)
    review_avg = serializers.FloatField(source='movie_user_rating_set.avg', read_only=True)
    class Meta:
        model = User
        fields = ('username', 'point', 'ranking', 'tier', 'review_count', 'review_avg')
        
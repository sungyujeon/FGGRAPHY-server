from django.contrib import admin
from .models import Movie, Genre, BelongsToCollection, ProductionCompany, ProductionCountry, SpokenLanguage

admin.site.register([
    Movie,
    Genre,
    BelongsToCollection,
    ProductionCompany,
    ProductionCountry,
    SpokenLanguage,
])
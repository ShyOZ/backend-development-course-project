from django.contrib import admin

from .models import Movie, MovieInfo

admin.site.register(Movie)
admin.site.register(MovieInfo)
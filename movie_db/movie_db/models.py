from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    poster = models.ImageField(upload_to="posters")

    def __str__(self):
        return self.title


class MovieInfo(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="movie_info"
    )

    director = models.CharField(max_length=200)

    actor1 = models.CharField(max_length=50)
    actor2 = models.CharField(max_length=50)
    actor3 = models.CharField(max_length=50)
    actor4 = models.CharField(max_length=50)

    year = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"info about {self.movie.title}"

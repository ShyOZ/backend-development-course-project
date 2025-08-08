from django.contrib.auth.models import User
from django.db import models


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


class Review(models.Model):
    RATING_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_text = models.TextField(
        blank=True, help_text="Share your thoughts about this movie"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "movie"], name="one_per_user_per_movie")
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}'s review of {self.movie.title} - {self.rating}/5"

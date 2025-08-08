from django.contrib import admin

from .models import Movie, MovieInfo, Review


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'description_preview', 'has_poster', 'has_movie_info']
    list_filter = ['movie_info__year']
    search_fields = ['title', 'description']
    
    @admin.display(description="Description")
    def description_preview(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    
    @admin.display(boolean=True, description='Has Poster')
    def has_poster(self, obj):
        return bool(obj.poster)
    
    @admin.display(boolean=True, description='Has Details')
    def has_movie_info(self, obj):
        return hasattr(obj, 'movie_info') and obj.movie_info.exists()


@admin.register(MovieInfo)
class MovieInfoAdmin(admin.ModelAdmin):
    list_display = ['movie', 'director', 'year', 'main_actors_preview']
    list_filter = ['year', 'director']
    search_fields = ['movie__title', 'director', 'actor1', 'actor2', 'actor3', 'actor4']
    
    @admin.display(description='Main Actors')
    def main_actors_preview(self, obj):
        actors = [actor for actor in [obj.actor1, obj.actor2, obj.actor3, obj.actor4] if actor]
        return ', '.join(actors[:2]) + ('...' if len(actors) > 2 else '')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'movie']
    search_fields = ['movie__title', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
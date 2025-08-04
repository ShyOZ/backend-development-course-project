from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    # Movie URLs
    path("", views.home, name="home"),
    path("movie/<int:movie_id>/", views.movie_info, name="movie_info"),
]

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
    # Review URLs
    path("movie/<int:movie_id>/review/add/", views.add_review, name="add_review"),
    path("movie/<int:movie_id>/review/edit/", views.edit_review, name="edit_review"),
    path("movie/<int:movie_id>/review/delete/", views.delete_review, name="delete_review"),
]

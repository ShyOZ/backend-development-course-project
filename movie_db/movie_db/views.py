from django.contrib import messages
from django.contrib.auth import login as _login, logout as _logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from .forms import CustomLoginForm, CustomSignupForm
from .models import Movie, MovieInfo


@never_cache
@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            _login(request, user)

            if not form.cleaned_data.get("remember_me"):
                request.session.set_expiry(0)

            messages.success(request, f"Welcome back, {user.username}!")

            next_page = request.GET.get("next", "home")
            return redirect(next_page)
    else:
        form = CustomLoginForm()

    context = {"form": form, "title": "Login to Movie Database"}
    return render(request, "login.html", context)


@never_cache
@require_http_methods(["GET", "POST"])
def signup_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomSignupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]

            if User.objects.filter(username=username).exists():
                form.add_error("username", "This username is already taken.")
            else:
                user = form.save()

                _login(request, user)

                messages.success(
                    request,
                    f"Welcome to Movie Database, {user}! Your account has been created successfully.",
                )
                return redirect("home")
    else:
        form = CustomSignupForm()

    context = {"form": form, "title": "Join Movie Database"}
    return render(request, "signup.html", context)


@require_http_methods(["GET", "POST"])
def logout_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        username = request.user.username
        _logout(request)
        messages.info(
            request, f"You have been logged out successfully. See you soon, {username}!"
        )

    return redirect("home")


@require_http_methods(["GET"])
def home(request: HttpRequest) -> HttpResponse:
    movies = Movie.objects.select_related().order_by("-id")

    # statistics for sidebar
    total_movies = Movie.objects.count()
    total_users = User.objects.count()

    context = {
        "movies": movies,
        "total_movies": total_movies,
        "total_users": total_users,
        "title": "Movie Database",
    }
    return render(request, "home.html", context)


@require_http_methods(["GET"])
def movie_info(request: HttpRequest, movie_id: int) -> HttpResponse:
    movie = get_object_or_404(Movie, id=movie_id)

    # Get movie info if it exists
    try:
        movie_details = movie.movie_info.get()
    except MovieInfo.DoesNotExist:
        movie_details = None

    context = {
        "movie": movie,
        "movie_details": movie_details,
        "title": f"{movie.title} - Movie Database",
    }
    return render(request, "movie_detail.html", context)

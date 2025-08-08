from django.contrib import messages
from django.contrib.auth import login as _login, logout as _logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from .forms import CustomLoginForm, CustomSignupForm, ReviewForm
from .models import Movie, MovieInfo, Review


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

    # Get all reviews for this movie
    reviews = movie.reviews.select_related('user').all()
    
    # Get user's existing review if logged in
    user_review = None
    if request.user.is_authenticated:
        try:
            user_review = movie.reviews.get(user=request.user)
        except Review.DoesNotExist:
            pass
    
    # Calculate average rating
    total_reviews = reviews.count()
    average_rating = None
    if total_reviews > 0:
        total_rating = sum(review.rating for review in reviews)
        average_rating = round(total_rating / total_reviews, 1)

    context = {
        "movie": movie,
        "movie_details": movie_details,
        "reviews": reviews,
        "user_review": user_review,
        "total_reviews": total_reviews,
        "average_rating": average_rating,
        "title": f"{movie.title} - Movie Database",
    }
    return render(request, "movie_detail.html", context)


@login_required
@require_http_methods(["POST"])
def add_review(request: HttpRequest, movie_id: int) -> HttpResponse:
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Check if user already has a review for this movie
    if Review.objects.filter(user=request.user, movie=movie).exists():
        messages.error(request, "You have already reviewed this movie. You can edit your existing review.")
        return redirect("movie_info", movie_id=movie_id)
    
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.movie = movie
        review.save()
        
        messages.success(request, f"Your review for '{movie.title}' has been added successfully!")
    else:
        messages.error(request, "Please correct the errors in your review.")
    
    return redirect("movie_info", movie_id=movie_id)


@login_required
@require_http_methods(["POST"])
def edit_review(request: HttpRequest, movie_id: int) -> HttpResponse:
    movie = get_object_or_404(Movie, id=movie_id)
    review = get_object_or_404(Review, user=request.user, movie=movie)
    
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
        form.save()
        messages.success(request, f"Your review for '{movie.title}' has been updated successfully!")
    else:
        messages.error(request, "Please correct the errors in your review.")
    
    return redirect("movie_info", movie_id=movie_id)


@login_required
@require_http_methods(["POST"])
def delete_review(request: HttpRequest, movie_id: int) -> HttpResponse:
    movie = get_object_or_404(Movie, id=movie_id)
    review = get_object_or_404(Review, user=request.user, movie=movie)
    
    review.delete()
    messages.success(request, f"Your review for '{movie.title}' has been deleted.")
    
    return redirect("movie_info", movie_id=movie_id)

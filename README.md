# Backend Development Course - Course Project

***The project and this file will be updated as the course progresses***

## The Subject
Building a [Django](https://www.djangoproject.com) web application that serves as a movie database system. Users can register, authenticate, browse movies, and write reviews with ratings.

## The Concepts
This project consolidates all Django concepts learned throughout the course by implementing a full-featured web application. The main features include:
1. User authentication system with custom login and signup forms
2. Movie database with image upload capabilities
3. Movie review system with 1-5 star ratings and text reviews
4. User session management and access control
5. CRUD operations for movie management (admin panel only)
6. Template inheritance and dynamic content rendering
7. Media file handling for movie posters

The project demonstrates Django's Model-View-Template (MVT) architecture, database relationships, form handling, user authentication, and media file management.

## The Tools
- [**Django Framework**](https://www.djangoproject.com): The core web framework providing authentication, ORM, templating, and URL routing.
- [**Pillow**](https://pillow.readthedocs.io/): Python Imaging Library for handling image uploads and processing movie posters.
- [**SQLite Database**](https://www.sqlite.org/): Default Django database for storing user accounts, movie information, and relationships.
- [**Django Forms**](https://docs.djangoproject.com/en/5.2/topics/forms/): Custom form classes for user authentication and movie data input with validation.
- [**Django Authentication System**](https://docs.djangoproject.com/en/5.2/topics/auth/): Built-in user management with custom login/signup views and session handling.
- [**Django Template Language**](https://docs.djangoproject.com/en/5.2/ref/templates/language/): Template inheritance system with base templates and dynamic content rendering.
- [**Django Media Handling**](https://docs.djangoproject.com/en/5.2/howto/static-files/): Configuration for uploading, storing, and serving movie poster images.

<br/><br/>

The project's virtual environment and dependencies are managed using [**uv**](https://docs.astral.sh/uv/), with dependencies defined in `pyproject.toml` and `requirements.txt`.

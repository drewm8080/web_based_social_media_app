# Web Based Blogging Application Documentation

## Introduction

This documentation provides an overview of a Flask-based web application designed for blogging, including its setup, user forms, database models, routes, and HTML templates.

## Setup and Initialization

- **File**: `__init__.py`
- **Description**: Initializes Flask app with configurations for SQLAlchemy, Flask-Login, and Bcrypt.

## User Forms

- **File**: `forms.py`
- **Description**: Defines forms for registration, login, account updates, and post creation using Flask-WTF.

## Database Models

- **File**: `models.py`
- **Description**: Outlines `User` and `Post` models for the database schema.

## Application Routes

- **File**: `routes.py`
- **Description**: Manages application routes for user authentication, profile management, and post operations.

## HTML Templates

HTML templates provide the structure and layout for the application's web pages.

- **Layout Template**: `layout.html` - The base template for the application.
- **Home Page**: `home.html` - Displays all blog posts.
- **About Page**: `about.html` - Provides information about the application.
- **Login Page**: `login.html` - For user login.
- **Registration Page**: `register.html` - For new user registration.
- **Account Page**: `account.html` - Allows users to update their profile.
- **Create Post Page**: `create_post.html` - For creating new blog posts.
- **Post Detail Page**: `post.html` - Displays a single post in detail.

## Features

- Comprehensive user registration and login.
- Profile and account management.
- Blog post creation, editing, and deletion.

## Conclusion

This Flask application offers a platform for blogging with user authentication, profile management, and post handling, showcasing Flask's capabilities in web development.

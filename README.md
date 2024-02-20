# Web Based Blogging Application Documentation

## Introduction

This documentation provides an overview of a Flask-based web application designed for blogging. It covers the application's setup, user forms, database models, and routes.

## Setup and Initialization

- **File**: `__init__.py`
- **Description**: Initializes Flask app with configurations for SQLAlchemy, Flask-Login, and Bcrypt for secure password handling.

## User Forms

- **File**: `forms.py`
- **Description**: Defines user interaction forms using Flask-WTF, including user registration, login, account updates, and post creation forms.

## Database Models

- **File**: `models.py`
- **Description**: Contains `User` and `Post` models, detailing the database schema for storing user profiles and blog posts.

## Application Routes

- **File**: `routes.py`
- **Description**: Specifies the application's routes for displaying pages, handling user authentication, account management, and blog post operations.

## Features

- User registration and login system.
- Profile management for updating user details.
- Functionality for creating, updating, and deleting blog posts.

## Conclusion

This Flask application provides a comprehensive platform for blogging, including user management and post interactions, demonstrating the capabilities of Flask and its extensions in web development.

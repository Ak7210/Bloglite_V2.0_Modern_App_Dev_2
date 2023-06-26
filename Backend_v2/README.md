# Bloglite 
    Welcome to Bloglite-
        It is a blogging application that allows users to post, edit, save, view, like and comment blog posts.

# Features
    * User Authentication
    * Create, Edit and Delete the Blog
    * View the Friends Blogs and post comments on the blogs.
    * Daily reminder
    * Monthly Report
    * Caching
    * Export blogs in csv format

# Requirements
    * Requirements for the project are listed in the requirements.txt file.

# Installation
    * make a copy of the backend and then run the wsl in windows
    * install all the requirements which is written in requirements.txt
        ```sh
            pip install requirements.txt

    * run the python app
        ```sh
            python app.py

    * run the redis server
        ```sh
            redis-server

    * run the celery worker
        ```sh
            celery -A app.celery worker --loglevel=info

    * run the celery beat
        ```sh
            celery -A app.celery beat --loglevel=info

    * Finally run mailhog
        ```sh
            install it from browser
            then run it.

## Usage
    Run the frontend and enjoy the blogging!


Cinova video content library management system.

This project is a Django web application for managing a library of movies and TV series.

_______________________________________________________________________________________________________________________________________________________________

Preview: 
![photo_2023-11-10_20-15-18](https://github.com/zubkovoleg01/cinova/assets/120819704/34f7ccea-1bba-465a-9c84-9745cac3db8e)

_______________________________________________________________________________________________________________________________________________________________

● Registration and authentication:

Users can register and authenticate in the system.

● User profiles:

Users have their own profiles with the ability to edit.

● Content:

Added a large library of movies, TV series and other content by criteria: new, popular, random, whatever. The type of which can be changed depending on the required goals.

● Reviews:

A large database of ratings and reviews has been created for each film and TV series.

● System of reviews and ratings:

Users can leave reviews, rate movies and TV shows.

● List management:

Users add and remove content from favorites.

● Banner:

Administrators have the ability to add, remove and change banners on the home page.

● Search:

Added the ability to search for content by keywords.

● Genres:

Added the ability to sort content by different genres.

● Recommendation content:

Offer of several films.

● Pagination:

Ability to switch pages.

● Details:

Added trailers, viewing methods, actors, similar movies and other necessary information.


_______________________________________________________________________________________________________________________________________________________________

Deployment Instructions

● Installing dependencies:

pip install -r requirements.txt

● Creating migrations and applying:

python manage.py makemigrations
python manage.py migrate

● Creating a superuser (for the administrative panel):

python manage.py createsuperuser

● Starting the server:

python manage.py runserver

● Administrative panel:

Go to http://localhost:8000/admin and log in using the superuser credentials.

● Adding Movies and Tv Shows:

In the admin panel, you can add and edit information about movies and TV shows.

● Documentation of the Kinopoisk API (optional):

Documentation of the Kinopoisk API

_______________________________________________________________________________________________________________________________________________________________


# Theatre-API-mate

Project of "Theatre service API".
You can managing  with actors, genres, plays,
performances, reservations tickets.

This project was written on Django Rest-framework.

# Installing

You can use this commands to install project on you own localhost

* Install PostgreSQL and create a database
```shell
git clone https://github.com/Bloodviel/Theatre-API-mate.git
cd theatre_api
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```
* Create .env file in base directory
* Fill .env file with data
```shell
POSTGRES_HOST=YOUR_HOST
POSTGRES_DB=YOUR_DB
POSTGRES_USER=YOUR_USER
POSTGRES_PASSWORD=YOUR_PASSWORD
DJANGO_SECRET_KEY=YOUR_SECRET_KEY
```
* Makemigrations
* Use "python manage.py runserver" to start

# Run project with docker

* Download [Docker](https://www.docker.com/products/docker-desktop/)
* Run commands:
```shell
docker build
docker-compose up
```

# To use authenticate system

* Download [ModHeader](https://chrome.google.com/webstore/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj?hl=en)
* /api/user/register - to create user
* /api/user/token - to get token

# Features

* JSON Web Token authenticated
* Documentation /api/doc/swagger/
* Creating genres, actors, plays, theatre halls
* Managing plays, tickets and reserve them
* Filtering plays by date, title
* Filtering performances by title, actors, genres
* Adding performances

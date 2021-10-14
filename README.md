# Car API - Python, Django, REST

This is a simple REST Api created for Netguru's application process.

----

# Requirements

* Python 3

I **highly suggest** grabbing the latest release of Python available at the time and starting the project in a virtual environment, as per the instruction below.

# Installation

Clone the repository...

    git clone https://github.com/pkecerski/CarAPI.git

Set up a virtual environment in your desired directory and start it...

    python3 -m venv venv
    source venv/bin/activate

Install modules using `pip`...

    pip install -r requirements.txt

Create a new database...

    sqlite3 db.db

Make your migrations...
    
    python manage.py makemigrations
    python manage.py migrate

Create a new superuser...

    python manage.py createsuperuser

Check if it works...

    python manage.py runserver

This should provide you with a localhost address, where the app will run.
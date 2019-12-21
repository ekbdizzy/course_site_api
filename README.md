## Django Rest Framework API
Simple API for site with courses on DRF.
Samples of using on main page. User model is changed to custom, USERNAME = email.

### Requirements:
~~~~
pip install -r requirements.txt
~~~~

### Create and fill database
~~~~
python manage.py makemigrations
python manage.py migrate
python manage.py fill_db  # create models for categories and products using factory_boy 
~~~~



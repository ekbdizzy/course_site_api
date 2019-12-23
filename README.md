## Django Rest Framework API
Simple API for site with courses on DRF.
Samples of using on main page. <br>User model is changed to custom, USERNAME = email.

### Requirements:
~~~~
pip install -r requirements.txt
~~~~

You need also RabbitMQ for Celery: https://www.rabbitmq.com/
~~~~
rabbitmq-server
~~~~

### Create and fill database
~~~~
python manage.py fill_db  # create models for categories and products using factory_boy 
~~~~



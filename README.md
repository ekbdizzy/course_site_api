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

### Tests
~~~
sh runtest.sh  # result in console
sh runtest_html.sh  # full result in html (./htmlcov/)
~~~

### API request samples

Get list with all courses (GET)
~~~
localhost:8000/api/course/list
~~~

Detail view to course by id (GET)
~~~
localhost:8000/api/course/detail/<course_id:int>
~~~

Register new user (POST)
~~~
url: localhost:8000/api/user/register

request: { "full_name": "Aleksey",
           "email": "aleksey@mail.ru",
           "password": "password" }
~~~
Login user (POST)
~~~
url: localhost:8000/api/user/login

request: { "email": "aleksey@mail.ru",
           "password": "password" }
~~~
All students on course (GET)
~~~
localhost:8000/api/course/detail/(course_id:int)/students
~~~ 
Add student to course (POST)
~~~
url: localhost:8000/api/course/detail/(course_id:int)/students

request: { "email": "aleksey@mail.ru" }
~~~

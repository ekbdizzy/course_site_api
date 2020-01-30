cp course_site/sample_env.py course_site/my_env.py
python manage.py makemigrations user course lesson
python manage.py migrate
echo "making fake data in db"
python manage.py fill_db
python manage.py collectstatic
python manage.py runserver 0.0.0.0:8000
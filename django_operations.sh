ls
pwd
sleep 5s
python manage.py makemigrations user course lesson
python manage.py migrate
echo "making fake data in db"
python manage.py fill_db
python manage.py collectstatic
echo "create django superuser"
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
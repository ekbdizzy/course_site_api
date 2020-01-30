docker-compose build
echo "********************************"
docker-compose run web python manage.py makemigrations user course lesson && \
docker-compose run web python manage.py migrate
echo "making fake data in db"
docker-compose run web python manage.py fill_db
docker-compose run web python manage.py collectstatic
echo "create django superuser"
docker-compose run web python manage.py createsuperuser
docker-compose up
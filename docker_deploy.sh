docker-compose build
docker-compose run web python manage.py makemigrations user course lesson
docker-compose run web manage.py migrate
docker-compose run manage.py fill_db
docker-compose run manage.py collectstatic -y
docker-compose run manage.py createsuperuser
docker-compose up
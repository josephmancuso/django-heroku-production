cd ..
call pip install -r requirements.txt
call python manage.py collectstatic
call python manage.py makemigrations
call python manage.py migrate

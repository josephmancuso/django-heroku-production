cd ..
rem call pip install -r requirements.txt
call python manage.py makemigrations
call python manage.py migrate
call python manage.py runserver

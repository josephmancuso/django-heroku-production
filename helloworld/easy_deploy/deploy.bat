cd ..
call heroku login
SET ran=%RANDOM%
call heroku create restsaas%ran%
call heroku git:remote -a restsaas%ran%
call git init
call git add .
call git status
call git commit -m "Heroku Commit"
call git push heroku master
call heroku pg:reset DATABASE_URL --confirm restsaas%ran%
call heroku run python manage.py makemigrations
call heroku run python manage.py migrate
call heroku run python manage.py createsuperuser
call heroku open /admin

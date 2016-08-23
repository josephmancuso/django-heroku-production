cd ..
call heroku login
SET ran=%RANDOM%
call heroku create app%ran%
call heroku git:remote -a app%ran%
call git init
call git add .
call git status
call git commit -m "Heroku Commit"
call git push heroku master
call heroku pg:reset DATABASE_URL --confirm app%ran%
call heroku run python manage.py makemigrations
call heroku run python manage.py migrate
call heroku run python manage.py createsuperuser
call heroku open /admin

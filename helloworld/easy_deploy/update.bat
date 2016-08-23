cd ..
call git add .
call git status
git commit -C Head
call git push heroku master --force
call heroku open
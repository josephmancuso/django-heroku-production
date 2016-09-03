# BASIC Production Ready Django Application

This repo allows anyone to clone this repo, then set up their Django application to deploy to heroku FAST. I wanted to make something
where I just had to change 1 file, then set `DEBUG=False` and I was good to go.

---

## Background

Recently I have built an amazing software SaaS product with Django and it worked perfectly in development. Once I switched
`DEBUG=False` all hell broke lose and everything started breaking. Pushing to heroku was such a pain. I couldn't get Amazon S3
to work and spent 2 full days trying to integrate it.

## Features

- BASIC. The reason for this repo is essentially to have a project that can be deployed within minutes with best practices
- Uses Amazon S3 to fulfill static and media files. Setup is EASY.
- Uses Amazon RDS PostgreSQL for production environment database.
- Uses SQLite for development environment database.
- In your Amazon Bucket, your static files and media files are seperated into their respective folders which makes a CLEAN bucket.
- Already uses a .env file through [django-environ](https://github.com/joke2k/django-environ) inspired by [12factor](https://12factor.net/)


# Usage

## First Steps

Clone this repository using:

    $ git clone https://github.com/FurySkyBusiness/django-heroku-production.git

### Create an Amazon S3 Bucket and a User
You'll need to create an Amazon S3 Bucket and User. Follow the instructions in this link. Everything involving Django is already done for you.
 Just complete the first few steps and stop at the `S3 for Django static files` header.
[Only Do The First Steps That Require You To Create A Bucket And A User](https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/)

### Create an Amazon RDS PostgreSQL database.
If you want to put your Django project in production, you'll need an external database. Amazon RDS allows you to set up
 a reliable production database. Once again everything involving Django is done for you, just put your information in your
 `.env` file.

### Set up your `.env` variables
Make sure you set up your `django-environ` variables inside the `.env` inside the root of your project
(Same place as where your manage.py file is). Don't commit your actual `.env` to source-control! Add it to your .gitignore file.

```python
    # This is WRONG
    AWS_STORAGE_BUCKET_NAME="Bucket-Name"
```
```python
    # This is CORRECT
    AWS_STORAGE_BUCKET_NAME=Bucket-Name
```


## Deployed Locally

Make sure you complete everything inside `First Steps` first. Then run:

    $ pip install -r requirements.txt
    $ python manage.py createsuperuser

Alternatively, you can go to the `/easy_deploy` folder and run on Windows:

    $ .\local.bat

Then run the server.

## Deployment to Heroku

Deploying to Heroku is incredibly easy. Once you finished everything in First Steps above, just set `DEBUG=True`, navigate to the `/easy_deploy` folder and run on Windows

    $ .\deploy.bat

Enter your Heroku login credentials and let the program run. Your all set!

Your ready to launch!


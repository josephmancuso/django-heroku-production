# BASIC Production Ready Django Application

This repo allows anyone to clone this repo, then set up their django application to deploy to heroku FAST

---

## Background

Recently I have built an amazing software SaaS product with Django and it worked perfectly in development. Once I switched
`DEBUG=FALSE` all hell broke lose and everything started breaking. Pushing to heroku was such a pain. I couldn't get Amazon S3
to work and spent 2 full days trying to integrate it.

## Features

- BASIC. The reason for this repo is essentially to have a project that can be deployed within minutes
- Uses Amazon S3 to fulfill static and media files. Setup is EASY.
- Already uses a .env file through [django-environ](https://github.com/joke2k/django-environ) inspired by [12factor](https://12factor.net/)


# Usage

## First Steps

Clone this repository using:

    $ git clone https://github.com/FurySkyBusiness/django-heroku-production.git

### Create an Amazon S3 Bucket and a User
You'll need to create an Amazon S3 Bucket and User. Follow the instructions in this link. Everything involving Django is already done for you.
 Just complete the first few steps and stop at the `S3 for Django static files` header.
[Only Do The First Steps That Require You To Create A Bucket And A User](https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/)

### Set up your `.env` variables
Make sure you set up your `djangon-environ` variables inside the `.env` inside the main root of your project
(Same place as where your manage.py file is). Copy and paste the content from `.env-template`
and replace it with your information. You can then safely delete `.env-template`. Don't commit your actual `.env` to source-control!

## Deployed Locally

Make sure you complete everything inside `First Steps` first. Then run:

    $ pip install -r requirements.txt
    $ python manage.py collectstatic
    $ python manage.py makemigrations
    $ python manage.py migrate

Then run the server.

## Deployment to Heroku

Deploying to Heroku is incredibly easy. Once you finished everything in First Steps above, just navigate to the `helloworld/easy_deploy` folder and run

    $ .\deploy.bat

Enter your Heroku login credentials and let the program run. Your all set!
Your ready to launch!


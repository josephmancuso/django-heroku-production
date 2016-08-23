# Restaurant Software Product For Fury Sky Web Design

Allows any business to start receiving online orders within minutes. This is the beginning of software development for
this company.

---

## Features

- Production-ready configuration within minutes
- Can be built and deployed right in front of the clients eyes
- Self Contained. Utilizes Amazon S3 to fulfill static file and media storage
- Allows the business to start taking orders fast and easy

# Usage

This software can be used to sell to any local restaurant business. The beauty of this product is that the client doesnt
have to wait weeks or months until someone is created for them. In order to start selling your own product like this:

## First Steps

Make sure you set up your `djangon-environ` variables inside the `.env` inside the main root of your project
(Same place as where your manage.py file is). Just create a `.env` file, copy and paste the content from `.env-template`
and replace it with your information. You can then safely delete `.env-template`

## Deployment to Heroku

Deploying to Heroku is incredibly easy. Once you finished everything in First Steps above, just navigate to the `app/easy_deploy` folder and run

    $ .\deploy.bat

Enter your Heroku login credentials and let the program run. Your all set!

## Deployed Locally

    $ git clone https://github.com/FurySkyBusiness/RestaurantSaaS.git
    $ python manage.py collectstatic
    $ python manage.py makemigrations
    $ python manage.py migrate

Your ready to launch!


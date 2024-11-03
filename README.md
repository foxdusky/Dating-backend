# Dating API

This API is a minimal backend component for a dating app

# [Project Structure](./project-structure.md)

# Edpoints

## POST api/clients/create/

Endpoint for registering a new client has a username & e_mail uniqueness check under the hood. After successful
registration, it gives the token

## GET api/clients/current/

Endpoint for getting information about the current user.

## POST api/clients/{id}/match

Endpoint to mark "like" another user by their id

## POST api/list

Endpoint to get a list of all users with filtering and sorting by all fields, as well as pagination

# Deploy

Execute the command

~~~
git clone https://github.com/foxdusky/Dating-backend.git
~~~

OR

~~~
gh repo clone foxdusky/Dating-backend
~~~

create an env file in the root of the repository

ENV EXAMPLE

~~~
COMPOSE_PROJECT_NAME='YOUR_COMPOSE_PROJECT_NAME'

# DEV OR PROD ENVIRONMENT
IS_DEV_ENV=1

SECRET_KEY='YOUR_SECRET_KEY'

POSTGRES_USER='YOUR_POSTGRES_USER'
POSTGRES_PASSWORD=''YOUR_POSTGRES_PASSWORD

#REPLACE @POSTGRES_USER:@POSTGRES_PASSWORD TO THE REAL ONE

DB_CON_STR=postgresql://@POSTGRES_USER:@POSTGRES_PASSWORD@db:5432/postgres

# Migration con str
#REPLACE @POSTGRES_USER:@POSTGRES_PASSWORD TO THE REAL ONE
#DB_CON_STR=postgresql://@POSTGRES_USER:@POSTGRES_PASSWORD@localhost:5432/postgres

PICTURES_DIR=/app/pics

# REPLACE THAT TO REAL PATHS IF THAT IS PROD ENVIRONMENT
SSL_KEY_FILE=./.env
SSL_CERT_FILE=./.env

REDIS_HOST=redis-server
REDIS_PORT=6379

RESEND_API_KEY='YOUR_RESEND_KEY'

#int value
MATCHING_REQUEST_DAILY_LIMITATION='YOUR_VALUE_OF_USER_DAILY_LIMIT_FOR_MATCHING'

~~~

run using docker

~~~
docker-compose up -d --build
~~~
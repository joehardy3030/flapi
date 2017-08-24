# flapi
Flask API learning project

Based on the flasky book

python manage.py runserver --host 0.0.0.0

Options for actual deployment: 
http://flask.pocoo.org/docs/0.12/deploying/

initialize the db migration repository 

python manage.py db init

python manage.py db migrate -m "initial migration"

python manage.py db upgrade

environment variables

export FLAPI_ADMIN=

export MAIL_USERNAME=

export MAIL_PASSWORD=

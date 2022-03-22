# [Bidnamic Python Challenge: Edward Segun's Attempt](https://bidnamic.edwardsegun.com/bidnamic)

This is my implementation of the coding test given by Bidnamic

# Project Structure
├── bidnamic-python-challenge           # the django project BASE_DIR   
│   ├── bidnamic                        # the project folder   
│   │   ├── settings                    # contains development and production settings   
│   │   │   ├── ...  
│   │   │   ├── prod_settings.py        # production settings file  
│   │   │   └── edgam_settings.py       # edward's development settings file  
│   │   ├── ...  
│   │   ├── base_settings.py            # base settings file  
│   │   ├── celery.py                   # configuration for celery  
│   │   ├── urls.py                     # http urls file  
│   │   └── wsgi.py                     # used to serve the application  
│   ├── portal                          # the app folder  
│   │   ├── migrations                  # migration files for the `portal` app  
│   │   │   └── ...  
│   │   │── static                      # static files for the `portal` app  
│   │   │   └── ...  
│   │   │── templates                   # template files for the `portal` app  
│   │   │   └── ...  
│   │   │── ...  
│   │   │── authentication.py           # custom authentication backend  
│   │   │── context_processors.py       # custom context processor  
│   │   │── middleware.py               # custom middleware used to enforce only one active session per user  
│   │   │── ...  
│   │   │── tasks.py                    # celery tasks definitions  
│   │   │── ...  
│   │   │── utils.py                    # contains custom helper classes and methods  
│   │   └── ...   
│   ├── .gitignore                      # Git Ignore File  
│   ├── ...  
│   ├── manage.py                       # django start up file  
│   ├── README.md                       # the file you are reading  
│   └── requirements.txt                # or pip to install python dependencies into a venv

# Installation (Ubuntu)
This app is uses `Python == 3.7.7`

Create the database and user, depending on the database settings in the selected settings file  

Navigate to the base directory of the project

Create the directory for logs called `logs`
```sh
$ mkdir logs
```    

Create a python3 virtual environment (assuming you've navigated to the base directory) called `venv`
```sh
$ virtualenv -p python3 venv
```  
or
```sh
$ python3 -m venv venv
```  
Next, activate the `venv` 
```sh
$ source venv/bin/activate
```  
Now install dependencies  
```sh
(venv) $ pip install -r requirements.txt
```  
Now run migration  
```sh
(venv) $ python manage.py migrate
```  
If being installed in production  
```sh
(venv) $ python manage.py collectstatic --no-input
```  
Create super user  
```sh
(venv) $ python manage.py createsuperuser
```  
Next exit from virtual environment  
```sh
(venv) $ deactivate
```  
To use `nginx` to serve the webapp, install it  
```sh
$ apt-get install nginx
```  
Then configure `nginx` to serve the app  
```sh
$ nano /etc/nginx/sites-available/bidnamic
```  
```sh
server {
    listen 80;
    
    server_name [domain name];
    
    access_log /var/www/bidnamic-python-challenge/logs/nginx_access.log;
    error_log /var/www/bidnamic-python-challenge/logs/nginx_error.log;

    location /bidnamic/ {
        proxy_pass http://unix:/var/www/bidnamic-python-challenge/bidnamic.sock;
        proxy_http_version 1.1;

        proxy_read_timeout 86400;
        proxy_redirect     off;

        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header Origin '';
    }

    location /bidnamic/static {
        alias /var/www/bidnamic-python-challenge/static;
    }

    location /bidnamic/media {
        alias /var/www/bidnamic-python-challenge/media;
    }
}
```  
Then link the file to the enabled folder
```sh
$ ln -s /etc/nginx/sites-available/bidnamic /etc/nginx/sites-enabled/
```     
Next restart `nginx` 
```sh
$ systemctl restart nginx
```
To use `nginx` to serve the webapp, install it  
```sh
$ apt-get install redis-server
```  
Then configure `redis`  
```sh
$ nano /etc/redis/redis.conf
```  
```sh
. . .

# If you run Redis from upstart or systemd, Redis can interact with your
# supervision tree. Options:
#   supervised no      - no supervision interaction
#   supervised upstart - signal upstart by putting Redis into SIGSTOP mode
#   supervised systemd - signal systemd by writing READY=1 to $NOTIFY_SOCKET
#   supervised auto    - detect upstart or systemd method based on
#                        UPSTART_JOB or NOTIFY_SOCKET environment variables
# Note: these supervision methods only signal "process is ready."
#       They do not enable continuous liveness pings back to your supervisor.
supervised systemd

. . .
```    
Next restart `redis` 
```sh
$ systemctl restart redis
```
Next, install and configure `supervisor` to serve `gunicorn`
```sh
$ apt-get install supervisor
```
```sh
$ nano /etc/supervisor/conf.d/bidnamic_group.conf
```   
```sh
[group:bidnamic_group]
programs=bidnamic,worker

[program:customizer]
command=/var/www/bidnamic-python-challenge/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/bidnamic-python-challenge/bidnamic.sock bidnamic.wsgi:application

directory=/var/www/bidnamic-python-challenge
user=root
numprocs=1
stdout_logfile=/var/www/bidnamic-python-challenge/logs/gunicorn.log
stderr_logfile=/var/www/bidnamic-python-challenge/logs/gunicorn.log
autostart=true
autorestart=true

[program:worker]
command=/var/www/bidnamic-python-challenge/venv/bin/celery -A bidnamic worker --loglevel=INFO --queues bidnamic_default_queue
directory=/var/www/bidnamic-python-challenge
user=root
numprocs=1
stdout_logfile=/var/www/bidnamic-python-challenge/logs/worker.log
stderr_logfile=/var/www/bidnamic-python-challenge/logs/worker.log
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=600
stopasgroup=true
priority=998

```   
Next start the process 
```sh
$ supervisorctl reread
$ supervisorctl update
```  
Check the status of the process
```sh
$ supervisorctl status bidnamic_group:*
```  
# Using the Web App
## Base URL `https://bidnamic.edwardsegun.com/bidnamic`
## Login `/auth/signin/`
Admin username: **sanjay@bidnamic.com** OR `superuser` created earlier

Admin password: **temppa$$1** OR `superuser` created earlier

## Index Page `/`

## Django Admin `/admin/`

# Using the API
## Base URL `https://bidnamic.edwardsegun.com/bidnamic/api`
## Authentication `/token/`
Admin username: **sanjay@bidnamic.com** OR `superuser` created earlier

Admin password: **temppa$$1** OR `superuser` created earlier

The api uses django rest framework simplejwt for authentication.

**Request Sample**
```
curl --location --request POST 'https://bidnamic.edwardsegun.com/bidnamic/api/token/' \
--header 'Content-Type: application/json' \
--data-raw '{"username": "sanjay", "password": "temppa$$1"}'
```
**Response Sample**
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0ODAyMjk0NCwiaWF0IjoxNjQ3OTM2NTQ0LCJqdGkiOiI2YjU1ZjBiMzFhYjU0M2E5YjAyZTFkZmY0NzIxNTg3MiIsInVzZXJfaWQiOjF9.e_bJBX35bc2hCqzGxnCvZfglKlkzoQ9EI0yoMA7fZgE",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ3OTM2ODQ0LCJpYXQiOjE2NDc5MzY1NDQsImp0aSI6IjUzNWMxMDQyYmE4ODRkNWFiYzdlY2QxNjlhZGMwZDE2IiwidXNlcl9pZCI6MX0.gM_Jum40GyWdHiu3TBvU3QF-0rbMLYPa6MAb3ZDXwY0"
}
```

## Fetch ROAS `/roas/fetch/`
This endpoint is called to fetch ROAS

**Request Parameters are;**
### query *
This is a string that contains the value to use in retrieving results
### which *
This is a string that specifies whether the results should be based on `campaigns` or `ad-groups`
### limit *
This is an integer that specifies how many records should be returned
**Request Sample**
```
curl --location --request POST 'https://bidnamic.edwardsegun.com/bidnamic/api/roas/fetch/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bidnamic [access]' \
--form 'query="venum"' \
--form 'which="campaigns"' \
--form 'limit="10"'
```

**Response Parameters are;**
### search_term
### total_cost
### total_conversion_value
### structure_value / alias
**Response Sample**
```
{
    "results": [
        {
            "search_term": "venum boxing boots",
            "total_cost": 0.13,
            "total_conversion_value": 119.99,
            "roas": 922.9999999999999,
            "structure_value": "venum"
        },
        . . . 
    ]
}
```

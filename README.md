# miare

first of all we need to create on redis container with docker
to use it as message broker

```shell
docker run -d -p 6378:6379 redis
```

### for run project:

first:
```shell
pip install -r requirements.txt
```
second:
```shell
python manage.py makemigrations
```
third:
```shell
python mange.py migrate
```
fourth:
```shell
python manage.py runserver
```


### you must run celery & celery beat alongside project

celery worker:
```shell
celery -A core worker -l info
```
celery beat:
```shell
celery -A core beat -l info
```
flower:
```shell
# if you want to monitoring celery tasks:
celery -A core flower --address=127.0.0.1 --port=5555
```















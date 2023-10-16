# reservation system
The backend project for simple reservation system using Python and Django

### Stack
Following applications must be installed and configured:

- python3.9 
- Postgresql

### Run
- Open a terminal in root folder of reservation_system.
- Create a virtual environment with `virtualenv` and activate it:
```
virtualenv _env && source _env/bin/activate
```
- Install requirements:
```
pip install -r infrastructure/requirements.txt
```
- Copy `env.sample` as `.env` in root folder:
```
cp infrastructure/env.sample .env
```
- Configure settings in `.env` file with your stack data.
- Export environment variables:
```
. $PWD/loadenv.sh
```
- Migrate database:
```
python manage.py migrate
```
- Run project:
```
python manage.py runserver
```
- In order to load data from fixtures:
```
python manage.py loaddata infrastructure/fixture.json
```

### Docs
- To access documentation, check docs directory.

### RestAPI PlayGround
- To access the RestAPI playground, use the URL: host:port/playground/





# Montreal McFlurry Map
## Launch flask app
```
pip install -r requirements.txt
limit 10 FLASK_RUN_PORT=8000 FLASK_APP=server.py FLASK_ENV=development PGDATABASE=mcflurry PGHOST=127.0.0.1 PGPASSWORD=postgres PGUSER=postgres flask run --host=0.0.0.0
```
## environment variables :
- FLASK_APP=server.py 
- FLASK_ENV=development
- FLASK_RUN_PORT=8000
- PGDATABASE=mcflurry 
- PGHOST=127.0.0.1 
- PGPASSWORD=postgres 
- PGUSER=postgres
- LIMIT=5 limit number of restaurant menu to fetch to 5

## refresh menu of restaurants 
`/refresh`

## check status of app and db connection
`/health`

## AWS Lambda
Voir [lambda/readme.md](https://github.com/ttwthomas/mcflurry/blob/main/lambda/readme.md)

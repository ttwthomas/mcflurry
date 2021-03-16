# Montreal McFlurry Map
## Launch flask app
```
pip install -r requirements.txt
PGDATABASE=mcflurry PGHOST=127.0.0.1 PGPASSWORD=postgres PGUSER=postgres flask 
```

## environment variables :
- PGDATABASE=mcflurry 
- PGHOST=127.0.0.1 
- PGPASSWORD=postgres 
- PGUSER=postgres
- LIMIT=5 limit number of restaurant menu to fetch to 5

## refresh menu of restaurants 
`/refresh`

## check status of app and db connection
`/health`
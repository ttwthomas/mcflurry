import psycopg2
import json
import main as resto


def save_restaurants(cur, restaurants):
    create_table_query="DROP TABLE IF EXISTS demo; CREATE TABLE IF NOT EXISTS demo( id SERIAL PRIMARY KEY, DATA JSON);"
    cur.execute(create_table_query)
    for restaurant in restaurants:
        save_restaurants_query="insert into demo(DATA) values (%s);"
        cur.execute(save_restaurants_query, [json.dumps(restaurant)])
    return cur.statusmessage

def get_restaurants(cur):
    get_restaurants_query="SELECT data FROM demo;"
    cur.execute(get_restaurants_query)
    rows = cur.fetchall()
    restaurants = [row[0] for row in rows] # removing tuples
    restaurants = json.dumps(restaurants)
    restaurants = "export const restaurants = {}".format(restaurants)
    return (restaurants)

def init():
    try:
        conn = psycopg2.connect(dbname="mcflurry")
        conn.autocommit = True
        cur = conn.cursor()
    except:
        print("unable to connect to the database")
        exit(1)

    return cur

def healthcheck(cur):
    select_query="SELECT 1"
    cur.execute(select_query)
    result = cur.fetchone()[0]
    return result


if __name__ == "__main__":
    restaurants = resto.load_restaurants()
    restaurants_menu = resto.get_unavailable_menu(restaurants[:5])
    cur = init()
    save_restaurants(cur,restaurants_menu)

    print(get_restaurants(cur))

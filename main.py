import requests
import json, os, time, sys
import http.server
import socketserver

def get_restaurants():                                                                                                                                                             
    url= "https://api.skipthedishes.com/customer/v1/graphql"                                                                                                                       
    headers = {                                                                                                                                                                    
        'authority': 'api.skipthedishes.com',                                                                                                                                      
        'accept': '*/*',                                                                                                                                                           
        'accept-language': 'en',                                                                                                                                                   
        'app-token': 'd7033722-4d2e-4263-9d67-d83854deb0fc',                                                                                                                       
        'content-type': 'application/json',                                                                                                                                        
        'dnt': '1',                                                                                                                                                                
        'origin': 'https://www.skipthedishes.com',                                                                                                                                 
        'parameters': 'filterBy=&isCuisineSearch=false&isSorted=false&search=mc',                                                                                                  
        'referer': 'https://www.skipthedishes.com/',                                                                                                                               
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',                                                                                          
        'sec-ch-ua-mobile': '?0',                                                                                                                                                  
        'sec-ch-ua-platform': '"macOS"',                                                                                                                                           
        'sec-fetch-dest': 'empty',                                                                                                                                                 
        'sec-fetch-mode': 'cors',                                                                                                                                                  
        'sec-fetch-site': 'same-site',                                                                                                                                             
        'sec-gpc': '1',                                                                                                                                                            
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',                                     
    }                                                                                                                                                                              
                                                                                                                                                                                   
    json_data = {                                                                                                                                                                  
        'operationName': 'QueryRestaurantsCuisinesList',                                                                                                                           
        'variables': {                                                                                                                                                             
            'city': 'montreal',                                                                                                                                                    
            'province': 'QC',                                                                                                                                                      
            'isDelivery': True,                                                                                                                                                    
            'dateTime': 0,                                                                                                                                                         
            'search': 'mc',                                                                                                                                                        
            'language': 'en',                                                                                                                                                      
        },                                                                                                                                                                         
        'extensions': {                                                                                                                                                            
            'persistedQuery': {                                                                                                                                                    
                'version': 1,                                                                                                                                                      
                'sha256Hash': 'de41a8aae22964fa0f2815f1bad863a14ad29f0e95004559d4ada0b31b388c06',                                                                                  
            },                                                                                                                                                                     
        },                                                                                                                                                                         
                                                                                                                                                                                   
    }                                                                                                                                                                              
                                                                                                                                                                                   
    req = requests.post(url,headers=headers,json=json_data)
    restaurants = []
    for restaurant in req.json()["data"]["restaurantsList"]["openRestaurants"] :
        if "mcdonalds" in restaurant['cleanUrl'] and restaurant["location"]["position"]: 
            restauItem = {
                "name": restaurant["location"]["name"],
                "url": restaurant["cleanUrl"],
                "location": restaurant["location"]["position"],
                "open": restaurant["isOpen"],
            }
            restaurants.append(restauItem)
    
    return restaurants

def get_menu(cleanUrl):
    url = "https://api-skipthedishes.skipthedishes.com/v1/restaurants/clean-url/{}?fullMenu=true&language=en".format(cleanUrl)
    headers = {
        'app-token': 'd7033722-4d2e-4263-9d67-d83854deb0fc',
    }
    
    req = requests.get(url,headers=headers)
    # skipping 0 and 1, "alergy restriction" and "popular" categories
    categories = req.json()["menu"]["menuGroups"][2:]
    items = []
    for category in categories:

        items += category["menuItems"]
    return items

def load_restaurants():
    restaurants_file = 'restaurants.json'
    if os.path.isfile(restaurants_file):    # if file exist
        with open(restaurants_file) as f:
            restaurants = json.load(f)
    else:                                   # if file doesn't exist
        restaurants = get_restaurants()
        with open(restaurants_file, 'w') as json_file:
            json.dump(restaurants, json_file)
    return restaurants

def save_restaurants_menu_json(restaurants_menu):
    restaurants_menu_json = 'missingflurry.js'
    with open(restaurants_menu_json, 'w') as json_file:
        json_file.write("export const restaurants = {}".format(json.dumps(restaurants_menu, indent=4)))
        print("saved missingflurry.js")

def get_unavailable_menu(restaurants):
    restaurants_menu = []
    for restaurant in restaurants :
        menu = get_menu(restaurant["url"])
        indispo = []
        for item in menu :
            if item["available"] is not True:
                item = item["name"]
                if "Flurr" in item and "Egg" not in item:
                    indispo.append(item)
        restaurant["unavailable"] = indispo 
        # if len(restaurant["unavailable"]) > 0:
        restaurants_menu.append(restaurant)
    return restaurants_menu

if __name__ == "__main__":
    restaurants = load_restaurants()
    restaurants_menu = get_unavailable_menu(restaurants)
    save_restaurants_menu_json(restaurants_menu)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory="./", **kwargs)
            
    PORT=int(os.environ.get('PORT',8000))
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving on port", PORT)
        httpd.serve_forever()

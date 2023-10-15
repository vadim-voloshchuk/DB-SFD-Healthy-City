import requests
import random
import pandas as pd
from shapely.geometry import Polygon
from shapely.ops import transform
import pyproj
import overpy
from geopy.distance import great_circle
import numpy as np

api = overpy.Overpass()

geonames_username = 'kingofsweetsx2k'

base_url = 'http://api.geonames.org/searchJSON'
params = {
    'q': 'Russia',
    'country': 'RU',
    'featureClass': 'P',
    'lang':'ru',
    'maxRows': 50,
    'username': geonames_username,
}

response = requests.get(base_url, params=params)
print(response.text)

if response.status_code == 200:
    data = response.json()
    cities = [entry['name'] for entry in data['geonames']]


points = {
    "negative": {
        "values": ["wine_shop","alcohol","drinks","food_court","electronic_cigarettes","tobacco", "adult_gaming_centre","amusement_arcade","bar","biergarten","fast_food","cafe","ice_cream","pub"],
        "key": "amenity"
    },
    "positive": {
        "values": ["bandstand", "bathing_place", "beach_resort", "bowling_alley", "dance", "disc_golf_course", "escape_game", "firepit", "fishing", "fitness_centre", "fitness_station", "garden", "golf_course", "horse_riding", "ice_rink", "ice_rink", " miniature_golf", "nature_reserve", "park", "pitch", "playground", "exhibition_centre", "music_venue", "shelter", "animal_training", "dive_centre", "public_bath"],
        "key": "leisure"
    },
    "main_city": {
        "values": ["university","college","school","kindergarten","language_school","music_school"],
        "key": "amenity"
    }
}

def get_points(reg = "Таганрог", type = "positive"):
    result = api.query(f"""
    area[name="{reg}"];
    (
        node["{points[type]['key']}"~"{'|'.join(points[type]['values'])}"](area);
    );
    out body;
    """)


    return result

def get_reg_based(city):
    result = api.query(f"""
    area[name="{city}"];
    /*added by auto repair*/
    (._;>;);
    /*end of auto repair*/

    out body;
    """)
    if result.areas != []:
        for area in result.areas:
            resp = area.tags
        return str(resp.get('place')), str(resp.get('population')),  str(resp.get('addr:country')), str(resp.get('addr:region'))

    else: return None, None, None, None

def get_green_area(city_name):
    query = f"""
    area[name="{city_name}"];
    (
        way["leisure"="park"](area);
        way["leisure"="square"](area);
        way["landuse"="recreation_ground"](area);
        way["landuse"="forest"](area);
    );
    /*added by auto repair*/
    (._;>;);
    /*end of auto repair*/
    out geom;
    """

    result = api.query(query)

    total_area = 0

    for way in result.ways:
        coords = [(node.lon, node.lat) for node in way.nodes]
        polygon = Polygon(coords)
        projected_polygon = transform(pyproj.Transformer.from_crs(4326, 3857, always_xy=True).transform, polygon)
        area = projected_polygon.area
        total_area += area
    print(f"Площадь зеленых зон в {city_name}: {total_area} квадратных метров")
    return total_area

def get_transport_density(city_name):
    city_name = "Название Вашего Города"
    query = f"""
        area[name="Екатеринбург"];
        (
            relation["route"~"bus|subway|tram"](area);
            node["public_transport"~"platform"](area);
        );
        out geom;
        """

    result = api.query(query)

    number_of_routes = len(result.relations)
    number_of_stops = len(result.nodes)
    region_area = result.area[0].tags.get("area:highway")

    if region_area is not None:
        region_area = float(region_area)
        density = (number_of_routes + number_of_stops) / region_area
        print(f"Плотность общественного транспорта: {density} на квадратный метр")
        return density
    else:
        return None
        print("Площадь региона не найдена. Невозможно вычислить плотность транспорта.")

def get_reg_points(reg = "Таганрог"):
    points_data_loacl = pd.DataFrame(columns = ['name', 'obj_type', 'type', 'geo', 'lat', 'lon'])
    types = ["negative", "positive", "main_city"]
    max_objs = {
        "negative": "",
        "positive": "",
        "main_city": ""
    }
    for type in types:
        resp  = get_points(reg, type = type)
        names = []
        obj_type = []
        latitudes = []
        longitudes = []

        for node in resp.nodes:
            names.append(node.tags.get("name"))
            obj_type.append(node.tags.get(points[type]['key']))
            latitudes.append(node.lat)
            longitudes.append(node.lon)

        points_data_loacl = pd.concat([points_data_loacl, pd.DataFrame({'name': names, 'obj_type': obj_type, 
        'type': type, 'lat': latitudes, 'lon': longitudes})], ignore_index=True)
        try:
            max_obj_type = points_data_loacl[points_data_loacl['type'] == type]['obj_type'].value_counts()
            print(max_obj_type.idxmax())
            max_objs[type] = max_obj_type.idxmax()
        except:
            max_objs[type] == "None"

    
    return points_data_loacl, max_objs

def calculate_distance(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return great_circle(coords_1, coords_2).meters

def count_negative_points_near_positive(df, max_distance=100):
    count = 0
    for index, row in df.iterrows():
        if row['type'] == 'positive':
            for i, r in df.iterrows():
                if r['type'] == 'negative':
                    distance = calculate_distance(row['lat'], row['lon'], r['lat'], r['lon'])
                    if distance <= max_distance:
                        count += 1
                        break
    return count

def calculate_average_distance(df, max_distance=200):
    distances = []

    for index, row in df.iterrows():
        if row['type'] == 'negative':
            distances_to_positive = []

            for i, r in df.iterrows():
                if r['type'] == 'positive':
                    distance = calculate_distance(row['lat'], row['lon'], r['lat'], r['lon'])
                    if distance <= max_distance:
                        distances_to_positive.append(distance)

            if distances_to_positive:
                distances.append(np.mean(distances_to_positive))

    if distances:
        return np.mean(distances)
    else:
        return None

def collect_all_data(cities):
    dataset = pd.DataFrame(columns = [
        'city', 'positive_count',
        'green_zone', 'place', 'population', 'country', 'region',
        # 'transport_desteny',
        'negative_count', 'main_city_count', 
        'average_distance', 'bad_dist_count',
        'max_negative', 'max_main', 'max_positive'
    ])
    
    for city in cities:
        points_data, max_objs = get_reg_points(city)
        print(max_objs)
        green_zone = get_green_area(city)
        # transport_desteny = get_transport_density(city)
        place, population, country, region = get_reg_based(city)
        print(place, population, country, region)

        positive_count = len(points_data[points_data['type'] == 'positive'])
        negative_count = len(points_data[points_data['type'] == 'negative'])
        main_city_count = len(points_data[points_data['type'] == 'main_city'])
        print(f"P|N|M: {positive_count}|{negative_count}|{main_city_count}")
        
        # if negative_count > 0:
        #     average_distance = calculate_average_distance(points_data)
        #     bad_dist_count = count_negative_points_near_positive(points_data)
        # else:
        #     average_distance = np.nan

        raw_data = pd.DataFrame({'city': city, 'positive_count': positive_count, 
                                  'negative_count': negative_count, 'main_city_count': main_city_count, 
                                  'green_zone': green_zone, #'transport_desteny':transport_desteny,
                                  'place': place, 'population': population, 'country': country, 'region': region,
                                #   'average_distance': average_distance, 'bad_dist_count': str(bad_dist_count),
                                  'max_negative': max_objs['negative'], 'max_main': max_objs['main_city'], 'max_positive':max_objs['positive']
                                  }, index = [0])
        # points_data_loacl = pd.concat([points_data_loacl, pd.DataFrame({'name': names, 'obj_type': obj_type, 
        # 'type': type, 'lat': latitudes, 'lon': longitudes})], ignore_index=True)
        dataset = pd.concat([dataset, raw_data], ignore_index=True)
    
    return dataset

if __name__ == "__main__":
    data = collect_all_data(cities)
    data.to_csv('dataset.csv')

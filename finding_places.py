import json
import requests
import sys
import time


LOCATION = '21.013171,105.822266'  # Just an example
key = "AIzaSyCMTsML4kBe_lkQFgb8Ide7zI2vOarN0BM"
""" Go to https://developers.google.com/places/web-service/
and follow instruction to get key"""

session = requests.session()


def places(radius, keyword):
    place = []
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    parameters = {"location": LOCATION,
                  "radius": radius,
                  "keyword": keyword,
                  "key": key}
    response = session.get(url, params=parameters).json()
    place.extend(response["results"])
    while "next_page_token" in response:
        time.sleep(10)
        parameters.update({"pagetoken": response["next_page_token"]})
        response_next = session.get(url, params=parameters).json()
        place.extend(response_next)
        if len(place) > 50:
            break
    return place


def geojson_map(datas):
    geojson_map = {
        "type": "FeatureCollection",
        "features": [
                {"type": "Feature",
                        "geometry": {"type": "Point",
                                             "coordinates":
                                             [float(data['geometry']['location']['lng']),   # NOQA
                                              float(data['geometry']['location']['lat'])]}, # NOQA
                "properties": {"Address": data['vicinity'],
                                "name": data['name']}
                } for data in datas if type(data) is dict]}
    with open('bar.geojson', 'wt') as f:
        json.dump(geojson_map, f, ensure_ascii=False, indent=4)


def main():
    radius = int(sys.argv[1])
    keyword = sys.argv[2]
    datas = places(radius, keyword)
    geojson_map(datas)


if __name__ == "__main__":
    main()

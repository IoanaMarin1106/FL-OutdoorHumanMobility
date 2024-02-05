import requests
import pandas as pd
import csv

class Place:
    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location

    def __str__(self) -> str:
        return f"id={self.id}\nname={self.name}\nlocation.lat={self.location[0]}\nlocation.long={self.location[1]}\n"



SEARCH_NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"

SEARCH_NEARBY_HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": "",   # insert key here
    "X-Goog-FieldMask": "places.displayName,places.location,places.id,places.types"
}

circles_df = pd.read_csv("data.csv")

df = circles_df

places = list()
places_chunk = list()

with open('places.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(['id', 'name', 'latitude', 'longitude'])

    for idx in df.index:
        SEARCH_NEARBY_BODY = {
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": df['lat'][idx],
                        "longitude": df['long'][idx]
                    },
                    "radius": 100.0
                }
            }
        }

        try:
            response = requests.post(
            url = SEARCH_NEARBY_URL,
            json = SEARCH_NEARBY_BODY,
            headers = SEARCH_NEARBY_HEADERS
            )

            response_json = response.json()

            if response_json != {}:
                for place in response_json['places']:
                    elem = (place['id'], place['displayName']['text'], float(place['location']['latitude']), float(place['location']['longitude']), list(place['types']))
                    places.append(elem)
                    places_chunk.append(elem)

            if (len(places_chunk) > 500):
                write.writerows(places_chunk)
                places_chunk = list()

        except:
            print(f"exception occured for point {df['lat'][idx]},{df['long'][idx]}")


print(f"Number of places extracted from circles: {len(places)}")

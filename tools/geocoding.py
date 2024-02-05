import requests
import pandas as pd

KEY = "" # insert key here
GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={key}"

df = pd.read_csv("places.csv")
df["northeast_lat"]=""
df["northeast_lng"]=""
df["southwest_lat"]=""
df["southwest_lng"]=""


for idx in df.index:
    response = requests.get(GEOCODING_URL.format(lat=df["latitude"][idx], lng=df["longitude"][idx], key=KEY))

    filtered_places = list(filter(lambda x: "bounds" in x["geometry"] and x["geometry"]["location_type"] == "ROOFTOP",
                               list(response.json()['results'])))

    if len(filtered_places) > 0:
        place_bounds = filtered_places[0]["geometry"]["bounds"]
        
        df["northeast_lat"][idx] = float(place_bounds["northeast"]["lat"])
        df["northeast_lng"][idx] = float(place_bounds["northeast"]["lng"])

        df["southwest_lat"][idx] = float(place_bounds["southwest"]["lat"])
        df["southwest_lng"][idx] = float(place_bounds["southwest"]["lng"])


df.rename(columns={"latitude": "mark_lat", "longitude": "mark_lng"})

df.to_csv("geocoded-places.csv", index=False)
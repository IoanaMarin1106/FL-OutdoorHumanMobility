import csv
import requests
import time

KEY = '65bf5d47d53f4881855288sol08483f'
GEOCODING_URL = 'https://geocode.maps.co/reverse?lat={lat}&lon={lon}&api_key={key}'


places = list()
places_chunk = list()

with open('filtered-places.csv') as file_obj, open('geocoded-places.csv', 'a') as output: 
    reader_obj = csv.reader(file_obj) 
    writer_obj = csv.writer(output)

    # skip header
    headings = next(reader_obj)
    writer_obj.writerow(headings + ['boundingbox'])

    for idx, row in enumerate(reader_obj):
        # rate limiting - 1req/s
        time.sleep(1)

        try:
            response = requests.get(GEOCODING_URL.format(lat=row[2], lon=row[3], key=KEY))
            elem = (row[0], row[1], row[2], row[3], str(response.json()['boundingbox']))
            places.append(elem)

            writer_obj.writerow(elem)
            print(f'[#{idx + 1}/3426] {elem}')

        except:
            print(f"exception occured for point {row[2]},{row[3]}")

print(f"Number of geocoded places: {len(places)}")


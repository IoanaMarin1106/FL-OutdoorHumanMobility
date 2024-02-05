import math
import utm
import csv

lat_center, long_center = 44.43934, 26.10434  # Latitude and Longitude of the large circle
r_large = 10923  # Radius of the large circle in meters
r_small = 100  # Radius of the small circle in meters
center = utm.from_latlon(lat_center, long_center)

side = r_small * 2
apothem = math.sqrt(3)/2 * side

no_rings = math.ceil((math.ceil(r_large/apothem) - 1) / 2)

corner1_hexagons = list()
corner2_hexagons = list()
corner3_hexagons = list()
corner4_hexagons = list()
corner5_hexagons = list()
corner6_hexagons = list()

def calculate_hexagon_center_corner1(center, distance_meters):
    delta_y = distance_meters * math.sin(math.radians(60))
    delta_x = distance_meters * math.sin(math.radians(30))

    new_y = center[1] + delta_y
    new_x = center[0] - delta_x

    return (new_x, new_y)


def calculate_hexagon_center_corner2(center, distance_meters):
    delta_y = distance_meters * math.sin(math.radians(60))
    delta_x = distance_meters * math.sin(math.radians(30))

    new_y = center[1] + delta_y
    new_x = center[0] + delta_x

    return (new_x, new_y)


def calculate_hexagon_center_corner3(center, distance_meters):
    delta_x = distance_meters

    new_y = center[1]
    new_x = center[0] + delta_x

    return (new_x, new_y)


def calculate_hexagon_center_corner4(center, distance_meters):
    delta_y = distance_meters * math.sin(math.radians(60))
    delta_x = distance_meters * math.sin(math.radians(30))

    new_y = center[1] - delta_y
    new_x = center[0] + delta_x

    return (new_x, new_y)


def calculate_hexagon_center_corner5(center, distance_meters):
    delta_y = distance_meters * math.sin(math.radians(60))
    delta_x = distance_meters * math.sin(math.radians(30))

    new_y = center[1] - delta_y
    new_x = center[0] - delta_x

    return (new_x, new_y)


def calculate_hexagon_center_corner6(center, distance_meters):
    delta_x = distance_meters

    new_y = center[1]
    new_x = center[0] - delta_x

    return (new_x, new_y)


for i in range(1, no_rings + 1):
    easting1, northing1 = calculate_hexagon_center_corner1(center, 2 * i * apothem)
    corner1_hexagons.append((easting1, northing1))

    easting2, northing2 = calculate_hexagon_center_corner2(center, 2 * i * apothem)
    corner2_hexagons.append((easting2, northing2))

    easting3, northing3 = calculate_hexagon_center_corner3(center, 2 * i * apothem)
    corner3_hexagons.append((easting3, northing3))

    easting4, northing4 = calculate_hexagon_center_corner4(center, 2 * i * apothem)
    corner4_hexagons.append((easting4, northing4))

    easting5, northing5 = calculate_hexagon_center_corner5(center, 2 * i * apothem)
    corner5_hexagons.append((easting5, northing5))

    easting6, northing6 = calculate_hexagon_center_corner6(center, 2 * i * apothem)
    corner6_hexagons.append((easting6, northing6))


def calculate_edge1_hexagons(first_corner, apothem, ring):
    hexagons = ((first_corner, ) * (ring - 1))

    new_hexagons = list()
    for index, hex in zip(range(len(hexagons)), hexagons):
        new_hexagons.append((first_corner[0] + 2 * (index + 1) * apothem, first_corner[1]))
     
    return new_hexagons


def calculate_edge2_hexagons(first_corner, apothem, ring):
    hexagons = ((first_corner, ) * (ring - 1))
    delta_x = 2 * apothem * math.sin(math.radians(30))
    delta_y = 2 * apothem * math.sin(math.radians(60))

    new_hexagons = list()
    for index, hex in zip(range(len(hexagons)), hexagons):
        new_hexagons.append((first_corner[0] + (index + 1) * delta_x, first_corner[1] - (index + 1) * delta_y))

    return new_hexagons



def calculate_edge3_hexagons(first_corner, apothem, ring):
    hexagons = ((first_corner, ) * (ring - 1))
    delta_x = 2 * apothem * math.sin(math.radians(30))
    delta_y = 2 * apothem * math.sin(math.radians(60))

    new_hexagons = list()
    for index, hex in zip(range(len(hexagons)), hexagons):
        new_hexagons.append((first_corner[0] - (index + 1) * delta_x, first_corner[1] - (index + 1) * delta_y))

    return new_hexagons



def calculate_edge4_hexagons(first_corner, apothem, ring):
    hexagons = ((first_corner, ) * (ring - 1))

    new_hexagons = list()
    for index, hex in zip(range(len(hexagons)), hexagons):
        new_hexagons.append((first_corner[0] - 2 * (index + 1) * apothem, first_corner[1]))

    return new_hexagons


def calculate_edge5_hexagons(first_corner, apothem, ring):
    hexagons = ((first_corner, ) * (ring - 1))
    delta_x = 2 * apothem * math.sin(math.radians(30))
    delta_y = 2 * apothem * math.sin(math.radians(60))

    new_hexagons = list()
    for index, hex in zip(range(len(hexagons)), hexagons):
        new_hexagons.append((first_corner[0] - (index + 1) * delta_x, first_corner[1] + (index + 1) * delta_y))

    return new_hexagons


def calculate_edge6_hexagons(first_corner, apothem, ring):
    hexagons = ((first_corner, ) * (ring - 1))
    delta_x = 2 * apothem * math.sin(math.radians(30))
    delta_y = 2 * apothem * math.sin(math.radians(60))

    new_hexagons = list()
    for index, hex in zip(range(len(hexagons)), hexagons):
        new_hexagons.append((first_corner[0] + (index + 1) * delta_x, first_corner[1] + (index + 1) * delta_y))

    return new_hexagons


edge1_hexagons = list()
edge2_hexagons = list()
edge3_hexagons = list()
edge4_hexagons = list()
edge5_hexagons = list()
edge6_hexagons = list()

for i in range(2, no_rings + 1):
    edge1_hexagons.extend(calculate_edge1_hexagons(corner1_hexagons[i - 1], apothem, i))
    edge2_hexagons.extend(calculate_edge2_hexagons(corner2_hexagons[i - 1], apothem, i))
    edge3_hexagons.extend(calculate_edge3_hexagons(corner3_hexagons[i - 1], apothem, i))
    edge4_hexagons.extend(calculate_edge4_hexagons(corner4_hexagons[i - 1], apothem, i))
    edge5_hexagons.extend(calculate_edge5_hexagons(corner5_hexagons[i - 1], apothem, i))
    edge6_hexagons.extend(calculate_edge6_hexagons(corner6_hexagons[i - 1], apothem, i))



def pointy_hex_corner(center, side, i) -> tuple[float, float]:
    angle_deg = 60 * i - 30
    x = center[0] + side * math.cos(math.radians(angle_deg))
    y = center[1] + side * math.sin(math.radians(angle_deg))
    return (x, y)


def get_hex_corners(center, side) -> list[tuple[float, float]]:
    corners = list()
    for i in range(6):
        corners.append(pointy_hex_corner(center, side, i))

    return corners


all_hexagons = corner1_hexagons + corner2_hexagons + corner3_hexagons + corner4_hexagons + corner5_hexagons + corner6_hexagons + edge1_hexagons + edge2_hexagons + edge3_hexagons + edge4_hexagons + edge5_hexagons + edge6_hexagons
all_circles = list()

for hexagon in all_hexagons:
    all_circles.extend(get_hex_corners(hexagon, side))

all_circles.extend(all_hexagons)

filtered_circles = list(set([i for i in all_circles]))

circles_latlon = list()

for circle in filtered_circles:
    circles_latlon.append(utm.to_latlon(circle[0], circle[1], 35, 'T'))


print(len(circles_latlon))

with open('data.csv', 'w') as f:
     
    # using csv.writer method from CSV package
    write = csv.writer(f)
     
    write.writerow(["lat", "long"])
    write.writerows(circles_latlon)


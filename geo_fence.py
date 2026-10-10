from shapely.geometry import Point, Polygon
import matplotlib.path as mpltPath
from functools import reduce
import operator
import math
import random
#coords = [[ 12.934158,77.609316], [ 12.934796,77.609852],[ 12.934183,77.610646], [ 12.933551,77.610100], [12.934158,77.609316]]
#clg ground
coords = [[9.097791, 76.487491],[9.097810, 76.487754],[9.097499, 76.487793],[9.097487, 76.487566]]
#batminton court
#coords =[[1,1],[1,2],[3,2],[3,1]]
#sorting the geofence coords in clockwise direction
center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), coords), [len(coords)] * 2))
coords = sorted(coords, key=lambda coord: (-135 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)

#Testing if a point inside or outside
poly = Polygon(coords)

#point = Point(12.933556,77.609854)
point = Point(2.5,1.5)

print(coords) #print coordinates
"""if(point.within(poly)):
    print("Inside")
else:
    print("Outside")"""


def generate_random_point_in_polygon(poly=poly):
    minx, miny, maxx, maxy = poly.bounds
    while True:
        p = Point(round(random.uniform(minx, maxx), 6), round(random.uniform(miny, maxy), 6))
        if poly.contains(p):
            return p.x, p.y  # returns longitude and latitude separately


# Generate 10 random points within the polygon
"""for _ in range(10):
    latitudee,longitudee = generate_random_point_in_polygon()
    print("lat",latitudee,"long",longitudee)"""
x,y=generate_random_point_in_polygon()
print(x ,",", y)




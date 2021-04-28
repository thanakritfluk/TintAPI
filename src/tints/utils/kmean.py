from math import sqrt
import colorsys
from src.tints.settings import RETURN_INDEX, NUMBER_K, BLACK_THRESHOLD
import random
try:
  import Image
except ImportError:
  from PIL import Image,ImageColor

class Point:
  
  def __init__(self, coordinates):
    self.coordinates = coordinates

class Cluster:
  
  def __init__(self, center, points):
    self.center = center
    self.points = points

class KMeans:
  
  def __init__(self, n_clusters, min_diff = 1):
    self.n_clusters = n_clusters
    self.min_diff = min_diff
    
  def calculate_center(self, points):    
    n_dim = len(points[0].coordinates)    
    vals = [0.0 for i in range(n_dim)]    
    for p in points:
      for i in range(n_dim):
        vals[i] += p.coordinates[i]
    coords = [(v / len(points)) for v in vals]    
    return Point(coords)
  
  def assign_points(self, clusters, points):
    plists = [[] for i in range(self.n_clusters)]

    for p in points:
      smallest_distance = float('inf')

      for i in range(self.n_clusters):
        distance = euclidean(p, clusters[i].center)
        if distance < smallest_distance:
          smallest_distance = distance
          idx = i

      plists[idx].append(p)
    
    return plists
    
  def fit(self, points):
    clusters = [Cluster(center=p, points=[p]) for p in random.sample(points, self.n_clusters)]
    
    while True:

      plists = self.assign_points(clusters, points)

      diff = 0

      for i in range(self.n_clusters):
        if not plists[i]:
          continue
        old = clusters[i]
        center = self.calculate_center(plists[i])
        new = Cluster(center, plists[i])
        clusters[i] = new
        diff = max(diff, euclidean(old.center, new.center))

      if diff < self.min_diff:
        break

    return clusters

def euclidean(p, q):
  n_dim = len(p.coordinates)
  return sqrt(sum([
      (p.coordinates[i] - q.coordinates[i]) ** 2 for i in range(n_dim)
  ]))

def is_black_color(color):
    is_black = False
    h, s, v = colorsys.rgb_to_hsv(color[0], color[1], color[2])
    if v <= BLACK_THRESHOLD:
        is_black = True
    return is_black

def get_points(image_path):  
  img = Image.open(image_path)
  img.thumbnail((200, 400))
  img = img.convert("RGB")
  w, h = img.size
  points = []
  for count, color in img.getcolors(w * h):
    for _ in range(count):
      if not is_black_color(Point(color).coordinates):
        points.append(Point(color)) 
  return points

def rgb_to_hex(rgb):
  return '#%s' % ''.join(('%02x' % p for p in rgb))

def hex_to_rgb(hex_list):
    rgb_list = []
    for i in hex_list:
        rgb_list.append(ImageColor.getcolor(i, "RGB"))
    return rgb_list

def get_colors(image_path, n_colors=NUMBER_K):
  points = get_points(image_path)
  clusters = KMeans(n_clusters=n_colors).fit(points)
  clusters.sort(key=lambda c: len(c.points), reverse = True)
  rgbs = [map(int, c.center.coordinates) for c in clusters]
  hex_list = list(map(rgb_to_hex, rgbs))
  # print("Hex Kmean 5 n =", hex_list)
  rgb_list = hex_to_rgb(hex_list)
  # print("RGB Kmean 5 n =", rgb_list)
  return rgb_list

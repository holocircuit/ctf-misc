s = open("location.csv","r").read().strip().split("\n")[1:]

def get_lat_long(row):
  s = row.split(",")
  return (float(s[2]), float(s[3]))

lat_long = list(map(get_lat_long, s))

lats  = list(map(lambda a: a[0], lat_long))
longs = list(map(lambda a: a[1], lat_long))

# linearly rescale the lats and longs to be in a different interval
lats  = list(map(lambda x: (x + 95.0) * 40, lats))
longs = list(map(lambda x: (x + 15.0) * 40, lats))

print(max(longs), min(longs))

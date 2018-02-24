import math

N = int(input())
positions = []
for _ in range(N):
    s = input()
    x = float(s.split(" ")[0])
    y = float(s.split(" ")[1])

    # we optimise the function f below by putting these in polar co-ordinates, so we only have to do 1 trig operation each time
    r = math.sqrt(x*x + y*y)
    if x == 0:
      theta = math.pi / 2
    else:
      theta = math.atan2(y, x)
    positions.append((r, theta))

def f(theta):
    values = []
    for (r, theta2) in positions:
        values.append(r * math.cos(theta - theta2))
    return max(values) - min(values)

MAX_ERROR = 0.0000005
INTERVALS = 200
# the period of the function is pi, but we'll take two intervals in case the lowest point is near an endpoint
(lower, upper) = (0, 2*math.pi)

diff = 1

while diff > MAX_ERROR / 2:
    # improve the interval
    length = (upper - lower) / INTERVALS
    inputs = [lower + i*length for i in range(INTERVALS + 1)]
    points_on_graph = [(x, f(x)) for x in inputs]

    outputs = [x[1] for x in points_on_graph]

    min_output = min(outputs)
    max_output = max(outputs)
    diff = max_output - min_output
    print("%.12f %.12f" % (diff, length))
    if diff <= MAX_ERROR / 2:
        break

    # find the input which gives the lowest output
    lowest_point = points_on_graph[0]
    for point in points_on_graph[1:]:
        if point[1] < lowest_point[1]:
            lowest_point = point

    (lower, upper) = (lowest_point[0] - length, lowest_point[0] + length)

print("%6f" % min_output)

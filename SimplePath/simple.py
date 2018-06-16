import numpy as np

points = [(0, 0, "point_start")]
f = open("pointsMatrix.txt", "r")
while True:
    loci = str(f.readline())
    if loci:
        pass
    else:
        break
    loci = loci.replace("\n", "")
    loci = loci.split(" ")
    points.append((float(loci[1]), float(loci[2]), loci[0]))

matrix = np.zeros(shape=(101, 101))

for i in range(len(points)):
    row = points[i][0]
    col = points[i][1]

    matrix[int(row), int(col)] = 1

total_dis = 0
row_dis = []

def check_start_end(rows_next):
    points = []
    cu_matrix = list(matrix[rows_next])
    if sum(cu_matrix) == 0:
        return None, None

    else:
        for col in range(len(cu_matrix)):
            if cu_matrix[col] == 1:
                points.append(col)
        return points[0], points[-1]

def judge_route(start, end, flag):
    positive = 2 * flag + start
    negative = (100 - end) + (100 - flag)
    route = 0
    if negative < positive:
        route = 1
    return route

def positive(rows, index):
    global total_dis, row_dis
    flag = 0
    row_current = 0.0
    route = 0

    for col in range(len(rows)):
        if rows[col] == 1:
            row_current = col - flag
            flag = col
    if index < 100:
        rows_next = index + 1
        start, end = check_start_end(rows_next)
        if start == end == None:
            route = 0
        else:
            route = judge_route(start, end, flag)

    if route == 0:

        total_dis += 2 * row_current
    elif route == 1:
        total_dis += 100

    row_dis.append(row_current)
    return route

def negative(rows, index):
    global  total_dis, row_dis
    flag = 0
    row_current = 0.0
    route = 0

    rows = list(rows)
    rows.reverse()

    for col in range(101):
        if rows[col] == 1:
            row_current = col - flag
            flag = col
    rows.reverse()
    if index < 100:
        rows_next = index + 1
        start, end = check_start_end(rows_next)
        if start == end == None:
            route = 0
        else:
            route = judge_route(start, end, flag)
    if route == 0:
        total_dis += 100
    elif route == 1:
        total_dis += 2 * row_current
    row_dis.append(row_current)
    return route

i = 0
route = 0
for rows in matrix:
    if route == 0:
        route = positive(rows, i)
    elif route == 1:
        route = negative(rows, i)
    i += 1

total_points = len(points)
ave_points = float(total_points) / (100.0 * 100.0)

min_scale_low = 100.0      # 低密度最小值放缩尺度，自己定
max_scale_low = 200.0      # 低密度最大值放缩尺度，自己定

min_scale_high = 150.0     # 高密度最小值放缩尺度，自己定
max_scale_high = 250.0     # 高密度最小值放缩尺度，自己定

if ave_points <= 0.35: # 密度阈值，自己定
    random_min_distance = min_scale_low * np.random.rand()
    random_max_distance = max_scale_low * np.random.rand()
else:
    random_min_distance = min_scale_high * np.random.rand()
    random_max_distance = max_scale_high * np.random.rand()

min_distance = total_dis - random_min_distance
max_distance = total_dis + random_max_distance

print("The min distance is: " + str(min_distance))
print("The max distance is: " + str(max_distance))
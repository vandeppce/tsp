import numpy as np
import matplotlib.pyplot as plt

def calDist(xindex, yindex, points):
    return (np.power(points[xindex][0] - points[yindex][0], 2) + np.power(points[xindex][1] - points[yindex][1], 2)) ** 0.5

def calPathDist(indexList, points):
    sum = 0.0
    for i in range(1, len(indexList)):
        sum += calDist(indexList[i], indexList[i - 1], points)
    return sum

def pathCompare(path1, path2, points):
    if calPathDist(path1, points) <= calPathDist(path2, points):
        return True
    return False

def generateRandomPath(bestPath):
    a = np.random.randint(len(bestPath))
    while True:
        b = np.random.randint(len(bestPath))
        if np.abs(a - b) > 1:
            break
    if a > b:
        return b, a, bestPath[b:a + 1]
    else:
        return a, b, bestPath[a:b + 1]

def reversePath(path):
    rePath = path.copy()
    rePath[1:-1] = rePath[-2:0:-1]
    return rePath

def updateBestPath(bestPath, points):
    count = 0
    while count < MAXCOUNT:
        print(calPathDist(bestPath, points))
        print(bestPath.tolist())
        start, end, path = generateRandomPath(bestPath)
        rePath = reversePath(path)
        if pathCompare(path, rePath, points):
            count += 1
            continue
        else:
            count = 0
            bestPath[start:end + 1] = rePath
    return bestPath

'''
def draw(bestPath):
    ax = plt.subplot(111, aspect='equal')
    ax.plot(cities[:, 0], cities[:, 1], 'x', color='blue')
    for i, city in enumerate(cities):
        ax.text(city[0], city[1], str(i))
    ax.plot(cities[bestPath, 0], cities[bestPath, 1], color='red')
    plt.show()
'''

def opt2():
    # 随便选择一条可行路径
    bestPath = np.arange(0, len(points))
    bestPath = np.append(bestPath, 0)
    bestPath = updateBestPath(bestPath, points)
    for item in bestPath:
        print(points[item][2])

MAXCOUNT = 100
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

opt2()
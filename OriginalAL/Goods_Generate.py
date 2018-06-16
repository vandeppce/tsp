import random
import numpy as np
import matplotlib.pyplot as plt

def generate():
    row = []
    space = []
    size = 40
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for i in range(1, size+1):
        for j in range(1, size+1):
            #plt.scatter(int(i), int(j), c = 'grey')
            row.append(j)
        space.append(row)

    num_points = 5
    points = []

    for num in range(num_points):
        flag = 0
        point = np.random.randint(1, size + 1, size=(1, 2))
        add_point = ["point" + str(num)]

        for item in points:
            if point[0][0] == item[1] and point[0][1] == item[2]:
                flag = 1
                break

        if flag == 0:
            add_point.append(point[0][0])
            add_point.append(point[0][1])
            plt.scatter(point[0][0], point[0][1], c = 'r')
            points.append(add_point)

        if flag == 1:
            num -= 1
            break

    f = open("pointsMatrix.txt", "w")

    for item in points:
        f.write("%s %i %i\n" % (item[0], item[1], item[2]))
    print("货物位置生成成功！")
    plt.show()

generate()
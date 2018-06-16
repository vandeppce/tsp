import tkinter as tk
from Opt_GUI.TSP import TSP
from Opt_GUI.TwoOp import *

from tkinter import messagebox
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
from Opt_GUI.Point import Point
from Opt_GUI.SA import valSimulateAnnealSum
import math
import sys
from random import choice, sample
from Opt_GUI.HC import valHillClimbSum
# from BTrack import *

def generate():
    row = []
    space = []
    size = 100

    generate.f.clf()
    generate.a = generate.f.add_subplot(111)

    color = ['b', 'r', 'y', 'g']

    for i in range(1, size + 1):
        for j in range(1, size + 1):
            row.append(j)
        space.append(row)

    if var_num.get() == "":
        num_points = 40
    else:
        num_points = int(var_num.get())
    points = []

    for num in range(num_points):
        flag = 0
        point = np.random.randint(1, size + 1, size=(1, 2))
        add_point = ["point" + str(num + 1)]

        for item in points:
            if point[0][0] == item[1] and point[0][1] == item[2]:
                flag = 1
                break

        if flag == 0:
            add_point.append(point[0][0])
            add_point.append(point[0][1])

            generate.a.scatter(point[0][0], point[0][1], s=3, color=color[np.random.randint(len(color))])
            generate.a.set_title('The distribution of %d goods' % num_points)
            generate.canvas.draw()

            points.append(add_point)

        if flag == 1:
            num -= 1
            break

    f = open("pointsMatrix.txt", "w")

    for item in points:
        f.write("%s %i %i\n" % (item[0], item[1], item[2]))
    print("货物位置生成成功！")


def optimizer_with_ga():

    if var_iteration.get() == "":
        max_iteration = 1000
    else:
        max_iteration = int(var_iteration.get())
    tsp = TSP()
    distanceOfPath, distances, bestPath = tsp.run(max_iteration)

    generate.f.clf()
    generate.a = generate.f.add_subplot(111)
    generate.a.plot(distances)
    generate.a.set_title('Best path after per iteration')
    generate.canvas.draw()

    path = "bestPath_from_ga.txt"
    fp = open(path, 'w')
    fp.write("-> point_start\n")
    for item in bestPath:
        fp.write("-> %s\n" % item)
    fp.write("-> point_start\n")
    messagebox.showinfo(title='Result', message="After %d iterations, the minimum distance is %f, and the best path has been written into %s"
                                                % (max_iteration, distanceOfPath, path))

def optimizer_with_2op():

    if var_iteration_for_2op.get() == "":
        max_iteration = 1000
    else:
        max_iteration = int(var_iteration_for_2op.get())


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

    bestpath, distanceOfPath, distances = opt2(points, max_iteration)

    generate.f.clf()
    generate.a = generate.f.add_subplot(111)
    generate.a.plot(distances)
    generate.a.set_title('Best path after per iteration')
    generate.canvas.draw()

    path = "bestPath_from_2op.txt"
    fp = open(path, 'w')
    for item in bestpath:
        fp.write("-> %s\n" % points[item][2])

    messagebox.showinfo(title='Result',
                        message="After %d iterations, the minimum distance is %f, and the best path has been written into %s"
                                % (max_iteration, distanceOfPath, path))

def conflict(k):
    global n,graph,x,best_x,min_cost
    # 第k个节点，是否前面已经走过
    if k < n and x[k] in x[:k]:
        return True
    # 回到出发节点
    if k == n and x[k] != x[0]:
        return True
    # 前面部分解的旅费之和超出已经找到的最小总旅费
    cost = sum([graph[node1][node2] for node1,node2 in zip(x[:k], x[1:k+1])])
    if 0 < min_cost < cost:
        return True
    return False # 无冲突

def tsp_b(k): # 到达（解x的）第k个节点
    global n,graph,x,X,min_cost,best_x
    if k > n: # 解的长度超出，已走遍n+1个节点 （若不回到出发节点，则 k==n）
        cost = sum([graph[node1][node2] for node1,node2 in zip(x[:-1], x[1:])]) # 计算总旅费
        if min_cost == 0 or cost < min_cost:
            best_x = x[:]
            min_cost = cost
            #print(x)
    else:
        for node in graph[x[k-1]]: # 遍历节点x[k-1]的邻接节点（状态空间）
            x[k] = node
            if not conflict(k): # 剪枝
                tsp_b(k+1)

def optimizer_with_sa():
    parent_dir = os.path.abspath(".")
    filename = parent_dir + "/pointsMatrix.txt"
    lines = open(filename).readlines()
    list = []
    for line in lines:
        params = line.strip().split()
        point = Point(params[1], params[2])
        list.append(point)

    num = len(list)
    arr = [[col for col in range(num)] for row in range(num)]

    for row in range(num):
        for col in range(num):
            if col == row:
                arr[row][col] = 0
            else:
                p1 = list[row]
                p2 = list[col]
                arr[row][col] = round(math.sqrt(math.pow((p1.x - p2.x), 2) + math.pow((p1.y - p2.y), 2)),2)  # 求欧式距离，保留2位小数

    indexList = [i for i in range(num)]  # 原始的节点序列
    selectedList = []  # 选择好的元素

    mincost = sys.maxsize  # 最小的花费
    steplist = [0]
    count = 0  # 计数器
    t = 100  # 初始温度
    t_min = 95  # 最小温度

    while count < num:
        count += 1
        # 构建一个邻域: 如果indexList中元素个数大于10个，则取样的个数为剩余元素个数的十分之一。否则为剩余元素个数对10的取余数
        leftItemNum = len(indexList)
        #  print "leftItemNum:" ,leftItemNum
        nextnum = leftItemNum // 10 if leftItemNum >= 10 else leftItemNum % 10

        nextnodeList = sample(indexList, nextnum)  # 从剩余的节点中选出nextnum个节点

        if len(selectedList) == 0:
            item = choice(nextnodeList)
            selectedList.append(item)
            indexList.remove(item)
            mincost = 0
            continue

        curnode = selectedList[len(selectedList) - 1]

        nextnode, maxcost, t = valSimulateAnnealSum(curnode, nextnodeList, t,t_min,arr)  # 对待选的序列路径求和

        # 将返回的路径值添加到原来的路径值上，同时，在剩余的节点序列中，删除nextnode节点
        mincost += maxcost
        steplist.append(mincost)
        indexList.remove(nextnode)
        selectedList.append(nextnode)
    path = 'bestPath_from_sa.txt'
    fp = open(path, 'w')
    fp.write("-> point_start\n")
    for item in selectedList:
        item = "point" + str(item + 1)
        fp.write("-> %s\n" % item)
    fp.write("-> point_start\n")
    messagebox.showinfo(title='Result',
                        message="The minimum distance is %f, and the best path has been written into %s" % (
                        mincost, path))

    generate.f.clf()
    generate.a = generate.f.add_subplot(111)
    generate.a.plot(steplist)
    generate.a.set_title('Total path after each step')
    generate.canvas.draw()

def optimizer_with_hc():
    parent_dir = os.path.abspath(".")
    filename = parent_dir + "/pointsMatrix.txt"
    lines = open(filename).readlines()
    list = []
    for line in lines:
        params = line.strip().split()
        point = Point(params[1], params[2])
        list.append(point)

    num = len(list)
    arr = [[col for col in range(num)] for row in range(num)]

    for row in range(num):
        for col in range(num):
            if col == row:
                arr[row][col] = 0
            else:
                p1 = list[row]
                p2 = list[col]
                arr[row][col] = round(math.sqrt(math.pow((p1.x - p2.x), 2) + math.pow((p1.y - p2.y), 2)),2)  # 求欧式距离，保留2位小数
    cost = 0
    slist = []
    leftnodeList = [i for i in range(num)]  ### 原始的节点序列
    finalcost = 0
    finallist = [0]
    count = 0
    while count < num:
        count += 1
        # 构建一个邻域: 如果indexList中元素个数大于10个，则取样的个数为剩余元素个数的十分之一。否则为剩余元素个数对10的取余数
        leftItemNum = len(leftnodeList)
        nextnum = leftItemNum // 10 if leftItemNum >= 10 else leftItemNum % 10

        nodeList = sample(leftnodeList, nextnum)  ### 从剩余的节点中选出nextnum个节点

        if len(slist) == 0:
            item = choice(nodeList)
            slist.append(item)
            nodeList.remove(item)
            finalcost = 0
            continue

        curnode = slist[len(slist) - 1]

        nextnode, maxcost = valHillClimbSum(curnode, nodeList, arr)  # 对待选的序列路径求和

        # 将返回的路径值添加到原来的路径值上，同时，在剩余的节点序列中，删除nextnode节点
        finalcost += maxcost
        finallist.append(finalcost)
        leftnodeList.remove(nextnode)
        slist.append(nextnode)

    path = 'bestPath_from_hc.txt'
    fp = open(path, 'w')
    fp.write("-> point_start\n")
    for item in slist:
        item = "point" + str(item + 1)
        fp.write("-> %s\n" % item)
    fp.write("-> point_start\n")
    messagebox.showinfo(title='Result',
                        message="The minimum distance is %f, and the best path has been written into %s" % (finalcost, path))

    generate.f.clf()
    generate.a = generate.f.add_subplot(111)
    generate.a.plot(finallist)
    generate.a.set_title('Total path after each step')
    generate.canvas.draw()

def optimizer_with_bt():
    global x, X, min_cost, best_x, n, graph

    points = [(0, 0, "point0")]
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

    n = len(points)
    distances = []
    for item1 in points:
        distance = []
        for item2 in points:
            tmp_distance = np.sqrt((item1[0] - item2[0]) ** 2 + (item1[1] - item2[1]) ** 2)
            distance.append(tmp_distance)
        distances.append(distance)

    graph = []

    for i in range(n):
        graph_item = {}
        for j in range(n):
            if i == j:
                continue
            graph_item[j] = distances[i][j]
        graph.append(graph_item)

    x = [0] * (n + 1)  # 一个解（n+1元数组，长度固定）
    X = []  # 一组解
    best_x = [0] * (n + 1)  # 已找到的最佳解（路径）
    min_cost = 0  # 最小旅费

    x[0] = 0  # 出发节点：路径x的第一个节点（随便哪个）
    tsp_b(1)  # 开始处理解x中的第2个节点
    path = "bestPath_from_btrack.txt"
    fp = open(path, 'w')
    for item in best_x:
        if item == 0:
            item = "point_start"
        else:
            item = "point" + str(item)
        fp.write("-> %s\n" % item)
    messagebox.showinfo(title='Result',
                        message="The minimum distance is %f, and the best path has been written into %s" % (min_cost, path))
    print(best_x)

matplotlib.use('TKAgg')

window = tk.Tk()

generate.f = Figure(figsize=(4,3))
generate.canvas = FigureCanvasTkAgg(generate.f, master=window)
generate.canvas.draw()
generate.canvas.get_tk_widget().grid(row=0, columnspan=3)

window.title('Welcome to path optimizer simulator')
window.geometry('700x300')

tk.Label(window, text = "goods generation").place(x = 375, y = 70)
tk.Label(window, text = "ga path optimizer").place(x = 375, y = 100)
tk.Label(window, text = "2op path optimizer").place(x = 375, y = 130)
tk.Label(window, text = "annealing optimizer").place(x = 375, y = 160)
tk.Label(window, text = "hill climb optimizer").place(x = 375, y = 190)
tk.Label(window, text = "btrack path optimizer").place(x = 375, y = 220)

var_num = tk.StringVar()
entry_num = tk.Entry(window, textvariable=var_num).place(x = 625, y = 70, width = 50)

var_iteration = tk.StringVar()
entry_iteration = tk.Entry(window, textvariable=var_iteration).place(x = 625, y = 100, width = 50)

var_iteration_for_2op = tk.StringVar()
entry_iteration2op = tk.Entry(window, textvariable=var_iteration_for_2op).place(x = 625, y = 130, width = 50)

# var_iteration_for_bt = tk.StringVar()
# entry_iterationbtrack = tk.Entry(window, textvariable=var_iteration_for_bt).place(x = 300, y = 390, width = 50)

btn_genetate = tk.Button(window, text = 'generate', command = generate).place(x = 525, y = 70)
btn_optimizer = tk.Button(window, text = 'GAopt', command = optimizer_with_ga).place(x = 525, y = 100)
btn_optimizer2op = tk.Button(window, text = "2OPopt", command = optimizer_with_2op).place(x = 525, y = 130)
btn_optimizersa = tk.Button(window, text = "SAopt", command = optimizer_with_sa).place(x = 525, y = 160)
btn_optimizerhc = tk.Button(window, text = "HCopt", command = optimizer_with_hc).place(x = 525, y = 190)
btn_optimizerbt = tk.Button(window, text = "BTopt", command = optimizer_with_bt).place(x = 525, y = 220)

window.mainloop()
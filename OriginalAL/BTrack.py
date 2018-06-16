import numpy as np

'''
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

# 旅行商问题（TSP）
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
'''

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
x = [0]*(n+1) # 一个解（n+1元数组，长度固定）
X = []     # 一组解
best_x = [0]*(n+1) # 已找到的最佳解（路径）
min_cost = 0    # 最小旅费

'''
# 测试
x[0] = 0 # 出发节点：路径x的第一个节点（随便哪个）
tsp_b(1)  # 开始处理解x中的第2个节点
print(best_x)
print(min_cost)
'''
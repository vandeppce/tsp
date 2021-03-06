# -*- encoding: utf-8 -*-

import math
from Opt_GUI.GA import GA


class TSP(object):
    def __init__(self, aLifeCount=100, ):
        self.initPoints()
        self.lifeCount = aLifeCount
        self.ga = GA(aCrossRate=0.7,
                     aMutationRate=0.02,
                     aLifeCount=self.lifeCount,
                     aGeneLength=len(self.points),
                     aMatchFun=self.matchFun())

    def initPoints(self):
        self.points = []

        f = open("pointsMatrix.txt", "r")
        while True:
            # 一行一行读取
            loci = str(f.readline())
            if loci:
                pass  # do something here
            else:
                break
                # 用readline读取末尾总会有一个回车，用replace函数删除这个回车
            loci = loci.replace("\n", "")
            # 按照空格分割
            loci = loci.split(" ")

            self.points.append((float(loci[1]), float(loci[2]), loci[0]))


    # distance就是计算这样走要走多长的路
    def distance(self, order):
        distance = 0.0
        # i从-1到32,-1是倒数第一个
        start = self.points[0]
        end = self.points[len(self.points) - 2]

        for i in range(0, len(self.points) - 1):
            index1, index2 = order[i], order[i + 1]
            city1, city2 = self.points[index1], self.points[index2]
            distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
        distance += math.sqrt(start[0] ** 2 + start[1] ** 2)
        distance += math.sqrt(end[0] ** 2 + end[0] ** 2)

        return distance


        # 适应度函数，因为我们要从种群中挑选距离最短的，作为最优解，所以（1/距离）最长的就是我们要求的

    def matchFun(self):
        return lambda life: 1.0 / self.distance(life.gene)

    def run(self, n=0):

        distances = []
        bestPath = []
        while n > 0:
            self.ga.next()
            distance = self.distance(self.ga.best.gene)

            distances.append(distance)

            print(("%d : %f") % (self.ga.generation, distance))
            print(self.ga.best.gene)
            n -= 1
        print("经过%d次迭代，最优解距离为：%f" % (self.ga.generation, distance))
        print("遍历点顺序为：")

        print("point_start")
        for i in self.ga.best.gene:
            print(self.points[i][2])
            bestPath.append(self.points[i][2])
        print("point_start")
        distanceOfPath = distance
        return distanceOfPath, distances, bestPath


def main():
    max_iteration = 500
    tsp = TSP()
    tsp.run(max_iteration)


if __name__ == '__main__':
    main()
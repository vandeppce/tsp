import sys
from random import choice,shuffle,sample,uniform

def valSimulateAnnealSum(curnode,nextnodeList,t,t_min,arr):

    if nextnodeList == None or len(nextnodeList) < 1 :
        print("empty")
        return 0

    maxcost = sys.maxsize
    retnode = 0

    for node in nextnodeList:
        # print "curnode : ",curnode ," node: " ,node ," mincost : ",mincost

        t *= 0.9  ## 退火因子
        if arr[curnode][node] < maxcost:

            maxcost = arr[curnode][node]
            retnode = node
            ## 以一定的概率接受较差的解
        else:
            r = uniform(0,1)
            if arr[curnode][node] > maxcost and t > t_min and math.exp(( arr[curnode][node] - maxcost ) / t) > r:
                retnode = node
                maxcost = arr[curnode][node]
                return(retnode,maxcost,t)

    return (retnode,maxcost,t)
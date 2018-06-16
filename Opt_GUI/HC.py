import sys
def valHillClimbSum(curnode,nextnodeList,arr):

    if nextnodeList == None or len(nextnodeList) < 1 :
        print("empty")
        return 0

    maxcost = sys.maxsize

    retnode = 0
    for node in nextnodeList:
    # print "curnode : ",curnode ," node: " ,node ," mincost : ",mincost
        if arr[curnode][node] < maxcost :
            maxcost = arr[curnode][node]
            retnode = node
        else:
            return (retnode,maxcost)

    return (retnode,maxcost)
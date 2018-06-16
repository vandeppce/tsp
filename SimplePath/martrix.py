import numpy as np

m=0

f = open('test.txt', 'w')
while m<100:
    data = np.random.randint(0, 2, size=(5, 5))
    total_dis = 0
    end_points = []
    print(data)
    for row in range(5):
        end = 0
        for col in range(5):
            if data[row, col] == 1:
                end = col
        end_points.append(end)

    for i in range(5):
        if data[4,i]==1:
            total = sum(end_points)+4+i

    num=0
    for i in range(5):
        for j in range(5):
            if data[i,j]==1:
                num=num+1
  
    print("Goods number= "+str(num))        
            
    print("Total length= "+str(total))
    
    m=m+1
    print("这是第 "+str(m)+"次数据")

    f.write("迭代次数: {0}, 商品总数: {1}, 路径长度: {2}\n".format(m, num, total))

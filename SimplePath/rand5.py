import numpy as np

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

end = end_points[-1]
back1 = end + 4

back2 = (4 - end) + 4 + 4

back = min(back1, back2)

total = sum(end_points) + back
print(total)
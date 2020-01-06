position = [[-0.005, -0.0035], [-0.0005, -0.0032], [-0.0007, -0.0003], [0, 0.0001], [0.0007, -0.000175],
            [0.0025, -0.00025]]
points = []
result = []

for index in range(len(position)):
    points.append([len(result), index])
    x = position[index][0]
    y = position[index][1]
    for stay in range(1000):
        result.append([x * 1E5, y * 1E5])

    next_index = index + 1
    if next_index < len(position):
        offset_x = (position[next_index][0] - x) / 1000
        offset_y = (position[next_index][1] - y) / 1000
        for diff in range(1000):
            result.append([(x + offset_x * diff) * 1E5, (y + offset_y * diff) * 1E5])

json = {"position": result, "points": points}

print(str(json))

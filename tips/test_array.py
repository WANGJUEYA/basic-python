import copy

coordinates = [
    [[-1.5e-4, 3e-4], [-0.5e-4, 3e-4], [-0.5e-4, 4e-4], [0.5e-4, 4e-4], [0.5e-4, 3e-4], [1.5e-4, 3e-4], [1.5e-4, 2e-4],
     [0.5e-4, 2e-4], [0.5e-4, 1e-4], [-0.5e-4, 1e-4], [-0.5e-4, 2e-4], [-1.5e-4, 2e-4], [-1.5e-4, 3e-4]]]
shape = coordinates[0]
position = [[-0.005, -0.0035], [-0.0005, -0.0032], [-0.0007, -0.0003], [0, 0.0001], [0.0007, -0.000175],
            [0.0025, -0.00025]]
buildings = []
building = {
    "type": "FeatureCollection",
    "features": [{
        "id": "w23278144",
        "properties": {"height": 22, "levels": 5},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [[-1.5e-4, 3e-4], [-0.5e-4, 3e-4], [-0.5e-4, 4e-4], [0.5e-4, 4e-4], [0.5e-4, 3e-4], [1.5e-4, 3e-4],
                 [1.5e-4, 2e-4], [0.5e-4, 2e-4], [0.5e-4, 1e-4], [-0.5e-4, 1e-4], [-0.5e-4, 2e-4], [-1.5e-4, 2e-4],
                 [-1.5e-4, 3e-4]]]
        },
        "type": "Feature"
    }]
}

index = 0
for i_p in position:
    index += 1
    t_coordinates = []
    t_shape = copy.deepcopy(shape)
    t_build = copy.deepcopy(building)
    for index_s in range(len(t_shape)):
        t_shape[index_s] = [t_shape[index_s][0] + i_p[0], t_shape[index_s][1] + i_p[1]]
    t_coordinates.append(t_shape)
    t_build['features'][0]['geometry']['coordinates'] = t_coordinates
    t_build['features'][0]['id'] = 'position No.' + str(index)
    buildings.append(t_build)
    print(t_build)
str_b = str(buildings)
print(str_b)

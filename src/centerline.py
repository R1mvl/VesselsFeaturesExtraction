import nibabel as nib
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import plotly.graph_objects as go 
from skimage.morphology import skeletonize_3d

img = nib.load('data/output.nii')
data = img.get_fdata()

data = data[:, :, np.any(data, axis=(0, 1))]
data = data[:, np.any(data, axis=(0, 2)), :]
data = data[np.any(data, axis=(1, 2)), :, :]

matrix = np.zeros(data.shape)
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        for k in range(data.shape[2]):
            if data[i,j,k] > 0:
                matrix[i,j,k] = 1

matrix[57, 34, 37] = 0

"""
    Skeletonization
"""

skeleton_matrix = skeletonize_3d(matrix)
skeleton_matrix[skeleton_matrix == 255] = 1

"""
    Topology extraction
"""

centerline = []
extremities = []
intersection = []

skeleton_point = []
for i in range(skeleton_matrix.shape[0]):
    for j in range(skeleton_matrix.shape[1]):
        for k in range(skeleton_matrix.shape[2]):
            if skeleton_matrix[i,j,k] > 0:
                skeleton_point.append([i,j,k])

for i in range(len(skeleton_point)):
    neighbors = skeleton_matrix[skeleton_point[i][0]-1:skeleton_point[i][0]+2, skeleton_point[i][1]-1:skeleton_point[i][1]+2, skeleton_point[i][2]-1:skeleton_point[i][2]+2]
    if np.sum(neighbors) == 3:
        centerline.append(skeleton_point[i])
    elif np.sum(neighbors) == 2:
        extremities.append(skeleton_point[i])
    elif np.sum(neighbors) >= 4:
        intersection.append(skeleton_point[i])

print("Nombre de centerline :", len(centerline))
print("Nombre d'extremities :", len(extremities))
print("Nombre d'intersection :", len(intersection))

graph = []
for i in range(len(skeleton_point)):
    graph.append([skeleton_point[i], []])

for i in range(len(skeleton_point)):
    for j in range(len(skeleton_point)):
        if i != j:
            if skeleton_point[i][0] - 1 <= skeleton_point[j][0] <= skeleton_point[i][0] + 1 and skeleton_point[i][1] - 1 <= skeleton_point[j][1] <= skeleton_point[i][1] + 1 and skeleton_point[i][2] - 1 <= skeleton_point[j][2] <= skeleton_point[i][2] + 1:
                graph[i][1].append(j)
                graph[j][1].append(i)

def removeIntersectionNeighbors(point):
    """
        Remove edges between intersection points if they are already connected to another intersection point

        Args:
            point: list of coordinates of the point [x, y, z]

        Returns:
            None
    """
    neighbors = skeleton_matrix[point[0]-1:point[0]+2, point[1]-1:point[1]+2, point[2]-1:point[2]+2]
    neighbors_intersection = []
    for i in range(neighbors.shape[0]):
        for j in range(neighbors.shape[1]):
            for k in range(neighbors.shape[2]):
                if neighbors[i,j,k] > 0 and [point[0]-1+i, point[1]-1+j, point[2]-1+k] in intersection and [point[0]-1+i, point[1]-1+j, point[2]-1+k] != point:
                    neighbors_intersection.append([point[0]-1+i, point[1]-1+j, point[2]-1+k])

    if len(neighbors_intersection) >= 2:
        pointList = []
        for i in range(len(graph)):
            if graph[i][0] in neighbors_intersection:
                pointList.append(i)
        print(pointList)
        for i in range(len(graph)):
            if i in pointList:
                print(graph[i])
                for j in pointList:
                    while j in graph[i][1]:
                        graph[i][1].remove(j)
        for i in range(len(neighbors_intersection)):
            intersection.remove(neighbors_intersection[i])

for i in intersection:
    removeIntersectionNeighbors(i)

graph2 = []
for i in range(len(graph)):
    if graph[i][0] in intersection:
        graph2.append([graph[i][0], []])
    if graph[i][0] in extremities:
        graph2.append([graph[i][0], []])

def findDeph(graph, final_graph, idx_point, list, last_idx, edge_id):
    x, y, z = graph[idx_point][0]
    list.append([x,y,z])
    graph[idx_point].append(edge_id)
    if graph[idx_point][0] in intersection:
        index = 0
        for i in range(len(final_graph)):
            if final_graph[i][0] == [x,y,z]:
                index = i
                break
        final_graph[index][1].append(last_idx)
        for next in graph[idx_point][1]:
            if graph[next][0] not in list:
                edge_id += 1
                findDeph(graph, final_graph, next, list, index, edge_id)
    elif graph[idx_point][0] in extremities:
        index = 0
        for i in range(len(final_graph)):
            if final_graph[i][0] == [x,y,z]:
                index = i
                break
        final_graph[index][1].append(last_idx)
    else:
        for next in graph[idx_point][1]:
            if graph[next][0] not in list:
                findDeph(graph, final_graph, next, list, last_idx, edge_id)                

findDeph(graph, graph2, 0, [], 0, 0)

"""
    Voxel-branch assignment
"""

# create that find the shortest path from a point to graph point
def find_shortest_path(point, graph):
    """
        Find the shortest path from a point to graph point

        Args:
            point: list of coordinates of the point [x, y, z]
            graph: list of graph points

        Returns:
            list of coordinates of the shortest path
    """
    path = []
    min_dist = 100000
    edge_id = -1
    for idx in range(len(graph)):
        dist = abs(graph[idx][0][0] - point[0]) + abs(graph[idx][0][1] - point[1]) + abs(graph[idx][0][2] - point[2])
        if dist < min_dist:
            min_dist = dist
            edge_id = idx
    path.append(graph[edge_id][0])
    while graph[edge_id][0] != point:
        for i in range(len(graph[edge_id][1])):
            dist = abs(graph[graph[edge_id][1][i]][0][0] - point[0]) + abs(graph[graph[edge_id][1][i]][0][1] - point[1]) + abs(graph[graph[edge_id][1][i]][0][2])
    

point_assignment = np.zeros(matrix.shape)
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        for k in range(matrix.shape[2]): 
            if matrix[i,j,k] != 0:
                min_dist = 100000
                edge_id = -1
                for idx in range(len(graph)):
                    dist = abs(graph[idx][0][0] - i) + abs(graph[idx][0][1] - j) + abs(graph[idx][0][2] - k)
                    if dist < min_dist:
                        min_dist = dist
                        edge_id = graph[idx][2]
                point_assignment[i,j,k] = edge_id

"""
    Feature extraction
"""

"""
    Refinement
"""

"""
    Display graph
"""

"""
f = open("graphtest2.txt", "w")
for i in range(len(graph2)):
    f.write(str(i) + ";" + str([graph2[i][0][0] * -1, graph2[i][0][1] * -1, graph2[i][0][2]]) + ";" + str(graph2[i][1]) + "\n")

f = open("graphtest1.txt", "w")
for i in range(len(graph)):
    f.write(str(i) + ";" + str([graph[i][0][0] * -1, graph[i][0][1] * -1, graph[i][0][2]]) + ";" + str(graph[i][1]) + "\n")

fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(111, projection='3d')

for i in range(0, len(extremities)):
    ax.scatter(extremities[i][0], extremities[i][1], extremities[i][2], c='g', marker='o')

for i in range(0, len(intersection)):
    ax.scatter(intersection[i][0], intersection[i][1], intersection[i][2], c='b', marker='o')

color = ['r', 'g', 'b', 'y', 'c', 'm', 'k', 'w', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'lime', 'teal', 'navy']
for i in range(0, len(graph)):
    for j in range(0, len(graph[i][1])):
        ax.plot([graph[i][0][0], graph[graph[i][1][j]][0][0]], [graph[i][0][1], graph[graph[i][1][j]][0][1]], [graph[i][0][2], graph[graph[i][1][j]][0][2]], c=color[graph[i][2] % len(color)])

for i in range(0, len(graph2)):
    for j in graph2[i][1]:
        ax.plot([graph2[i][0][0], graph2[j][0][0]], [graph2[i][0][1], graph2[j][0][1]], [graph2[i][0][2], graph2[j][0][2]], c='black')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show() """

color = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'black', 'white', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'lime', 'teal', 'navy']
fig = go.Figure()
fig.update_layout(scene=dict(xaxis_title='X Label', yaxis_title='Y Label', zaxis_title='Z Label'))

exx = []
exy = []
exz = []
for i in range(0, len(extremities)):
    exx.append(extremities[i][0])
    exy.append(extremities[i][1])
    exz.append(extremities[i][2])
fig.add_trace(go.Scatter3d(x=exx, y=exy, z=exz, mode='markers', marker=dict(color='green', size=10)))

itx = []
ity = []
itz = []
for i in range(0, len(intersection)):
    itx.append(intersection[i][0])
    ity.append(intersection[i][1])
    itz.append(intersection[i][2])
fig.add_trace(go.Scatter3d(x=itx, y=ity, z=itz, mode='markers', marker=dict(color='blue', size=10)))

for i in range(0, len(graph)):
    for j in range(0, len(graph[i][1])):
        fig.add_trace(go.Scatter3d(x=[graph[i][0][0], graph[graph[i][1][j]][0][0]], y=[graph[i][0][1], graph[graph[i][1][j]][0][1]], z=[graph[i][0][2], graph[graph[i][1][j]][0][2]], mode='lines', line=dict(color=color[graph[i][2] % len(color)], width=6)))

for i in range(0, len(graph2)):
    for j in graph2[i][1]:
        fig.add_trace(go.Scatter3d(x=[graph2[i][0][0], graph2[j][0][0]], y=[graph2[i][0][1], graph2[j][0][1]], z=[graph2[i][0][2], graph2[j][0][2]], mode='lines', line=dict(color='black', width=6, dash='dash')))

x = []
y = []
z = []
c = []
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        for k in range(matrix.shape[2]):
            if matrix[i,j,k] > 0:
                x.append(i)
                y.append(j)
                z.append(k)
                c.append(point_assignment[i,j,k])

fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=4, color=c, colorscale='Portland', opacity=0.8)))

fig.show()
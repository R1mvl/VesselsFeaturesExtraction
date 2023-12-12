import numpy as np
from utils import searchIndexPointfromCoordInGraph
from tqdm import tqdm
import plotly.graph_objects as go

def propagation(data_matrix, graph, i, j, k, alreadyVisited, dist, distMax):
    alreadyVisited.append([i, j, k])

    isFind = searchIndexPointfromCoordInGraph(graph, [i, j, k])
    if isFind != -1 and len(graph[isFind]) > 2:
        return graph[isFind][2]

    if dist < distMax:
        for neighbor in neighbors:
            ni, nj, nk = neighbor
            if data_matrix[ni, nj, nk] == 1 and [ni, nj, nk] not in alreadyVisited:
                id = propagation(data_matrix, graph, ni, nj, nk, alreadyVisited, dist + 1, distMax)
                if id > -1:
                    return id
    return -1



def point_assignment(data_matrix, graph):
    """
        Assign each point of the skeleton to the closest edge of the graph

        Args:
            data_matrix: 3D matrix
            graph: list of graph points

        Returns:
            point_assignment: 3D matrix with the edge id of the closest edge of the graph
    """

    tpa = tqdm(total=len(graph), desc="Feature Annotation", colour="green", bar_format="{desc:30}: {percentage:3.0f}%|{bar:200}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")


    """
    for i in range(point_assignment.shape[0]):
        for j in range(point_assignment.shape[1]):
            for k in range(point_assignment.shape[2]):
                tpa.update(1)
                if data_matrix[i, j, k] == 1:
                    found = False
                    distance = 0
                    while not found:
                        res = propagation(data_matrix, graph, i, j, k, [], 0, distance)
                        if res > -1:
                            found = True
                            point_assignment[i, j, k] = res
                        else:
                            distance += 1 """
    
    queue = []
    queue2 = []
    point_assignment = np.zeros(data_matrix.shape, dtype=int) - 1
    point_assignment2 = np.zeros(data_matrix.shape, dtype=int) - 1
    for i in range(len(graph)):
        coord = graph[i][0]
        queue2.append(coord)
        point_assignment2[coord[0], coord[1], coord[2]] = graph[i][2]

    while len(queue2) > 0:

        queue = queue2.copy()
        point_assignment[point_assignment2 != -1] = point_assignment2[point_assignment2 != -1]

        queue2 = []

        while len(queue) > 0:
            i, j, k = queue[0]
            
            neighbors = []
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    for dk in range(-1, 2):
                        neighbors.append([i + di, j + dj, k + dk])

            histogram = {}
            for neighbor in neighbors:
                ni, nj, nk = neighbor
                if data_matrix[ni, nj, nk] == 1:
                    id = point_assignment[ni, nj, nk]
                    if id >= 0:
                        if id in histogram:
                            histogram[id] += 1
                        else:
                            histogram[id] = 1

            edge_id = -1
            if len(histogram) > 0:
                edge_id = max(histogram, key=histogram.get)

            for neighbor in neighbors:
                ni, nj, nk = neighbor
                if data_matrix[ni, nj, nk] == 1 and point_assignment2[ni, nj, nk] == -1:
                    point_assignment2[ni, nj, nk] = edge_id
                    queue2.append(neighbor)
                    tpa.total += 1        

            queue.pop(0)
            tpa.update(1)
            tpa.refresh()

        #break

    point_assignment[point_assignment2 != -1] = point_assignment2[point_assignment2 != -1]

    tpa.close()
    return point_assignment

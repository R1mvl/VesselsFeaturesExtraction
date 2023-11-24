import numpy as np
from utils import searchIndexPointfromCoordInGraph
from tqdm import tqdm

def propagation(data_matrix, graph, i, j, k, alreadyVisited, dist, distMax):
    alreadyVisited.append([i, j, k])

    isFind = searchIndexPointfromCoordInGraph(graph, [i, j, k])
    if isFind != -1 and len(graph[isFind]) > 2:
        return graph[isFind][2]
        
    neighbors = [
        (i + 1, j, k),
        (i - 1, j, k),
        (i, j + 1, k),
        (i, j - 1, k),
        (i, j, k + 1),
        (i, j, k - 1)
    ]

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

    point_assignment = np.zeros(data_matrix.shape)
    for i in range(point_assignment.shape[0]):
        for j in range(point_assignment.shape[1]):
            for k in range(point_assignment.shape[2]):
                if data_matrix[i, j, k] == 1:
                    found = False
                    distance = 0
                    while not found:
                        res = propagation(data_matrix, graph, i, j, k, [], 0, distance)
                        if res > -1:
                            found = True
                            point_assignment[i, j, k] = res
                        else:
                            distance += 1
    return point_assignment

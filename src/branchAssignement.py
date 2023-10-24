import numpy as np

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
    for i in range(data_matrix.shape[0]):
        for j in range(data_matrix.shape[1]):
            for k in range(data_matrix.shape[2]): 
                if data_matrix[i,j,k] != 0:
                    min_dist = 100000
                    edge_id = -1
                    for idx in range(len(graph)):
                        dist = abs(graph[idx][0][0] - i) + abs(graph[idx][0][1] - j) + abs(graph[idx][0][2] - k)
                        if dist < min_dist:
                            min_dist = dist
                            edge_id = graph[idx][2]
                    point_assignment[i,j,k] = edge_id
    return point_assignment
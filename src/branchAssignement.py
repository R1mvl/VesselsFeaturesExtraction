import numpy as np
from utils import searchIndexPointfromCoordInGraph
import scipy.spatial.distance


def find_shortest_edgeId(point, graph, matrix):
    """
        Find the shortest path from a point to graph point

        Args:
            point: coordinate of a point
            graph: list of graph points with edge id
            matrix: 3D matrix

        Returns:
            edge_id: edge id of the graph point
    """

    visited = []
    queue = [(point, -1)]

    while queue:
        (vertex, edge_id) = queue.pop(0)
        index = searchIndexPointfromCoordInGraph(graph, vertex)
        if index != -1:
            return vertex, graph[index][2]
        
        if vertex in visited:
            continue

        print(vertex)
        visited.append(vertex)

        neighbors = matrix[vertex[0]-1:vertex[0]+2, vertex[1]-1:vertex[1]+2, vertex[2]-1:vertex[2]+2]
        for i in range(neighbors.shape[0]):
            for j in range(neighbors.shape[1]):
                for k in range(neighbors.shape[2]):
                    if neighbors[i,j,k] != 0:
                        queue.append(([vertex[0]-1+i, vertex[1]-1+j, vertex[2]-1+k], edge_id))

    return None, None
    

                        

    
    
def point_assignment(data_matrix, graph):
    """
        Assign each point of the skeleton to the closest edge of the graph

        Args:
            data_matrix: 3D matrix
            graph: list of graph points

        Returns:
            point_assignment: 3D matrix with the edge id of the closest edge of the graph
    """
    """ point_assignment = np.zeros(data_matrix.shape)
    for i in range(point_assignment.shape[0]):
        for j in range(point_assignment.shape[1]):
            for k in range(point_assignment.shape[2]): 
                if data_matrix[i,j,k] != 0:
                    point_assignment[i,j,k] = find_shortest_path([i,j,k], graph, data_matrix)[1] """
    """ print(find_shortest_edgeId([48,24,18], graph, data_matrix)) """

    # for each point find the closest edge and givve to this point the edge id
    point_assignment = np.zeros(data_matrix.shape)
    for i in range(point_assignment.shape[0]):
        for j in range(point_assignment.shape[1]):
            for k in range(point_assignment.shape[2]): 
                if data_matrix[i,j,k] != 0:
                    close = scipy.spatial.distance.cdist([[i,j,k]], [[point[0][0], point[0][1], point[0][2]] for point in graph])
                    point_assignment[i,j,k] = graph[np.argmin(close)][2]
    return point_assignment
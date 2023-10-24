import numpy as np

def getGraphFromSkeleton(skeleton_point):
    """
        This function takes a list of coordinates of the skeleton points and returns a graph of the skeleton.

        Args:
            skeleton_point (list): list of coordinates of the skeleton points

        Returns:
            graph (list): graph of the skeleton
    """
    graph = []
    for i in range(len(skeleton_point)):
        graph.append([skeleton_point[i], []])

    for i in range(len(skeleton_point)):
        for j in range(len(skeleton_point)):
            if i != j:
                if skeleton_point[i][0] - 1 <= skeleton_point[j][0] <= skeleton_point[i][0] + 1 and skeleton_point[i][1] - 1 <= skeleton_point[j][1] <= skeleton_point[i][1] + 1 and skeleton_point[i][2] - 1 <= skeleton_point[j][2] <= skeleton_point[i][2] + 1:
                    graph[i][1].append(j)
                    graph[j][1].append(i)

    return graph

def getPointFeature(skeleton_point, skeleton_matrix):
    """
        This function takes a list of coordinates of the skeleton points and returns a list of coordinates of the centerline points, extremities points and intersection points.

        Args:
            skeleton_point (list): list of coordinates of the skeleton points
            skeleton_matrix (numpy.ndarray): 3D matrix with the skeleton of the input matrix

        Returns:
            centerline (list): list of coordinates of the centerline points
            extremities (list): list of coordinates of the extremities points
            intersection (list): list of coordinates of the intersection points
    """

    centerline = []
    extremities = []
    intersection = []

    for i in range(len(skeleton_point)):
        neighbors = skeleton_matrix[skeleton_point[i][0]-1:skeleton_point[i][0]+2, skeleton_point[i][1]-1:skeleton_point[i][1]+2, skeleton_point[i][2]-1:skeleton_point[i][2]+2]
        if np.sum(neighbors) == 3:
            centerline.append(skeleton_point[i])
        elif np.sum(neighbors) == 2:
            extremities.append(skeleton_point[i])
        elif np.sum(neighbors) >= 4:
            intersection.append(skeleton_point[i])

    return centerline, extremities, intersection

def removeIntersectionCycle(intersection, skeleton_matrix, graph):
    """
        This function removes the intersection points that are in a cycle.

        Args:
            intersection (list): list of coordinates of the intersection points
            skeleton_matrix (numpy.ndarray): 3D matrix with the skeleton of the input matrix
            graph (list): graph of the skeleton

        Returns:
            None
    """

    def removeIntersectionNeighbors(point):
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
            for i in range(len(graph)):
                if i in pointList:
                    for j in pointList:
                        while j in graph[i][1]:
                            graph[i][1].remove(j)
            for i in range(len(neighbors_intersection)):
                intersection.remove(neighbors_intersection[i])

    for i in intersection:
        removeIntersectionNeighbors(i)

def findLineFromCenterLine(extremities, intersection, graph):
    """
        This function make a list of coordinates of the lines that connect all the extremities points and the intersection points.

        Args:
            extremities (list): list of coordinates of the extremities points
            intersection (list): list of coordinates of the intersection points
            graph (list): graph of the skeleton

        Returns:
            lines (list): graph of the lines
    """ 

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

    return graph2

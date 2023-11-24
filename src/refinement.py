import math
from utils import searchIndexPointfromCoordInGraph

def minimumDistanceToSurface(point, data_matrix):
    """
        This fonction calculates the radius of the inner circle of the intersection point.

        Args:
            point (list): intersection point [x, y, z]
            data_matrix (list): matrix of the dataset

        Returns:
            radius (float): radius of the inner circle
    """

    radius = 0
    sphere = set()
    check = True
    while check:
        for i in range(0, 360, 10):
            for j in range(0, 360, 10):
                x = point[0] + radius * math.cos(math.radians(i)) * math.sin(math.radians(j))
                y = point[1] + radius * math.sin(math.radians(i)) * math.sin(math.radians(j))
                z = point[2] + radius * math.cos(math.radians(j))
                sphere.add((round(x), round(y), round(z)))

        for i in sphere:
            if data_matrix[i[0], i[1], i[2]] == 0:
                check = False
                break
        
        radius += 1

    return radius - 1

def length(intersection_point, extremity_point):
    """
        This fonction calculates the length between the intersection point and the extremity point.

        Args:
            intersection_point (list): intersection point [x, y, z]
            extremity_point (list): extremity point [x, y, z]

        Returns:
            length (float): length between the intersection point and the extremity point
    """
    
    return math.sqrt((intersection_point[0] - extremity_point[0])**2 + (intersection_point[1] - extremity_point[1])**2 + (intersection_point[2] - extremity_point[2])**2)

def get_intersection(graph, extrimity_point, intersections, data_matrix):
    """
        This function takes a graph and an extremity point and returns the intersection point connected to the extremity point.

        Args:
            graph (list): graph of the skeleton
            extrimity_point (list): coordinates of the extremity point [x, y, z]
            intersections (list): list of coordinates of the intersection point

        Returns:
            intersection (list): list of coordinates of the intersection point [x, y, z]
            averageRadius (list): list of the radius of the inner circle of the intersection point
    """

    def findIntersection(graph, idx_point, list, avgRadius):
        x, y, z = graph[idx_point][0]
        list.append([x,y,z])
        if graph[idx_point][0] in intersections:
            return graph[idx_point][0]
        else:
            for next in graph[idx_point][1]:
                if graph[next][0] not in list:
                    avgRadius.append(minimumDistanceToSurface(graph[next][0], data_matrix))
                    intersection_point = findIntersection(graph, next, list, avgRadius)
                    if intersection_point != None:
                        return intersection_point
    
    avgRadius = []
    intersection_point = findIntersection(graph, searchIndexPointfromCoordInGraph(graph, extrimity_point), [], avgRadius)
    averageRadius = sum(avgRadius) / len(avgRadius)

    return intersection_point, averageRadius

def bulge_size(graph, extrimity_point, intersections, data_matrix):
    """
        This function takes an extremity point and an intersection point and returns bulge size of the edge.

        Args:
            extrimity_point (list): coordinates of the extremity point [x, y, z]
            intersection_point (list): coordinates of the intersection point [x, y, z]
            data_matrix (list): matrix of the dataset

        Returns:
            bulge_size (float): bulge size of the edge
    """

    intersection_point, bulge_avg_radius = get_intersection(graph, extrimity_point, intersections, data_matrix)

    bulge_length = length(intersection_point, extrimity_point)
    bulge_inner_length = minimumDistanceToSurface(intersection_point, data_matrix)
    bulge_tip_radius = minimumDistanceToSurface(extrimity_point, data_matrix)

    return (bulge_length - bulge_inner_length + bulge_tip_radius) / bulge_avg_radius, intersection_point

def remove_bulge(data_matrix, point_assignement, intersections, extrimities, intersection_point, extrimity_point, edge_id):
    """
        This function removes the bulge of the edge.

        Args:
            graph (list): graph of the skeleton
            intersections (list): list of coordinates of the intersection point
            extrimities (list): list of coordinates of the extremity point
            intersection_point (list): coordinates of the intersection point [x, y, z]
            extrimity_point (list): coordinates of the extremity point [x, y, z]

        Returns:
            None
    """

    intersections.remove(intersection_point)
    extrimities.remove(extrimity_point)
    data_matrix[point_assignement == edge_id] = 0

def refinement(graph, intersections, extrimities, data_matrix, point_assignement, limit_bulge):
    """
        This function refines the graph by removing all the bulges.

        Args:
            graph (list): graph of the skeleton
            intersections (list): list of coordinates of the intersection point
            extrimities (list): list of coordinates of the extremity point
            data_matrix (list): matrix of the dataset
            point_assignement (list): list of the edge id of the closest edge of the graph
            limit_bulge (float): limit of the bulge size

        Returns:
            graph (list): graph of the skeleton without the bulges
            intersections (list): list of coordinates of the intersection point without the bulges
            extrimities (list): list of coordinates of the extremity point without the bulges
    """

    count = 0
    for extrimity_point in extrimities:

        bulge, intersection_point = bulge_size(graph, extrimity_point, intersections, data_matrix)

        if bulge < limit_bulge:
            idx_point = searchIndexPointfromCoordInGraph(graph, extrimity_point)
            remove_bulge(data_matrix, point_assignement, intersections, extrimities, intersection_point, extrimity_point, graph[idx_point][2])
            count += 1

    return data_matrix, intersections, extrimities, count

def searchIndexPointfromCoordInGraph(graph, coord):
    """
        This function search a coordinate in the graph and return the node if it exists.

        Args:
            graph (list): graph of the skeleton
            coord (list): coordinate of a point

        Returns:
            node (list): node index of the graph if it exists
    """
    for i in range(len(graph)):
        if graph[i][0] == coord:
            return i
    return -1
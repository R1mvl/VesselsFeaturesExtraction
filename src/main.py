from dataset import importMatrixFromNIIFile
from skeletonization import skeletonization, getCoordinatesPoint
from topology import getGraphFromSkeleton, getPointFeature, removeIntersectionCycle, findLineFromCenterLine
from branchAssignement import point_assignment
from visualisation import showGraphCenterline, showGraphLine, showGraphExtremities, showGraphIntersection, showMatrix, show
import numpy as np

data_matrix = importMatrixFromNIIFile('data/output.nii')

# outlier from the dataset so we remove it
data_matrix[57, 34, 37] = 0

skeleton_matrix = skeletonization(data_matrix)
skeleton_point = getCoordinatesPoint(skeleton_matrix)

centerLine, extremities, intersection = getPointFeature(skeleton_point, skeleton_matrix)

graph = getGraphFromSkeleton(skeleton_point)

removeIntersectionCycle(intersection, skeleton_matrix, graph)

graphLine = findLineFromCenterLine(extremities, intersection, graph)
point_edge = point_assignment(data_matrix, graph)

""" 
showGraphExtremities(extremities)
showGraphIntersection(intersection)

showMatrix(data_matrix, point_edge, [4,5])
showGraphLine(graphLine)
showGraphCenterline(graph)
show()
"""

print("Nombre de edgeID different dans point_edge : ", len(np.unique(point_edge)))
print("nombre de edge dans graphLine : ", len(graphLine))

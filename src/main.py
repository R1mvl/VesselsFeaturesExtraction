import datetime
time = datetime.datetime.now()

from utils import searchIndexPointfromCoordInGraph, printTime
from dataset import importMatrixFromNIIFile
from skeletonization import skeletonization, getCoordinatesPoint
from topology import getGraphFromSkeleton, getPointFeature, removeIntersectionCycle, findLineFromCenterLine
from branchAssignement import point_assignment
from visualisation import showGraphCenterline, showGraphLine, showGraphExtremities, showGraphIntersection, showMatrix, show, addPointToGraph, init_layout
import numpy as np


time = printTime("Import :", time)

data_matrix = importMatrixFromNIIFile('data/output.nii', False)
time = printTime("Import NII file:", time)

# outlier from the dataset so we remove it
data_matrix[57, 34, 37] = 0

skeleton_matrix = skeletonization(data_matrix)
skeleton_point = getCoordinatesPoint(skeleton_matrix)
time = printTime("Skeletonization :", time)

centerLine, extremities, intersection = getPointFeature(skeleton_point, skeleton_matrix)
time = printTime("Topology :", time)

graph = getGraphFromSkeleton(skeleton_point)
time = printTime("Graph :", time)

removeIntersectionCycle(intersection, skeleton_matrix, graph)
time = printTime("Remove intersection cycle :", time)

graphLine = findLineFromCenterLine(extremities, intersection, graph)
time = printTime("Find line from center line :", time)
#point_edge = point_assignment(data_matrix, graph)
#time = printTime("Point assignment :", time)

init_layout(graph)

showGraphExtremities(extremities)
showGraphIntersection(intersection)

#showGraphCenterline(graph)
showGraphLine(graphLine)

#showMatrix(data_matrix, point_edge)

#addPointToGraph(48,24,18)

show()
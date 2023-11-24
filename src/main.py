import datetime
time = datetime.datetime.now()

from utils import searchIndexPointfromCoordInGraph, printTime
from dataset import importMatrixFromNIIFile
from skeletonization import skeletonization, getCoordinatesPoint
from topology import getGraphFromSkeleton, getPointFeature, removeIntersectionCycle, findLineFromCenterLine
from FeatureExtraction import point_assignment
from visualisation import showGraphCenterline, showGraphLine, showGraphExtremities, showGraphIntersection, showMatrix, show, addPointToGraph, init_layout
from refinement import refinement
import numpy as np
from tqdm import tqdm

data_matrix = importMatrixFromNIIFile('data/output.nii', False)

data_matrix[57, 34, 37] = 0
data_matrix[221, 79, 213] = 0

count = 1
iteration = 1
timeStep = []

while count > 0:
    print("Iteration : ", iteration)
    iteration += 1
    pbar = tqdm(total=8, bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]', unit='step', colour='#00fff0')
    time = datetime.datetime.now()

    for i in range(data_matrix.shape[0]):
        for j in range(data_matrix.shape[1]):
            for k in range(data_matrix.shape[2]):
                if data_matrix[i, j, k] == 1:
                    neighbors = data_matrix[i-1:i+2, j-1:j+2, k-1:k+2]
                    if np.sum(neighbors) == 1:
                        data_matrix[i, j, k] = 0

    pbar.desc = "Skeletonization"
    skeleton_matrix = skeletonization(data_matrix)
    skeleton_point = getCoordinatesPoint(skeleton_matrix)
    timeStep.append([iteration, "Skeletonization", datetime.datetime.now() - time])
    time = datetime.datetime.now()
    pbar.update(1)

    pbar.desc = "Get point feature"
    centerLine, extremities, intersection = getPointFeature(skeleton_point, skeleton_matrix)
    timeStep.append([iteration, "Get point feature", datetime.datetime.now() - time])
    time = datetime.datetime.now()
    pbar.update(1)

    pbar.desc = "Get graph from skeleton"
    graph = getGraphFromSkeleton(skeleton_point)
    timeStep.append([iteration, "Get graph from skeleton", datetime.datetime.now() - time])
    time = datetime.datetime.now()
    pbar.update(1)

    pbar.desc = "Remove intersection cycle"
    removeIntersectionCycle(intersection, skeleton_matrix, graph)
    timeStep.append([iteration, "Remove intersection cycle", datetime.datetime.now() - time])
    time = datetime.datetime.now()
    pbar.update(1)

    pbar.desc = "Find line from center line"
    graphLine = findLineFromCenterLine(extremities, intersection, graph)
    timeStep.append([iteration, "Find line from center line", datetime.datetime.now() - time])
    time = datetime.datetime.now()
    pbar.update(1)

    pbar.desc = "Point assignment"
    point_edge = point_assignment(data_matrix, graph)
    timeStep.append([iteration, "Point assignment", datetime.datetime.now() - time])
    time = datetime.datetime.now()
    pbar.update(1)

    pbar.desc = "Refinement"
    data_matrix, intersections, extrimities, count = refinement(graph, intersection, extremities, data_matrix, point_edge, 2)
    timeStep.append([iteration, "Refinement", datetime.datetime.now() - time])
    time = datetime.datetime.now()
    pbar.update(1)

    graphLine = findLineFromCenterLine(extremities, intersection, graph)
    timeStep.append([iteration, "Find line from center line", datetime.datetime.now() - time])
    time = datetime.datetime.now()
    pbar.update(1)

    pbar.close()

    print("Nombre de edge retiré : ", count)

init_layout(graph)

showGraphExtremities(extremities)
showGraphIntersection(intersection)

showGraphCenterline(graph)
showGraphLine(graphLine)

#showMatrix(data_matrix, point_edge)

show()

for i in range(len(timeStep)):
    print(timeStep[i][0], " : ", timeStep[i][1], " : ", printTime(timeStep[i][2]))

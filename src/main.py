import datetime
time = datetime.datetime.now()

from utils import searchIndexPointfromCoordInGraph, printTime
from dataset import importMatrixFromNIIFile
from skeletonization import skeletonization
from topology import topology
from FeatureExtraction import point_assignment
from visualisation import showGraphCenterline, showGraphLine, showGraphExtremities, showGraphIntersection, showMatrix, show, addPointToGraph, init_layout
from refinement import refinement
import numpy as np
from tqdm import tqdm

data_matrix = importMatrixFromNIIFile('data/output.nii', False)

count = 1
iteration = 1

while count > 0:
    print("Iteration : ", iteration)
    pbarmain = tqdm(total=4, unit='step', colour='blue', desc="Main", bar_format="{desc:30}: {percentage:3.0f}%|{bar:200}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]", position=0)
    time = datetime.datetime.now()
    timeStep = []

    skeleton_matrix, skeleton_point = skeletonization(data_matrix)
    timeStep.append([iteration, "Skeletonization", datetime.datetime.now() - time])
    time = datetime.datetime.now()
    pbarmain.update(1)
    pbarmain.refresh()

    graph, graphLine, extremities, intersection = topology(skeleton_point, skeleton_matrix)
    timeStep.append([iteration, "Topology", datetime.datetime.now() - time])
    time = datetime.datetime.now()
    pbarmain.update(1)
    pbarmain.refresh()

    point_edge = point_assignment(data_matrix, graph)
    timeStep.append([iteration, "Point assignment", datetime.datetime.now() - time])
    time = datetime.datetime.now()
    pbarmain.update(1)
    pbarmain.refresh()

    data_matrix, intersections, extrimities, count = refinement(graph, intersection, extremities, data_matrix, point_edge, 2)
    timeStep.append([iteration, "Refinement", datetime.datetime.now() - time])
    time = datetime.datetime.now()
    pbarmain.update(1)
    pbarmain.refresh()

    pbarmain.close()

    print("Nombre de edge retiré : ", count)

    for i in range(len(timeStep)):
        print(timeStep[i][0], " : ", timeStep[i][1], " : ", timeStep[i][2])
    iteration += 1

init_layout(graph)

showGraphExtremities(extremities)
showGraphIntersection(intersection)

showGraphCenterline(graph)
showGraphLine(graphLine)

#showMatrix(data_matrix, point_edge, [0,1,2])

show()


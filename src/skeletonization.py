import numpy as np
from skimage.morphology import skeletonize_3d

def skeletonization(matrix):
    """
        This function takes a 3D matrix and returns a 3D matrix with the skeleton of the input matrix.
        The skeleton is the thinnest representation of the input matrix.

        Args:
            matrix (numpy.ndarray): 3D matrix

        Returns:
            skeleton_matrix (numpy.ndarray): 3D matrix with the skeleton of the input matrix
    """
    skeleton_matrix = skeletonize_3d(matrix)
    skeleton_matrix[skeleton_matrix == 255] = 1
    return skeleton_matrix

def getCoordinatesPoint(skeleton_matrix):
    """
        This function takes a 3D matrix and returns a list of coordinates of the skeleton points.

        Args:
            skeleton_matrix (numpy.ndarray): 3D matrix with the skeleton of the input matrix

        Returns:
            skeleton_point (list): list of coordinates of the skeleton points
    """

    skeleton_point = []
    for i in range(skeleton_matrix.shape[0]):
        for j in range(skeleton_matrix.shape[1]):
            for k in range(skeleton_matrix.shape[2]):
                if skeleton_matrix[i,j,k] > 0:
                    skeleton_point.append([i,j,k])

    return skeleton_point
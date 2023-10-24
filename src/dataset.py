import numpy as np
import nibabel as nib

def importMatrixFromNIIFile(path, removeEmptySlices = True):
    """
        This function takes a path to a .nii file and returns a 3D matrix

        Args:
            path (str): path to .nii file
            removeEmptySlices (bool): if True, empty slices are removed from the matrix

        Returns:
            matrix (numpy.ndarray): 3D matrix
    """


    img = nib.load(path)
    data = img.get_fdata()

    if removeEmptySlices:
        data = data[:, :, np.any(data, axis=(0, 1))]
        data = data[:, np.any(data, axis=(0, 2)), :]
        data = data[np.any(data, axis=(1, 2)), :, :]

    matrix = np.zeros(data.shape)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                if data[i,j,k] > 0:
                    matrix[i,j,k] = 1

    return matrix
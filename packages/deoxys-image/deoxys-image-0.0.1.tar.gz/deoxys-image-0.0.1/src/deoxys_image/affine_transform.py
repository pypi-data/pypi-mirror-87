import scipy
from scipy import ndimage
import numpy as np


def get_rotation_matrix(rotation_axis, theta, rank=3):
    r"""
    .. math::

        \begin{pmatrix}
            \cos(\frac{x'}{x})&\cos(\frac{y'}{x})&\cos(\frac{z'}{x})\\
            \cos(\frac{x'}{y})&\cos(\frac{y'}{y})&\cos(\frac{z'}{y})\\
            \cos(\frac{x'}{z})&\cos(\frac{y'}{z})&\cos(\frac{z'}{z})
        \end{pmatrix}

    x, y, z are axis 2, 0, 1 respectively

    Parameters
    ----------
    rotation_axis : [type]
        [description]
    theta : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """
    theta = np.deg2rad(theta)
    if rank == 3:
        if rotation_axis == 0:  # z
            rotation_matrix = np.array([[1, 0, 0],
                                        [0, np.cos(theta), -np.sin(theta)],
                                        [0, np.sin(theta), np.cos(theta)]])

        elif rotation_axis == 1:  # x
            rotation_matrix = np.array([[np.cos(theta), 0, np.sin(theta)],
                                        [0, 1, 0],
                                        [-np.sin(theta), 0, np.cos(theta)]])
        elif rotation_axis == 2:  # y
            rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                        [np.sin(theta), np.cos(theta), 0],
                                        [0, 0, 1]])
    elif rank == 4:
        if rotation_axis == 0:  # z
            rotation_matrix = np.array([[1, 0, 0, 0],
                                        [0, np.cos(theta), -np.sin(theta), 0],
                                        [0, np.sin(theta), np.cos(theta), 0],
                                        [0, 0, 0, 1]])

        elif rotation_axis == 1:  # x
            rotation_matrix = np.array([[np.cos(theta), 0, np.sin(theta), 0],
                                        [0, 1, 0, 0],
                                        [-np.sin(theta), 0, np.cos(theta), 0],
                                        [0, 0, 0, 1]])
        elif rotation_axis == 2:  # y
            rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0, 0],
                                        [np.sin(theta), np.cos(theta), 0, 0],
                                        [0, 0, 1, 0],
                                        [0, 0, 0, 1]])
    else:
        raise ValueError('Rotation matrix only support 3D and 4D tensor')

    return rotation_matrix


def get_shift_matrix(shift, rank=3):
    r"""
    Return the shift matrix in affine transform

    .. math::
        \begin{pmatrix}1&0&offset_x\\
                0&1&offset_y\\
                0&0&1
        \end{pmatrix}


    Parameters
    ----------
    shift : int,
        number of pixel to shift
    rank : int, optional
        the rank of the matrix, by default 3

    Returns
    -------
    np.array
        the shift matrix
    """
    shift_matrix = np.identity(rank)

    shift_matrix[:-1, -1] = shift

    return shift_matrix


def get_zoom_matrix(zoom_factor, rank=3):
    zoom_matrix = np.zeros((rank, rank))

    np.fill_diagonal(zoom_matrix, [zoom_factor for _ in range(rank-1)] + [1])

    return zoom_matrix


def transform_matrix_offset_center(matrix, width, height, depth=None):
    if matrix.shape[0] == 4 and depth is None:
        raise ValueError('4D tensor requires a depth value')

    z = width / 2 - 0.5
    x = height / 2 - 0.5

    if matrix.shape[0] == 3:
        offset_matrix = np.array([[1, 0, z],
                                  [0, 1, x],
                                  [0, 0, 1]])
        reset_matrix = np.array([[1, 0, -z],
                                 [0, 1, -x],
                                 [0, 0, 1]])

    elif matrix.shape[0] == 4:
        y = depth / 2 - 0.5
        offset_matrix = np.array([[1, 0, 0, z],
                                  [0, 1, 0, x],
                                  [0, 0, 1, y],
                                  [0, 0, 0, 1]])
        reset_matrix = np.array([[1, 0, 0, -z],
                                 [0, 1, 0, -x],
                                 [0, 0, 1, -y],
                                 [0, 0, 0, 1]])

    return np.dot(np.dot(offset_matrix, matrix), reset_matrix)


def affine_transform_matrix(rotation_axis=2, theta=0, rank=3,
                            zoom_factor=1, **kwargs):
    transform_matrix = None

    if theta:
        rotation_matrix = get_rotation_matrix(rotation_axis, theta, rank)
        transform_matrix = rotation_matrix

    # if shift:
    #     shift_matrix = get_shift_matrix(shift, rank)

    #     if transform_matrix is None:
    #         transform_matrix = shift_matrix
    #     else:
    #         transform_matrix = np.dot(transform_matrix, shift_matrix)

    if zoom_factor != 1:
        zoom_matrix = get_zoom_matrix(1/zoom_factor, rank)

        if transform_matrix is None:
            transform_matrix = zoom_matrix
        else:
            transform_matrix = np.dot(transform_matrix, zoom_matrix)

    return transform_matrix


def apply_affine_transform(image, mode='constant', cval=0, **kwargs):
    if not 3 <= image.ndim <= 4:
        raise ValueError(
            f'Not support affine transform for tensor of rank {image.ndim}')

    transform_matrix = affine_transform_matrix(rank=image.ndim, **kwargs)

    if transform_matrix is not None:
        offset_matrix = transform_matrix_offset_center(
            transform_matrix, *image.shape[:-1])

        offset = offset_matrix[..., -1]
        offset[-1] = 0
    else:
        transform_matrix = np.identity(image.ndim)
        offset = np.zeros(image.ndim)

    if kwargs.get('shift') is not None:
        offset[:-1] = offset[:-1] + np.array(kwargs['shift'])

    return ndimage.affine_transform(
        image, transform_matrix, offset, mode=mode, cval=cval)


def apply_flip(image, axis):
    image = np.array(image)
    if '__iter__' not in dir(axis):
        axis = [axis]
    if 0 in axis:
        image = image[::-1]

    if 1 in axis:
        image = image[:, ::-1]

    if 2 in axis:
        image = image[:, :, ::-1]

    return image

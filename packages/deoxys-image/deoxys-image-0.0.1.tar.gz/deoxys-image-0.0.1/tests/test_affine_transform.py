import pytest
import numpy as np
from deoxys_image import affine_transform_matrix, apply_affine_transform, \
    get_rotation_matrix, get_zoom_matrix, get_shift_matrix, apply_flip


def test_get_rotation_matrix_error():
    with pytest.raises(ValueError):
        get_rotation_matrix(rotation_axis=0, theta=30, rank=2)


def test_get_rotation_matrix():
    get_rotation_matrix(rotation_axis=0, theta=30, rank=3)
    get_rotation_matrix(rotation_axis=1, theta=30, rank=3)
    get_rotation_matrix(rotation_axis=2, theta=30, rank=3)

    rotation_matrix = get_rotation_matrix(rotation_axis=0, theta=30, rank=4)
    assert np.allclose(rotation_matrix[:, -1], [0, 0, 0, 1])
    assert np.allclose(rotation_matrix[-1, :], [0, 0, 0, 1])
    rotation_matrix = get_rotation_matrix(rotation_axis=1, theta=30, rank=4)
    assert np.allclose(rotation_matrix[:, -1], [0, 0, 0, 1])
    assert np.allclose(rotation_matrix[-1, :], [0, 0, 0, 1])
    rotation_matrix = get_rotation_matrix(rotation_axis=2, theta=30, rank=4)
    assert np.allclose(rotation_matrix[:, -1], [0, 0, 0, 1])
    assert np.allclose(rotation_matrix[-1, :], [0, 0, 0, 1])


def test_get_shift_matrix_error():
    with pytest.raises(ValueError):
        get_shift_matrix((14, 13), rank=4)

    with pytest.raises(ValueError):
        get_shift_matrix((14, 13, 13), rank=3)


def test_get_shift_matrix():
    shift_matrix = get_shift_matrix((30, 10), rank=3)
    assert np.all(shift_matrix == np.array([[1, 0, 30],
                                            [0, 1, 10],
                                            [0, 0, 1]]))

    shift_matrix = get_shift_matrix((30, 20, 10), rank=4)
    assert np.all(shift_matrix == np.array([[1, 0, 0, 30],
                                            [0, 1, 0, 20],
                                            [0, 0, 1, 10],
                                            [0, 0, 0, 1]]))


def test_get_zoom_matrix():
    zoom_matrix = get_zoom_matrix(2, rank=3)
    assert np.all(zoom_matrix == np.array([[2, 0, 0],
                                           [0, 2, 0],
                                           [0, 0, 1]]))

    zoom_matrix = get_zoom_matrix(0.5, rank=4)
    assert np.all(zoom_matrix == np.array([[0.5, 0, 0, 0],
                                           [0, 0.5, 0, 0],
                                           [0, 0, 0.5, 0],
                                           [0, 0, 0, 1]]))


def test_affine_transform_matrix():
    transform_matrix = affine_transform_matrix(
        rank=3, theta=90)

    assert np.allclose(transform_matrix, np.array([[0, -1, 0],
                                                   [1, 0, 0],
                                                   [0, 0, 1]]))

    transform_matrix = affine_transform_matrix(
        rank=3, zoom_factor=2)

    assert np.allclose(transform_matrix, np.array([[0.5, 0, 0],
                                                   [0, 0.5, 0],
                                                   [0, 0, 1]]))

    transform_matrix = affine_transform_matrix(
        rank=3, theta=90, zoom_factor=2, shift=(10, 20))

    assert np.allclose(transform_matrix, np.array([[0, -0.5, 0],
                                                   [0.5, 0, 0],
                                                   [0, 0, 1]]))


def test_apply_affine_transform():
    image = np.zeros((5, 5, 2))
    image[..., 0] = [[0, 0, 1, 0, 0],
                     [0, 1, 0, 1, 0],
                     [1, 0, 0, 0, 1],
                     [0, 1, 0, 1, 0],
                     [0, 0, 1, 0, 0]]
    image[..., 1] = [[1, 1, 1, 1, 1],
                     [0, 0, 1, 0, 0],
                     [1, 1, 1, 1, 1],
                     [0, 0, 1, 0, 0],
                     [0, 0, 1, 0, 0]]
    res = apply_affine_transform(image, theta=90, mode='constant', cval=0)

    expected = np.zeros((5, 5, 2))

    expected[..., 0] = [[0, 0, 1, 0, 0],
                        [0, 1, 0, 1, 0],
                        [1, 0, 0, 0, 1],
                        [0, 1, 0, 1, 0],
                        [0, 0, 1, 0, 0]]
    expected[..., 1] = [[0, 0, 1, 0, 1],
                        [0, 0, 1, 0, 1],
                        [1, 1, 1, 1, 1],
                        [0, 0, 1, 0, 1],
                        [0, 0, 1, 0, 1]]

    assert np.allclose(res, expected)

    image = np.zeros((5, 5, 2))
    image[..., 0] = [[0, 0, 1, 0, 0],
                     [0, 1, 0, 1, 0],
                     [1, 0, 0, 0, 1],
                     [0, 1, 0, 1, 0],
                     [0, 0, 1, 0, 0]]
    image[..., 1] = [[1, 1, 1, 1, 1],
                     [0, 0, 1, 0, 0],
                     [1, 1, 1, 1, 1],
                     [0, 0, 1, 0, 0],
                     [0, 0, 1, 0, 0]]
    res = apply_affine_transform(image, shift=(1, 0), mode='constant', cval=0)

    expected = np.zeros((5, 5, 2))

    expected[..., 0] = [[0, 1, 0, 1, 0],
                        [1, 0, 0, 0, 1],
                        [0, 1, 0, 1, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0]]
    expected[..., 1] = [[0, 0, 1, 0, 0],
                        [1, 1, 1, 1, 1],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0]]

    assert np.allclose(res, expected)


def test_apply_affine_transform_3d():
    image = np.zeros((3, 3, 3, 2))
    # 3d T in the first channel
    image[0][..., 0] = [[0, 0, 0],
                        [0, 1, 0],
                        [0, 0, 0]]
    image[1][..., 0] = [[0, 0, 0],
                        [0, 1, 0],
                        [0, 0, 0]]
    image[2][..., 0] = [[0, 0, 0],
                        [1, 1, 1],
                        [0, 0, 0]]
    # 3d H in the second channel
    image[0][..., 1] = [[1, 0, 1],
                        [0, 0, 0],
                        [0, 0, 0]]
    image[1][..., 1] = [[1, 1, 1],
                        [0, 0, 0],
                        [0, 0, 0]]
    image[2][..., 1] = [[1, 0, 1],
                        [0, 0, 0],
                        [0, 0, 0]]
    res = apply_affine_transform(
        image, theta=90, rotation_axis=0, mode='constant', cval=0)

    expected = np.zeros((3, 3, 3, 2))
    # 3d T in the first channel
    expected[0][..., 0] = [[0, 0, 0],
                           [0, 1, 0],
                           [0, 0, 0]]
    expected[1][..., 0] = [[0, 0, 0],
                           [0, 1, 0],
                           [0, 0, 0]]
    expected[2][..., 0] = [[0, 1, 0],
                           [0, 1, 0],
                           [0, 1, 0]]
    # 3d H in the second channel
    expected[0][..., 1] = [[0, 0, 1],
                           [0, 0, 0],
                           [0, 0, 1]]
    expected[1][..., 1] = [[0, 0, 1],
                           [0, 0, 1],
                           [0, 0, 1]]
    expected[2][..., 1] = [[0, 0, 1],
                           [0, 0, 0],
                           [0, 0, 1]]

    assert np.allclose(res, expected)

    image = np.zeros((3, 3, 3, 2))
    # 3d T in the first channel
    image[0][..., 0] = [[0, 0, 0],
                        [0, 1, 0],
                        [0, 0, 0]]
    image[1][..., 0] = [[0, 0, 0],
                        [0, 1, 0],
                        [0, 0, 0]]
    image[2][..., 0] = [[0, 0, 0],
                        [1, 1, 1],
                        [0, 0, 0]]
    # 3d H in the second channel
    image[0][..., 1] = [[1, 0, 1],
                        [0, 0, 0],
                        [0, 0, 0]]
    image[1][..., 1] = [[1, 1, 1],
                        [0, 0, 0],
                        [0, 0, 0]]
    image[2][..., 1] = [[1, 0, 1],
                        [0, 0, 0],
                        [0, 0, 0]]
    res = apply_affine_transform(
        image, shift=(1, 0, 0), mode='constant', cval=0)

    expected = np.zeros((3, 3, 3, 2))
    # 3d T in the first channel
    # expected[0][..., 0] = [[0, 0, 0],
    #                        [0, 1, 0],
    #                        [0, 0, 0]]
    expected[0][..., 0] = [[0, 0, 0],
                           [0, 1, 0],
                           [0, 0, 0]]
    expected[1][..., 0] = [[0, 0, 0],
                           [1, 1, 1],
                           [0, 0, 0]]
    # 3d H in the second channel
    expected[0][..., 1] = [[1, 1, 1],
                           [0, 0, 0],
                           [0, 0, 0]]
    expected[1][..., 1] = [[1, 0, 1],
                           [0, 0, 0],
                           [0, 0, 0]]

    assert np.allclose(res, expected)

    res = apply_affine_transform(
        image, shift=(0, 1, 0), mode='constant', cval=0)

    expected = np.zeros((3, 3, 3, 2))
    expected[0][..., 0] = [[0, 1, 0],
                           [0, 0, 0],
                           [0, 0, 0], ]
    expected[1][..., 0] = [[0, 1, 0],
                           [0, 0, 0],
                           [0, 0, 0]]
    expected[2][..., 0] = [[1, 1, 1],
                           [0, 0, 0],
                           [0, 0, 0]]

    assert np.allclose(res, expected)

    res = apply_affine_transform(
        image, shift=(0, 0, 1), mode='constant', cval=0)

    expected = np.zeros((3, 3, 3, 2))
    # 3d T in the first channel
    expected[0][..., 0] = [[0, 0, 0],
                           [1, 0, 0],
                           [0, 0, 0]]
    expected[1][..., 0] = [[0, 0, 0],
                           [1, 0, 0],
                           [0, 0, 0]]
    expected[2][..., 0] = [[0, 0, 0],
                           [1, 1, 0],
                           [0, 0, 0]]
    # 3d H in the second channel
    expected[0][..., 1] = [[0, 1, 0],
                           [0, 0, 0],
                           [0, 0, 0]]
    expected[1][..., 1] = [[1, 1, 0],
                           [0, 0, 0],
                           [0, 0, 0]]
    expected[2][..., 1] = [[0, 1, 0],
                           [0, 0, 0],
                           [0, 0, 0]]

    assert np.allclose(res, expected)


def test_flip_2d():
    image = np.zeros((3, 3, 2))
    image[..., 0] = [[1, 1, 0],
                     [1, 1, 0],
                     [0, 0, 0]]

    image[..., 1] = [[1, 1, 1],
                     [1, 1, 0],
                     [1, 0, 0]]

    res = apply_flip(image, 0)

    expected = np.zeros((3, 3, 2))
    expected[..., 0] = [[0, 0, 0],
                        [1, 1, 0],
                        [1, 1, 0]]

    expected[..., 1] = [[1, 0, 0],
                        [1, 1, 0],
                        [1, 1, 1]]

    assert np.all(res == expected)

    res = apply_flip(image, 1)

    expected = np.zeros((3, 3, 2))
    expected[..., 0] = [[0, 1, 1],
                        [0, 1, 1],
                        [0, 0, 0]]

    expected[..., 1] = [[1, 1, 1],
                        [0, 1, 1],
                        [0, 0, 1]]

    assert np.all(res == expected)

    res = apply_flip(image, axis=(0, 1))

    expected = np.zeros((3, 3, 2))
    expected[..., 0] = [[0, 0, 0],
                        [0, 1, 1],
                        [0, 1, 1]]

    expected[..., 1] = [[0, 0, 1],
                        [0, 1, 1],
                        [1, 1, 1]]

    assert np.all(res == expected)


def test_flip_3d():
    image = np.zeros((3, 3, 3, 1))

    image[0][..., 0] = [[1, 0, 0],
                        [1, 0, 0],
                        [1, 0, 0]]
    image[1][..., 0] = [[1, 0, 0],
                        [1, 0, 0],
                        [0, 0, 0]]
    image[2][..., 0] = [[1, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]]

    res = apply_flip(image, axis=0)

    expected = np.zeros((3, 3, 3, 1))

    expected[2][..., 0] = [[1, 0, 0],
                           [1, 0, 0],
                           [1, 0, 0]]
    expected[1][..., 0] = [[1, 0, 0],
                           [1, 0, 0],
                           [0, 0, 0]]
    expected[0][..., 0] = [[1, 0, 0],
                           [0, 0, 0],
                           [0, 0, 0]]

    assert np.all(res == expected)

    res = apply_flip(image, axis=1)

    expected = np.zeros((3, 3, 3, 1))

    expected[0][..., 0] = [[1, 0, 0],
                           [1, 0, 0],
                           [1, 0, 0]]
    expected[1][..., 0] = [[0, 0, 0],
                           [1, 0, 0],
                           [1, 0, 0]]
    expected[2][..., 0] = [[0, 0, 0],
                           [0, 0, 0],
                           [1, 0, 0]]

    assert np.all(res == expected)

    res = apply_flip(image, axis=(0, 1))

    expected = np.zeros((3, 3, 3, 1))

    expected[2][..., 0] = [[1, 0, 0],
                           [1, 0, 0],
                           [1, 0, 0]]
    expected[1][..., 0] = [[0, 0, 0],
                           [1, 0, 0],
                           [1, 0, 0]]
    expected[0][..., 0] = [[0, 0, 0],
                           [0, 0, 0],
                           [1, 0, 0]]

    assert np.all(res == expected)

    res = apply_flip(image, axis=(0, 1, 2))

    expected = np.zeros((3, 3, 3, 1))

    expected[2][..., 0] = [[0, 0, 1],
                           [0, 0, 1],
                           [0, 0, 1]]
    expected[1][..., 0] = [[0, 0, 0],
                           [0, 0, 1],
                           [0, 0, 1]]
    expected[0][..., 0] = [[0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 1]]

    assert np.all(res == expected)

    res = apply_flip(image, axis=2)

    expected = np.zeros((3, 3, 3, 1))

    expected[0][..., 0] = [[0, 0, 1],
                           [0, 0, 1],
                           [0, 0, 1]]
    expected[1][..., 0] = [[0, 0, 1],
                           [0, 0, 1],
                           [0, 0, 0]]
    expected[2][..., 0] = [[0, 0, 1],
                           [0, 0, 0],
                           [0, 0, 0]]

    assert np.all(res == expected)

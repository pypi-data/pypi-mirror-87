import pytest
import numpy as np
from itertools import product
from deoxys_image import get_patch_indice, get_patch_indice_all, check_drop
from deoxys_image import get_stratified_index, get_patches


def test_get_patch_indice_error():
    with pytest.raises(ValueError):
        get_patch_indice((2, 3, 4), (13, 13), 0)


def test_get_patch_indice():
    indice = get_patch_indice((20, 20, 20), (10, 10, 10), 0)

    expected = [(0, 0, 0), (0, 0, 10),
                (0, 10, 0), (0, 10, 10),
                (10, 0, 0), (10, 0, 10),
                (10, 10, 0), (10, 10, 10)]

    assert np.all(indice == expected)

    indice = get_patch_indice((20, 20, 20), (10, 10, 10), 0.5)

    expected = [(0, 0, 0), (0, 0, 5), (0, 0, 10),
                (0, 5, 0), (0, 5, 5), (0, 5, 10),
                (0, 10, 0), (0, 10, 5), (0, 10, 10),
                (5, 0, 0), (5, 0, 5), (5, 0, 10),
                (5, 5, 0), (5, 5, 5), (5, 5, 10),
                (5, 10, 0), (5, 10, 5), (5, 10, 10),
                (10, 0, 0), (10, 0, 5), (10, 0, 10),
                (10, 5, 0), (10, 5, 5), (10, 5, 10),
                (10, 10, 0), (10, 10, 5), (10, 10, 10)]

    assert np.all(indice == expected)

    indice = get_patch_indice((20, 20, 19), (10, 10, 10), 0.5)

    expected = [(0, 0, 0), (0, 0, 5), (0, 0, 9),
                (0, 5, 0), (0, 5, 5), (0, 5, 9),
                (0, 10, 0), (0, 10, 5), (0, 10, 9),
                (5, 0, 0), (5, 0, 5), (5, 0, 9),
                (5, 5, 0), (5, 5, 5), (5, 5, 9),
                (5, 10, 0), (5, 10, 5), (5, 10, 9),
                (10, 0, 0), (10, 0, 5), (10, 0, 9),
                (10, 5, 0), (10, 5, 5), (10, 5, 9),
                (10, 10, 0), (10, 10, 5), (10, 10, 9)]

    assert np.all(indice == expected)


def test_get_patch_indice_all():
    images = [np.zeros((20, 20, 20, 3)), np.zeros((20, 20, 19, 3))]

    indice = get_patch_indice_all(images, (10, 10, 10), 0.5)

    expected = []

    expected_indice_1 = [
        (0, 0, 0), (0, 0, 5), (0, 0, 10),
        (0, 5, 0), (0, 5, 5), (0, 5, 10),
        (0, 10, 0), (0, 10, 5), (0, 10, 10),
        (5, 0, 0), (5, 0, 5), (5, 0, 10),
        (5, 5, 0), (5, 5, 5), (5, 5, 10),
        (5, 10, 0), (5, 10, 5), (5, 10, 10),
        (10, 0, 0), (10, 0, 5), (10, 0, 10),
        (10, 5, 0), (10, 5, 5), (10, 5, 10),
        (10, 10, 0), (10, 10, 5), (10, 10, 10)
    ]

    expected_indice_2 = [
        (0, 0, 0), (0, 0, 5), (0, 0, 9),
        (0, 5, 0), (0, 5, 5), (0, 5, 9),
        (0, 10, 0), (0, 10, 5), (0, 10, 9),
        (5, 0, 0), (5, 0, 5), (5, 0, 9),
        (5, 5, 0), (5, 5, 5), (5, 5, 9),
        (5, 10, 0), (5, 10, 5), (5, 10, 9),
        (10, 0, 0), (10, 0, 5), (10, 0, 9),
        (10, 5, 0), (10, 5, 5), (10, 5, 9),
        (10, 10, 0), (10, 10, 5), (10, 10, 9)]

    for index in expected_indice_1:
        expected.append((0, index))

    for index in expected_indice_2:
        expected.append((1, index))

    for index, expected_index in zip(indice, expected):
        assert np.all(index == expected_index)


def test_check_drop_3d():
    image = np.zeros((10, 10, 10, 2))
    image[5:, :, :, 0] = 1
    image[5:, :5, :, 1] = 1

    images = np.array([image for _ in range(2)])

    indice = get_patch_indice((10, 10, 10), (5, 5, 5), 0)
    indice = list(product([0, 1], indice))

    res = check_drop(images, indice, (5, 5, 5), 0.4, None)
    expected = [
        False, False, False, False, True, True, True, True
    ] * 2

    assert np.all(res == expected)

    res = check_drop(images, indice, (5, 5, 5), 0.9, None)
    expected = [
        False, False, False, False, True, True, False, False
    ] * 2

    assert np.all(res == expected)

    res = check_drop(images, indice, (5, 5, 5), 0.9, 0)
    expected = [
        False, False, False, False, True, True, True, True
    ] * 2

    assert np.all(res == expected)


# def test_check_drop_3d_different_images():
#     image_1 = np.zeros((10, 10, 10, 2))
#     image_1[5:, :, :, 0] = 1
#     image_1[5:, :5, :, 1] = 1

#     image_2 = np.zeros((9, 10, 10, 2))
#     image_2[4:, :, :, 0] = 1
#     image_2[4:, :5, :, 1] = 1

#     images = np.array([image_1, image_2], dtype=object)

#     indice = get_patch_indice_all(images, (5, 5, 5), 0)

#     res = check_drop(images, indice, (5, 5, 5), 0.4, None)
#     print(res)
#     expected = [
#         False, False, False, False, True, True, True, True
#     ] * 2

#     assert np.all(res == expected)

#     res = check_drop(images, indice, (5, 5, 5), 0.9, None)
#     expected = [
#         False, False, False, False, True, True, False, False
#     ] * 2

#     assert np.all(res == expected)

#     res = check_drop(images, indice, (5, 5, 5), 0.9, 0)
#     expected = [
#         False, False, False, False, True, True, True, True
#     ] * 2

#     assert np.all(res == expected)


def test_check_drop_2d():
    image = np.zeros((10, 10, 2))
    image[5:, :, 0] = 1
    image[5:, :5, 1] = 1

    images = np.array([image for _ in range(2)])

    indice = get_patch_indice((10, 10), (5, 5), 0)
    indice = list(product([0, 1], indice))

    res = check_drop(images, indice, (5, 5), 0.4, None)

    expected = [
        False, False, True, True
    ] * 2

    assert np.all(res == expected)

    res = check_drop(images, indice, (5, 5), 0.9, None)
    expected = [
        False, False, True, False
    ] * 2

    assert np.all(res == expected)

    res = check_drop(images, indice, (5, 5), 0.9, 0)
    expected = [
        False, False, True, True
    ] * 2

    assert np.all(res == expected)


def test_stratified_index():
    values = np.array([0, 0, 0, 0, 0, 1, 1, 1])
    index = get_stratified_index(values, 4)

    assert len(index) == len(values)
    assert np.all(np.unique(index) == np.arange(len(values)))

    assert sum(values[index[:4]]) == 2
    assert sum(values[index[4:]]) == 1

    index = get_stratified_index(values, 3)

    assert len(index) == len(values)
    assert np.all(np.unique(index) == np.arange(len(values)))

    assert sum(values[index[:3]]) == 1
    assert sum(values[index[3:6]]) == 1
    assert sum(values[index[6:]]) == 1

    index = get_stratified_index(values, 2)

    assert len(index) == len(values)
    assert np.all(np.unique(index) == np.arange(len(values)))

    assert sum(values[index[:2]]) == 2
    assert sum(values[index[2:4]]) == 0
    assert sum(values[index[4:6]]) == 1
    assert sum(values[index[6:]]) == 0


def test_get_patches_3d():
    image = np.zeros((10, 10, 10, 2))
    image[5:, :, :, 0] = 1
    image[5:, :5, :, 1] = 1

    images = np.array([image for _ in range(2)])

    indice = get_patch_indice((10, 10, 10), (5, 5, 5), 0)

    # Only patches, in order
    patches = get_patches(images,
                          patch_indice=indice, patch_size=(5, 5, 5),
                          stratified=False, drop_fraction=0,
                          check_drop_channel=None)

    empty_patches = np.zeros((5, 5, 5, 2))
    half_patches = np.zeros((5, 5, 5, 2))
    half_patches[..., 0] = 1
    full_patches = np.ones((5, 5, 5, 2))

    expected = np.array([
        empty_patches, empty_patches, empty_patches, empty_patches,
        full_patches, full_patches, half_patches, half_patches
    ] * 2)

    assert len(patches) == 16
    assert np.all(patches == expected)

    # Only patches, in order, drop half
    patches = get_patches(images,
                          patch_indice=indice, patch_size=(5, 5, 5),
                          stratified=False, drop_fraction=0.4,
                          check_drop_channel=None)

    expected = np.array([
        full_patches, full_patches, half_patches, half_patches
    ] * 2)

    assert len(patches) == 8
    assert np.all(patches == expected)

    # Only patches, in order, only keep full
    patches = get_patches(images,
                          patch_indice=indice, patch_size=(5, 5, 5),
                          stratified=False, drop_fraction=0.9,
                          check_drop_channel=None)

    expected = np.array([
        full_patches, full_patches
    ] * 2)

    assert len(patches) == 4
    assert np.all(patches == expected)

    # Only patches, in order, drop half based on one channel
    patches = get_patches(images,
                          patch_indice=indice, patch_size=(5, 5, 5),
                          stratified=False, drop_fraction=0.4,
                          check_drop_channel=0)

    expected = np.array([
        full_patches, full_patches, half_patches, half_patches
    ] * 2)

    assert len(patches) == 8
    assert np.all(patches == expected)

    # patches, targets, stratified, without batch_size
    target = np.zeros((10, 10, 10, 1))
    target[5:, :5, :, 0] = 1

    targets = np.array([target for _ in range(2)])

    patches, labels = get_patches(images, target=targets,
                                  patch_indice=indice, patch_size=(5, 5, 5),
                                  stratified=True, drop_fraction=0.4,
                                  check_drop_channel=0)

    assert len(patches) == 8
    full_patches_num = 0
    half_patches_num = 0

    for patch, label in zip(patches, labels):
        if np.all(full_patches == patch):
            assert np.all(label == np.ones((5, 5, 5, 1)))
            full_patches_num += 1
        elif np.all(half_patches == patch):
            assert np.all(label == np.zeros((5, 5, 5, 1)))
            half_patches_num += 1

    assert full_patches_num == 4 and half_patches_num == 4

    # patches, targets, stratified based on target
    patches, labels = get_patches(images, target=targets,
                                  patch_indice=indice, patch_size=(5, 5, 5),
                                  stratified=True, drop_fraction=0.4,
                                  check_drop_channel=0, batch_size=4)

    assert len(patches) == 8

    full_patches_num = 0
    half_patches_num = 0
    for patch, label in zip(patches[:4], labels[:4]):
        if np.all(full_patches == patch):
            assert np.all(label == np.ones((5, 5, 5, 1)))
            full_patches_num += 1
        elif np.all(half_patches == patch):
            assert np.all(label == np.zeros((5, 5, 5, 1)))
            half_patches_num += 1

    assert full_patches_num == 2 and half_patches_num == 2

    full_patches_num = 0
    half_patches_num = 0
    for patch, label in zip(patches[4:], labels[4:]):
        if np.all(full_patches == patch):
            assert np.all(label == np.ones((5, 5, 5, 1)))
            full_patches_num += 1
        elif np.all(half_patches == patch):
            assert np.all(label == np.zeros((5, 5, 5, 1)))
            half_patches_num += 1

    assert full_patches_num == 2 and half_patches_num == 2


def test_get_patches_2d():
    image = np.zeros((10, 10, 2))
    image[5:, :, 0] = 1
    image[5:, :5, 1] = 1
    images = np.array([image for _ in range(2)])

    target = np.zeros((10, 10, 1))
    target[5:, :5, 0] = 1
    targets = np.array([target for _ in range(2)])

    indice = get_patch_indice((10, 10), (5, 5), 0)

    patches, labels = get_patches(images, target=targets,
                                  patch_indice=indice, patch_size=(5, 5),
                                  stratified=True, drop_fraction=0.4,
                                  check_drop_channel=0, batch_size=2)

    half_patches = np.zeros((5, 5, 2))
    half_patches[..., 0] = 1
    full_patches = np.ones((5, 5, 2))

    assert len(patches) == 4

    full_patches_num = 0
    half_patches_num = 0
    for patch, label in zip(patches[:2], labels[:2]):
        if np.all(full_patches == patch):
            assert np.all(label == np.ones((5, 5, 1)))
            full_patches_num += 1
        elif np.all(half_patches == patch):
            assert np.all(label == np.zeros((5, 5, 1)))
            half_patches_num += 1

    assert full_patches_num == 1 and half_patches_num == 1

    full_patches_num = 0
    half_patches_num = 0
    for patch, label in zip(patches[2:], labels[2:]):
        if np.all(full_patches == patch):
            assert np.all(label == np.ones((5, 5, 1)))
            full_patches_num += 1
        elif np.all(half_patches == patch):
            assert np.all(label == np.zeros((5, 5, 1)))
            half_patches_num += 1

    assert full_patches_num == 1 and half_patches_num == 1

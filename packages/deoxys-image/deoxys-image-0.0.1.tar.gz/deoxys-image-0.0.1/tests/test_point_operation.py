import pytest
import numpy as np
from deoxys_image import normalize
from deoxys_image import apply_random_brightness, apply_random_contrast
from deoxys_image import apply_random_gaussian_noise


def test_normalize_all_channel():
    base_data = np.array([np.arange(30) for _ in range(5)])

    normalized_image = np.zeros(30)
    normalized_image[20:] = 1
    normalized_image[10:20] = np.arange(10) / 10

    normalize_data = np.array([normalized_image for _ in range(5)])

    images = np.zeros((5, 5, 6, 2))
    images[..., 0] = base_data.reshape(5, 5, 6)
    images[..., 1] = base_data.reshape(5, 5, 6)

    expected = np.zeros((5, 5, 6, 2))
    expected[..., 0] = normalize_data.reshape(5, 5, 6)
    expected[..., 1] = normalize_data.reshape(5, 5, 6)

    res = normalize(images, 10, 20)

    assert np.allclose(res, expected)

    res = normalize(images)
    assert np.allclose(res, images/29)


def test_normalize_per_channel():
    base_data = np.array([np.arange(30) for _ in range(5)])

    normalized_image = np.zeros(30)
    normalized_image[20:] = 1
    normalized_image[10:20] = np.arange(10) / 10

    normalize_data = np.array([normalized_image for _ in range(5)])

    images = np.zeros((5, 5, 6, 3))
    images[..., 0] = base_data.reshape(5, 5, 6)
    images[..., 1] = base_data.reshape(5, 5, 6)
    images[..., 2] = base_data.reshape(5, 5, 6)

    expected = np.zeros((5, 5, 6, 3))
    expected[..., 0] = normalize_data.reshape(5, 5, 6)
    expected[..., 1] = normalize_data.reshape(5, 5, 6)
    expected[..., 2] = base_data.reshape(5, 5, 6) / 29

    res = normalize(images, [10, 10], [20, 20])

    assert np.allclose(res, expected)

    res = normalize(images, [10, 20], [20, 30])

    normalized_image = np.zeros(30)
    normalized_image[20:] = np.arange(10) / 10
    normalize_data = np.array([normalized_image for _ in range(5)])
    expected[..., 1] = normalize_data.reshape(5, 5, 6)

    assert np.allclose(res, expected)


def test_brightness_constant_all_channel():
    base_data = np.array([np.arange(1, 31) / 30 for _ in range(5)])

    images = np.zeros((5, 5, 6, 2))
    images[..., 0] = base_data.reshape(5, 5, 6)
    images[..., 1] = base_data.reshape(5, 5, 6)

    res = apply_random_brightness(images, low=1.5, high=1.5)

    assert np.allclose(res, (images + 0.5).clip(1/30, 1))

    res = apply_random_brightness(images, low=0.7, high=0.7)

    assert np.allclose(res, (images - 0.3).clip(1/30, 1))


def test_brightness_random_all_channel():
    base_data = np.array([np.arange(1, 31) / 30 for _ in range(30)])

    images = np.zeros((30, 5, 6, 2))
    images[..., 0] = base_data.reshape(30, 5, 6)
    images[..., 1] = base_data.reshape(30, 5, 6)

    res = apply_random_brightness(images, low=0.8, high=1.2)

    for i, img in enumerate(res):
        diff = img[2, 2, 0] - images[i, 2, 2, 0]
        assert -0.2 <= diff <= 0.2
        assert np.allclose(img, (images[i] + diff).clip(1/30, 1))


def test_brightness_random_per_channel():
    base_data = np.array([np.arange(1, 31) / 30 for _ in range(30)])

    images = np.zeros((30, 5, 6, 2))
    images[..., 0] = base_data.reshape(30, 5, 6)
    images[..., 1] = base_data.reshape(30, 5, 6)

    res = apply_random_brightness(images, low=0.8, high=1.2, channel=0)

    for i, img in enumerate(res):
        diff = img[2, 2] - images[i, 2, 2]
        assert -0.2 <= diff[0] <= 0.2
        assert np.allclose(img, (images[i] + diff).clip(1/30, 1))

    images = np.zeros((30, 5, 6, 3))
    images[..., 0] = base_data.reshape(30, 5, 6)
    images[..., 1] = base_data.reshape(30, 5, 6)
    images[..., 2] = base_data.reshape(30, 5, 6)

    res = apply_random_brightness(images, low=0.8, high=1.2, channel=[0, 1])

    for i, img in enumerate(res):
        diff = img[2, 2] - images[i, 2, 2]
        assert -0.2 <= diff[0] <= 0.2
        assert -0.2 <= diff[1] <= 0.2
        assert np.allclose(img, (images[i] + diff).clip(1/30, 1))


def test_contrast_constant_all_channel():
    base_data = np.array([np.arange(1, 31) / 30 for _ in range(5)])

    images = np.zeros((5, 5, 6, 2))
    images[..., 0] = base_data.reshape(5, 5, 6)
    images[..., 1] = base_data.reshape(5, 5, 6)

    res = apply_random_contrast(images, low=1.5, high=1.5)

    mn = images.mean()

    assert np.allclose(res, ((images - mn) * 1.5 + mn).clip(1/30, 1))

    res = apply_random_contrast(images, low=0.7, high=0.7)

    assert np.allclose(res, ((images - mn) * 0.7 + mn).clip(1/30, 1))


def test_contrast_random_all_channel():
    base_data = np.array([np.arange(1, 31) / 30 for _ in range(30)])

    images = np.zeros((30, 5, 6, 2))
    images[..., 0] = base_data.reshape(30, 5, 6)
    images[..., 1] = base_data.reshape(30, 5, 6)

    res = apply_random_contrast(images, low=0.8, high=1.2)
    mn = images.mean()

    for i, img in enumerate(res):
        diff = (img[2, 2, 0] - mn) / (images[i, 2, 2, 0] - mn)
        assert 0.8 <= diff <= 1.2
        assert np.allclose(img, ((images[i] - mn) * diff + mn).clip(1/30, 1))


def test_contrast_random_per_channel():
    base_data = np.array([np.arange(1, 31) / 30 for _ in range(30)])

    images = np.zeros((30, 5, 6, 2))
    images[..., 0] = base_data.reshape(30, 5, 6)
    images[..., 1] = base_data.reshape(30, 5, 6)

    res = apply_random_contrast(images, low=0.8, high=1.2, channel=0)
    mn = images.mean()

    for i, img in enumerate(res):
        diff = (img[2, 2] - mn) / (images[i, 2, 2] - mn)

        assert 0.8 <= diff[0] <= 1.2

        assert np.allclose(img, ((images[i] - mn) * diff + mn).clip(1/30, 1))

    images = np.zeros((30, 5, 6, 3))
    images[..., 0] = base_data.reshape(30, 5, 6)
    images[..., 1] = base_data.reshape(30, 5, 6)
    images[..., 2] = base_data.reshape(30, 5, 6)

    res = apply_random_contrast(
        images, low=0.8, high=1.2, channel=[0, 1])

    for i, img in enumerate(res):
        diff = (img[2, 2] - mn) / (images[i, 2, 2] - mn)

        assert 0.8 <= diff[0] <= 1.2
        assert 0.8 <= diff[1] <= 1.2
        assert np.allclose(img, ((images[i] - mn) * diff + mn).clip(1/30, 1))


def test_gaussian_noise():
    images = np.random.normal(0, 1, size=(30, 5, 5, 3))

    res = apply_random_gaussian_noise(images, (0.1, 0.3))
    assert not np.allclose(res, images)

    res = apply_random_gaussian_noise(images, 0.5, channel=0)
    assert not np.allclose(res[..., 0], images[..., 0])
    assert np.allclose(res[..., 1:], images[..., 1:])

    res = apply_random_gaussian_noise(images, 0.5, channel=[0, 1])
    assert not np.allclose(res[..., 0], images[..., 0])
    assert not np.allclose(res[..., 1], images[..., 1])
    assert np.allclose(res[..., 2], images[..., 2])

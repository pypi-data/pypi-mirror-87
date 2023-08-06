import pytest
import numpy as np
from deoxys_image import apply_random_gaussian_blur


def test_gaussian_blue():
    images = np.random.normal(0, 1, size=(30, 5, 5, 3))

    res = apply_random_gaussian_blur(images, low=0.6, high=1.3)
    assert not np.allclose(res, images)

    res = apply_random_gaussian_blur(images, low=0.6, high=1.3, channel=0)
    assert not np.allclose(res[..., 0], images[..., 0])
    assert np.allclose(res[..., 1:], images[..., 1:])

    res = apply_random_gaussian_blur(images, low=0.6, high=1.3, channel=[0, 1])
    assert not np.allclose(res[..., 0], images[..., 0])
    assert not np.allclose(res[..., 1], images[..., 1])
    assert np.allclose(res[..., 2], images[..., 2])

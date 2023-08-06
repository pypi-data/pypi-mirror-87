import pytest
import numpy as np

from deoxys_image import ImageAugmentation, get_random_affine_params


def test_get_random_affine_params():
    for _ in range(100):
        theta, zoom, shift = get_random_affine_params(
            (-4, 4), 0.2, (0.8, 1.2), 0.2, (np.zeros(2), np.zeros(2)), 0.1)

        assert -4 <= theta < 4
        assert 0.8 <= zoom < 1.2
        assert np.all(shift == 0)
        assert len(shift) == 2

    no_changes = 0
    for _ in range(100):
        theta, zoom, shift = get_random_affine_params(
            (-4, 4), 0.2,
            (0.8, 1.2), 0.2,
            (np.array([0, -4]), np.array([0, 4])), 0.1)

        assert -4 <= theta < 4
        assert 0.8 <= zoom < 1.2
        assert shift[0] == 0
        assert -4 <= shift[1] < 4
        assert len(shift) == 2

        if theta == 0 and zoom == 1 and np.all(shift == 0):
            no_changes += 1

    assert no_changes > 50


def test_augmentation_single():
    images = np.random.random((10, 3, 3, 2))
    targets = np.random.random((10, 3, 3, 1))

    aug = ImageAugmentation(rank=3, rotation_range=20, rotation_axis=2)
    aug.transform(images)
    aug.transform(images, targets)

    aug = ImageAugmentation(rank=3, zoom_range=1.5)
    aug.transform(images)

    aug = ImageAugmentation(rank=3, zoom_range=0.5)
    aug.transform(images, targets)

    aug = ImageAugmentation(rank=3, zoom_range=(0.8, 1.2))
    aug.transform(images)

    aug = ImageAugmentation(rank=3, shift_range=(0, 20))
    aug.transform(images)

    aug = ImageAugmentation(rank=3, shift_range=30)
    aug.transform(images, targets)

    aug = ImageAugmentation(rank=3, flip_axis=0)
    aug.transform(images, targets)

    aug = ImageAugmentation(rank=3, flip_axis=[0, 1])
    aug.transform(images)

    aug = ImageAugmentation(rank=3, brightness_range=0.8)
    aug.transform(images)

    aug = ImageAugmentation(rank=3, brightness_range=1.2)
    aug.transform(images)

    aug = ImageAugmentation(rank=3, brightness_range=(0.8, 1.2))
    aug.transform(images)

    aug = ImageAugmentation(rank=4, contrast_range=0.8)
    aug.transform(images)

    aug = ImageAugmentation(rank=4, contrast_range=1.2)
    aug.transform(images)

    aug = ImageAugmentation(rank=4, contrast_range=(0.8, 1.2))
    aug.transform(images)

    aug = ImageAugmentation(rank=4, noise_variance=0.8)
    aug.transform(images)

    aug = ImageAugmentation(rank=4, noise_variance=1.2)
    aug.transform(images)

    aug = ImageAugmentation(rank=4, noise_variance=(0.8, 1.2))
    aug.transform(images)

    aug = ImageAugmentation(rank=4, blur_range=0.8)
    aug.transform(images)

    aug = ImageAugmentation(rank=4, blur_range=1.2)
    aug.transform(images)

    aug = ImageAugmentation(rank=4, blur_range=(0.8, 1.2))
    aug.transform(images)

    with pytest.raises(ValueError):
        aug = ImageAugmentation(rank=3, shift_range=(0, -20))

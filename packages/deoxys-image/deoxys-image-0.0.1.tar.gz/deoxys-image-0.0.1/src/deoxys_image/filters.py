from scipy.ndimage import gaussian_filter
import numpy as np


def gaussian_blur(image, sigma=0.4, channel=None):
    image = np.array(image)

    if channel is None:
        channel = [i for i in range(image.shape[-1])]

    if '__iter__' not in dir(channel):
        channel = [channel]
    for c in channel:
        image[..., c] = gaussian_filter(
            image[..., c], sigma=sigma, order=0)
    return image


def apply_random_gaussian_blur(images, low=0.5, high=1.5, channel=None):
    images = np.array(images)
    sigma = np.random.sample(images.shape[0])*(high - low) + low

    for i in range(images.shape[0]):
        images[i] = gaussian_blur(
            images[i], sigma=sigma[i], channel=channel)

    return images

import numpy as np


def change_brightness(image, factor, channel=None):
    """
    Change brightness of an images by adding a constant to all pixels
    in the image so that `max(new_image) = factor * max(image)`

    Parameters
    ----------
    image : np.array
        the image
    factor : float
        change factor for brightness. Factor > 1 means the image will
        get brighter
    channel : int or list, optional
        channel or channels to be adjusted, by default None,
        which means all channels will be adjusted

    Returns
    -------
    np.array
        image with changes in brightness
    """
    image = np.array(image)

    if channel is None:
        imin = image.min()
        imax = image.max()

        change_const = imax * (factor - 1)
        return (image + change_const).clip(imin, imax)
    else:
        if '__iter__' not in dir(channel):
            channel = [channel]

        for c in channel:
            imin = image[..., c].min()
            imax = image[..., c].max()

            change_const = imax * (factor - 1)
            image[..., c] = (image[..., c] + change_const).clip(imin, imax)

        return image


def change_contrast(image, factor, channel=None):
    """
    Change contrast of an images by a factor

    Parameters
    ----------
    image : np.array
        the image
    factor : float
        change factor for contrast. Factor > 1 increases the contrast
    channel : int or list, optional
        channel or channels to be adjusted, by default None,
        which means all channels will be adjusted

    Returns
    -------
    np.array
        image with changes in contrast
    """
    image = np.array(image)

    if channel is None:
        imin = image.min()
        imax = image.max()
        imean = image.mean()

        return ((image - imean) * factor + imean).clip(imin, imax)
    else:
        if '__iter__' not in dir(channel):
            channel = [channel]

        for c in channel:
            imin = image[..., c].min()
            imax = image[..., c].max()
            imean = image[..., c].mean()

            image[..., c] = ((image[..., c] - imean) *
                             factor + imean).clip(imin, imax)

        return image


def apply_random_contrast(images, low=0.6, high=1.4, channel=None):
    images = np.array(images)

    change_factor = np.random.sample(images.shape[0])*(high - low) + low

    for i in range(images.shape[0]):
        images[i] = change_contrast(
            images[i], factor=change_factor[i], channel=channel)

    return images


def apply_random_brightness(images, low=0.7, high=1.3, channel=None):
    images = np.array(images)
    change_factor = np.random.sample(images.shape[0])*(high - low) + low

    for i in range(images.shape[0]):
        images[i] = change_brightness(
            images[i], factor=change_factor[i], channel=channel)

    return images


def gaussian_noise(image, noise_var=0.1, channel=None):
    """
    Apply gaussian noise of variance `noise_var` to a single image

    Parameters
    ----------
    image : np.array
        the image
    noise_var : float, optional
        the variance of the noise value, by default 0.1
    channel : int or list, optional
        channel or channels to be added with random noise, by default None,
        which means all channels are added with random noise
    Returns
    -------
    np.array
        images with noise
    """
    image = np.array(image)

    if channel is None:
        return image + np.random.normal(0, noise_var, size=image.shape)
    else:
        if '__iter__' in dir(channel):
            shape = list(image.shape[:-1]) + [len(channel)]
        else:
            shape = list(image.shape[:-1])

        image[..., channel] = image[..., channel] + \
            np.random.normal(0, noise_var, size=shape)

        return image


def apply_gaussian_noise(images, noise_var=0.1,
                         channel=None):  # pragma: no cover
    """
    Apply gaussian noise of variance `noise_var`

    Parameters
    ----------
    images : np.array
        images
    noise_var : float, optional
        the variance of the noise value
    channel: int or list, optional
        channel or channels to be added with random noise, by default None,
        which means all channels are added with random noise

    Returns
    -------
    np.array
        images with noise
    """
    images = np.array(images)

    if channel is None:
        return images + np.random.normal(0, noise_var, size=images.shape)
    else:
        if '__iter__' not in dir(channel):
            shape = list(images.shape[:-1]) + [len(channel)]
        else:
            shape = list(images.shape[:-1])

        images[..., channel] = images[..., channel] + \
            np.random.normal(0, noise_var, size=shape)

        return images


def apply_random_gaussian_noise(images, variance=None, channel=None):
    """
    Apply gaussian noise with random noise variance in the range of `variance`

    Parameters
    ----------
    images : np.array
        images
    variance : tuple or float, optional
        range of the noise variance, by default (0, 0.1)
    channel: int or list, optional
        channel or channels to be added with random noise, by default None,
        which means all channels are added with random noise
    """
    images = np.array(images)

    if variance is None:
        variance = (0, 0.1)

    if '__iter__' not in dir(variance):
        variance = (0, variance)

    variances = np.random.sample(
        images.shape[0])*(variance[1] - variance[0]) + variance[0]
    # if channel is None:
    #     for i in range(images.shape[0]):
    #         images[i] = images[i] + \
    #             np.random.normal(0.0, variances[i], size=images.shape[1:])
    # else:
    #     if '__iter__' not in dir(channel):
    #         shape = list(images.shape[1:-1]) + [len(channel)]
    #     else:
    #         shape = list(images.shape[1:-1])

    #     for i in range(images.shape[0]):
    #         images[i][..., channel] = images[i][..., channel] + \
    #             np.random.normal(0.0, variances[i], size=shape)

    # return images

    for i in range(images.shape[0]):
        images[i] = gaussian_noise(images[i], variances[i], channel=channel)

    return images


def normalize(images, vmin=None, vmax=None):
    images = np.array(images)
    n_channel = images.shape[-1]

    if vmin is None:
        vmin = np.array([images[..., i].min() for i in range(n_channel)])
    if vmax is None:
        vmax = np.array([images[..., i].max() for i in range(n_channel)])

    if '__iter__' in dir(vmin):
        vmin = np.array(vmin)
        if len(vmin) < n_channel:
            template = np.array([images[..., i].min()
                                 for i in range(n_channel)])
            template[:len(vmin)] = vmin
            vmin = template

    if '__iter__' in dir(vmax):
        vmax = np.array(vmax)

        if len(vmax) < n_channel:
            template = np.array([images[..., i].max()
                                 for i in range(n_channel)])
            template[:len(vmax)] = vmax
            vmax = template

    transformed_images = (images - vmin) / (vmax - vmin)
    transformed_images = transformed_images.clip(0, 1)

    return transformed_images

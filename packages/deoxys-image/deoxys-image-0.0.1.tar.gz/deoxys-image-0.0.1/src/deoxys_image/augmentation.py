import numpy as np

from .point_operation import gaussian_noise, change_brightness, change_contrast
from .filters import gaussian_blur
from .affine_transform import apply_affine_transform, apply_flip


class ImageAugmentation():
    r"""
        Apply transformation in 2d and 3d image for augmentation

        Parameters
        ----------
        rank : int
            rank of a single image (2d: 3, 3d: 4)
        rotation_range : int, optional
            range of the angle rotation, in degree, by default 0 (no rotation)
        rotation_axis : int, optional
            the axis of one image to apply rotation,
            by default 0
        rotation_chance : float, optional
            probability to apply rotation transformation to an image,
            by default 0.2
        zoom_range : float, list, tuple optional
            the range of zooming, zooming in when the number is less than 1,
            and zoom out when the number if larger than 1.
            If a `float`, then it is the range between that number and 1,
            by default 1 (no zooming)
        zoom_chance : float, optional
            probability to apply zoom transformation to an image,
            by default 0.2
        shift_range : tuple or list, optional
            the range of translation in each axis, by default None (no shifts)
        shift_chance : float, optional
            probability to apply translation transformation to an image,
            by default 0.1
        flip_axis : int, tuple, list, optional
            flip by one or more axis (in the single image),
            by default None (no flipping)
        brightness_range : int, tuple, list, optional
            range of the brightness portion,
            based on the max intensity value of each channel.
            For example, when the max intensity value of one channel is 1.0,
            and the brightness is chaned by 1.2, then every pixel in that
            channel will increase the intensity value by 0.2.

            .. math:: 0.2 = 1.0 \cdot (1.2 - 1)

            By default 1 (no changes in brightness)
        brightness_channel : int, tuple, list, optional
            the channel(s) to apply changes in brightness,
            by default None (apply to all channels)
        brightness_chance : float, optional
            probability to apply brightness change transform to an image,
            by default 0.1
        contrast_range : int, tuple, list, optional
            range of the contrast portion,
            (the history range is scaled up or down).
            By default 1 (no changes in contrast)
        contrast_channel : int, tuple, list, optional
            the channel(s) to apply changes in contrast,
            by default None (apply to all channels)
        contrast_chance : float, optional
            probability to apply contrast change transform to an image,
            by default 0.1
        noise_variance : int, tuple, list, optional
            range of the noise variance
            when adding Gaussian noise to the image,
            by default 0 (no adding noise)
        noise_channel : int, tuple, list, optional
            the channel(s) to apply Gaussian noise,
            by default None (apply to all channels)
        noise_chance : float, optional
            probability to apply gaussian noise to an image,
            by default 0.1
        blur_range : int, tuple, list, optional
            range of the blur sigma
            when applying the Gaussian filter to the image,
            by default 0 (no blur)
        blur_channel :int, tuple, list, optional
            the channel(s) to apply Gaussian blur,
            by default None (apply to all channels)
        blur_chance : float, optional
            probability to apply gaussian blur to an image,
            by default 0.1
        fill_mode : str, optional
            the fill mode in affine transformation
            (rotation, zooming, shifting / translation),
            one of {'reflect', 'constant', 'nearest', 'mirror', 'wrap'},
            by default 'constant'
        cval : int, optional
            When rotation, or zooming, or shifting is applied to the image,
            `cval` is the value to fill past edges of input
            if `fill_mode` is 'constant'.
            By default 0
        """

    def __init__(self, rank,
                 rotation_range=0, rotation_axis=0, rotation_chance=0.2,
                 zoom_range=1, zoom_chance=0.2,
                 shift_range=None, shift_chance=0.1,
                 flip_axis=None,
                 brightness_range=1, brightness_channel=None,
                 brightness_chance=0.1,
                 contrast_range=1, contrast_channel=None,
                 contrast_chance=0.1,
                 noise_variance=0, noise_channel=None,
                 noise_chance=0.1,
                 blur_range=0, blur_channel=None, blur_chance=0.1,
                 fill_mode='constant', cval=0):
        """
        Apply transformation in 2d and 3d image for augmentation
        """
        # check if perform affine transform
        self.affine_transform = rotation_range > 0 or \
            zoom_range != 1 or shift_range is not None

        # get the low high limit of the range
        if self.affine_transform:
            # 2d: rank=3; 3d: rank=4
            self.rotation_range, self.zoom_range, \
                self.shift_range = get_range_affine_transform(
                    rank, rotation_range, zoom_range, shift_range)

            self.rotation_axis = rotation_axis
            self.rotation_chance = rotation_chance

            self.zoom_chance = zoom_chance
            self.shift_chance = shift_chance

            self.fill_mode = fill_mode
            self.cval = cval

        # flip channel in the form of iterator
        if flip_axis is not None and '__iter__' not in dir(flip_axis):
            self.flip_axis = [flip_axis]
        else:
            self.flip_axis = flip_axis

        self.brightness_range = brightness_range

        # low, high of brightness
        if brightness_range != 1:
            self.brightness_range = get_range_value(
                brightness_range,
                default_val=1)
            self.brightness_chance = brightness_chance
            self.brightness_channel = brightness_channel
        else:
            self.brightness_range = brightness_range

        # low, high of contrast
        if contrast_range != 1:
            self.contrast_range = get_range_value(
                contrast_range,
                default_val=1)
            self.contrast_chance = contrast_chance
            self.contrast_channel = contrast_channel
        else:
            self.contrast_range = contrast_range

        # low, high of noise
        if noise_variance != 0:
            self.noise_variance = get_range_value(
                noise_variance,
                default_val=0)
            self.noise_chance = noise_chance
            self.noise_channel = noise_channel
        else:
            self.noise_variance = noise_variance

        # low, high of blur sigma
        if blur_range != 0:
            self.blur_range = get_range_value(
                blur_range,
                default_val=0)
            self.blur_chance = blur_chance
            self.blur_channel = blur_channel
        else:
            self.blur_range = blur_range

    def transform(self, images, targets=None):
        """
        Apply augmentation to a batch of images

        Parameters
        ----------
        images : np.array
            the image batch
        targets : np.array, optional
            the target batch, by default None

        Returns
        -------
        np.array
            the transformed images batch (and target)
        """
        # copy to another version
        transformed_images = images.copy()
        if targets is not None:
            transformed_targets = targets.copy()

        # loop through
        for i in range(len(images)):
            # apply affine transform if possible
            if self.affine_transform:
                theta, zoom_factor, shift = get_random_affine_params(
                    rotation_range=self.rotation_range,
                    rotation_chance=self.rotation_chance,
                    zoom_range=self.zoom_range,
                    zoom_chance=self.zoom_chance,
                    shift_range=self.shift_range,
                    shift_chance=self.shift_chance)
                # Only apply affine transform when needed
                if theta != 0 or zoom_factor != 1 or not np.all(shift == 0):
                    transformed_images[i] = apply_affine_transform(
                        transformed_images[i],
                        mode=self.fill_mode, cval=self.cval,
                        theta=theta, rotation_axis=self.rotation_axis,
                        zoom_factor=zoom_factor,
                        shift=shift)

                    if targets is not None:
                        transformed_targets[i] = apply_affine_transform(
                            transformed_targets[i],
                            mode=self.fill_mode, cval=self.cval,
                            theta=theta, rotation_axis=self.rotation_axis,
                            zoom_factor=zoom_factor,
                            shift=shift)

            # flip image
            if self.flip_axis is not None:
                actual_flip_axis = []
                for channel in self.flip_axis:
                    if np.random.uniform() < 0.5:
                        actual_flip_axis.append(channel)

                if len(actual_flip_axis) > 0:
                    transformed_images[i] = apply_flip(
                        transformed_images[i], actual_flip_axis)

                    if targets is not None:
                        transformed_targets[i] = apply_flip(
                            transformed_targets[i], actual_flip_axis)

            # brightness
            if self.brightness_range != 1 and \
                    np.random.uniform() < self.brightness_chance:
                transformed_images[i] = change_brightness(
                    transformed_images[i],
                    np.random.uniform(*self.brightness_range),
                    channel=self.brightness_channel)

            # contrast
            if self.contrast_range != 1 and \
                    np.random.uniform() < self.contrast_chance:
                transformed_images[i] = change_contrast(
                    transformed_images[i],
                    np.random.uniform(*self.contrast_range),
                    channel=self.contrast_channel)

            # gaussian noise
            if self.noise_variance != 0 and \
                    np.random.uniform() < self.noise_chance:
                transformed_images[i] = gaussian_noise(
                    transformed_images[i],
                    np.random.uniform(*self.noise_variance),
                    channel=self.noise_channel)

            # gaussian blur
            if self.blur_range != 0 and np.random.uniform() < self.blur_chance:
                transformed_images[i] = gaussian_blur(
                    transformed_images[i],
                    np.random.uniform(*self.blur_range),
                    channel=self.blur_channel)

        if targets is None:
            return transformed_images
        else:
            return transformed_images, transformed_targets


def get_range_value(value, default_val=1):
    if '__iter__' in dir(value):
        low, high = value
    elif value < default_val:
        low, high = value, default_val
    else:
        low, high = default_val, value

    return low, high


def get_range_affine_transform(rank, rotation_range,
                               zoom_range,
                               shift_range):

    if shift_range is None:
        shift_low = np.zeros(rank-1)
        shift_high = np.zeros(rank-1)
    else:
        if '__iter__' not in dir(shift_range):
            shift_range = np.array([shift_range] * (rank-1))
        else:
            shift_range = np.array(shift_range)

        if not np.all(shift_range >= 0):
            raise ValueError('All elements in shift range should >= 0')

        shift_low = -shift_range
        shift_high = shift_range

    rotation_low = -rotation_range
    rotation_high = rotation_range

    if '__iter__' in dir(zoom_range):
        zoom_low, zoom_high = zoom_range
    elif zoom_range < 1:
        zoom_low, zoom_high = zoom_range, 1
    else:
        zoom_low, zoom_high = 1, zoom_range

    return (rotation_low, rotation_high), (zoom_low, zoom_high), \
        (shift_low, shift_high)


def get_random_affine_params(rotation_range,
                             rotation_chance,
                             zoom_range, zoom_chance,
                             shift_range, shift_chance):
    if np.random.uniform() < rotation_chance:
        theta = np.random.uniform(*rotation_range)
    else:
        theta = 0

    if np.random.uniform() < zoom_chance:
        zoom_factor = np.random.uniform(*zoom_range)
    else:
        zoom_factor = 1

    if np.random.uniform() < shift_chance:
        shift_factor = np.random.uniform(*shift_range)
    else:
        shift_factor = np.zeros(len(shift_range[0]))

    return theta, zoom_factor, shift_factor


def apply_augmentation(images, targets=None,
                       rotation_range=0, rotation_axis=0, rotation_chance=0.2,
                       zoom_range=1, zoom_chance=0.2,
                       shift_range=None, shift_chance=0.1,
                       flip_axis=None,
                       brightness_range=1, brightness_channel=None,
                       brightness_chance=0.1,
                       contrast_range=1, contrast_channel=None,
                       contrast_chance=0.1,
                       noise_variance=0, noise_channel=None,
                       noise_chance=0.1,
                       blur_range=0, blur_channel=None, blur_chance=0.1,
                       fill_mode='constant', cval=0):  # pragma: no cover
    # copy to another version
    transformed_images = images.copy()
    if targets is not None:
        transformed_targets = targets.copy()

    # check if perform affine transform
    affine_transform = rotation_range > 0 or \
        zoom_range != 1 or shift_range is not None

    # get the low high limit of the range
    if affine_transform:
        rotation, zoom, shift_var = get_range_affine_transform(
            images.ndim - 1, rotation_range, zoom_range, shift_range)

    # flip channel in the form of iterator
    if flip_axis is not None and '__iter__' not in dir(flip_axis):
        flip_axis = [flip_axis]

    for i, image in enumerate(images):
        if affine_transform:
            theta, zoom_factor, shift = get_random_affine_params(
                rotation_range=rotation, rotation_chance=rotation_chance,
                zoom_range=zoom, zoom_chance=zoom_chance,
                shift_range=shift_var, shift_chance=shift_chance)
            # Only apply affine transform when needed
            if theta != 0 or zoom_factor != 1 or not np.all(shift == 0):
                transformed_images[i] = apply_affine_transform(
                    transformed_images[i],
                    mode=fill_mode, cval=cval,
                    theta=theta, rotation_axis=rotation_axis,
                    zoom_factor=zoom_factor,
                    shift=shift)

                if targets is not None:
                    transformed_targets[i] = apply_affine_transform(
                        transformed_targets[i],
                        mode=fill_mode, cval=cval,
                        theta=theta, rotation_axis=rotation_axis,
                        zoom_factor=zoom_factor,
                        shift=shift)

        if flip_axis is not None:
            actual_flip_axis = []
            for channel in flip_axis:
                if np.random.uniform() < 0.5:
                    actual_flip_axis.append(channel)

            if len(actual_flip_axis) > 0:
                transformed_images[i] = apply_flip(
                    transformed_images[i], actual_flip_axis)

                if targets is not None:
                    transformed_targets[i] = apply_flip(
                        transformed_targets[i], actual_flip_axis)

        if brightness_range != 1 and np.random.uniform() < brightness_chance:
            bright_low, bright_high = get_range_value(brightness_range,
                                                      default_val=1)

            transformed_images[i] = change_brightness(
                transformed_images[i],
                np.random.uniform(bright_low, bright_high),
                channel=brightness_channel)

        if contrast_range != 1 and np.random.uniform() < contrast_chance:
            contrast_low, contrast_high = get_range_value(contrast_range,
                                                          default_val=1)

            transformed_images[i] = change_contrast(
                transformed_images[i],
                np.random.uniform(contrast_low, contrast_high),
                channel=contrast_channel)

        if noise_variance > 0 and np.random.uniform() < noise_chance:
            noise_low, noise_high = get_range_value(noise_variance,
                                                    default_val=0)

            transformed_images[i] = gaussian_noise(
                transformed_images[i],
                np.random.uniform(noise_low, noise_high),
                channel=noise_channel)

        if blur_range != 0 and np.random.uniform() < blur_chance:
            blur_low, blur_high = get_range_value(blur_range,
                                                  default_val=0)

            transformed_images[i] = gaussian_blur(
                transformed_images[i],
                np.random.uniform(blur_low, blur_high),
                channel=blur_channel)

    if targets is None:
        return transformed_images
    else:
        return transformed_images, transformed_targets

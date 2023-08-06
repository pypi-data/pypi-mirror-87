import numpy as np
from itertools import product


def get_patch_indice(shape, patch_size, overlap):
    if len(patch_size) != len(shape):
        raise ValueError

    res = []
    for length, size in zip(shape, patch_size):
        # the lower index will increase with step = size * (1-overlap)
        indice = np.arange(0, length - size, int(size*(1-overlap)))
        # add the last index, which may not follow the overlap rule
        if length - size != indice[-1]:
            indice = np.append(indice, length - size)

        res.append(indice)

    # return the combination of all dimensions
    return list(product(*res))


def get_patch_indice_all(images, patch_size, overlap):
    res = []
    for i, img in enumerate(images):
        indice = get_patch_indice(img.shape[:-1], patch_size, overlap)
        res.extend(product([i], indice))

    return res


def check_drop(images, patch_indice, patch_size,
               drop_fraction, check_drop_channel=None):
    if check_drop_channel is None:
        # all channel are checked
        check_images = images.copy()
        pixel_sum = np.prod(patch_size) * images[0].shape[-1]

        # all images are of same size, get the whole min
        if images.dtype is not object:
            imin = check_images.min()
    else:  # Only specific channels are checked
        pixel_sum = np.prod(patch_size)
        # all images are of same size, get the whole min, take the last axis
        if images.dtype is not object:
            # all images are
            check_images = images[..., check_drop_channel]
            imin = check_images.min()
        else:
            # create the new image one by one
            check_images = np.array([img[..., check_drop_channel]
                                     for img in images], dtype=object)

    res = []

    for i, indice in patch_indice:
        # imin has to be recalculated for each image with different sizes
        if images.dtype is object:
            imin = check_images[i].min()

        if len(indice) == 2:
            x, y = indice
            w, h = patch_size
            check_data = check_images[i][x:x+w, y:y+h].flatten()
            passed = len(check_data[check_data > imin]
                         ) / pixel_sum > drop_fraction
        elif len(indice) == 3:
            x, y, z = indice
            w, h, d = patch_size
            check_data = check_images[i][x:x+w, y:y+h, z:z+d].flatten()

            passed = len(check_data[check_data > imin]
                         ) / pixel_sum > drop_fraction

        res.append(passed)

    return res


def get_patches(images, target=None, patch_indice=None, patch_size=None,
                stratified=True, batch_size=None,
                drop_fraction=0.1, check_drop_channel=None):
    try:
        images = np.array(images)
    except Exception:  # compatity check  # pragma: no cover
        images = np.array(images, dtype=object)

    if images.dtype == object:  # pragma: no cover
        raise NotImplementedError(
            'Cannot handle images with different sizes.'
            'Consider using get_patches_different_images')

    if target is not None:
        try:
            target = np.array(target)
        except Exception:  # compatity check  # pragma: no cover
            target = np.array(target, dtype=object)
        if not images.shape[1:-1] == target.shape[1:-1]:
            raise ValueError(
                'Image and target shape are mismatched ({} != {})'.format(
                    images.shape[:-1], target.shape[:-1]))

    if patch_indice is None or patch_size is None:
        raise ValueError('patch_indice and patch_size are required.')

    pixel_sum = np.prod(patch_size)

    # create indice for each images
    # [(0, (x,y,z)), (0, (x',y',z')), (1, (x,y,z)), (1, (x',y',z'))]

    patch_indice = np.array(
        list((product(np.arange(len(images)), patch_indice))), dtype=object)

    if drop_fraction > 0:
        check_drop_list = check_drop(images, patch_indice, patch_size,
                                     drop_fraction, check_drop_channel)

        patch_indice = patch_indice[check_drop_list]

    patch_img = np.zeros((len(patch_indice), *patch_size, images.shape[-1]))

    if target is not None:
        patch_label = np.zeros((len(patch_indice), *patch_size, 1))
        if stratified:
            label_percentage = np.zeros(len(patch_indice))
    for i, (im_i, indice) in enumerate(patch_indice):
        if len(indice) == 2:
            x, y = indice
            w, h = patch_size
            patch_img[i] = images[im_i][x:x+w, y:y+h]

            if target is not None:
                patch_label[i] = target[im_i][x:x+w, y:y+h]
                if stratified:
                    label_percentage[i] = patch_label[i].sum() / pixel_sum
        elif len(indice) == 3:
            x, y, z = indice
            w, h, d = patch_size

            patch_img[i] = images[im_i][x:x+w, y:y+h, z:z+d]
            if target is not None:
                patch_label[i] = target[im_i][x:x+w, y:y+h, z:z+d]
                if stratified:
                    label_percentage[i] = patch_label[i].sum() / pixel_sum

    if target is None:
        return patch_img
    else:
        if stratified:
            new_index = np.arange(len(patch_indice))
            if batch_size is None or len(patch_indice) < batch_size:
                np.random.shuffle(new_index)
            else:
                new_index = get_stratified_index(label_percentage, batch_size)
            patch_img = patch_img[new_index]
            patch_label = patch_label[new_index]

        return patch_img, patch_label


def get_patches_different_images(images, target=None, patch_indice=None,
                                 patch_size=None, overlap=0,
                                 stratified=True,
                                 drop_fraction=0.1,
                                 check_drop_channel=None):  # pragma: no cover
    images = np.array(images, dtype=object)
    target = np.array(target, dtype=object)

    indice = get_patch_indice_all(images, patch_size, overlap)

    raise NotImplementedError


def get_stratified_index(values, sample_size):
    median = np.median(values)

    index = np.arange(len(values))
    positive_index = index[values > median]
    negative_index = index[values <= median]

    np.random.shuffle(positive_index)
    np.random.shuffle(negative_index)

    split_num = int(np.ceil(len(values) / sample_size))
    pos_num = len(positive_index) // split_num
    step = 1

    inners = [[] for _ in range(split_num)]
    # cannot evenly distribute in each batch
    if pos_num == 0:
        step = int(np.ceil(split_num / len(positive_index)))

    while len(positive_index) > 0:
        for i in range(0, split_num, step):
            if len(positive_index) == 0:
                break
            inners[i].append(positive_index[-1])
            positive_index = positive_index[:-1]

    for inner in inners:
        while len(inner) < sample_size and len(negative_index) > 0:
            inner.append(negative_index[-1])
            negative_index = negative_index[:-1]
        np.random.shuffle(inner)

    # if len(np.concatenate(inners)) != len(values):
    #     raise RuntimeError(
    #         'Something wrong happened. Please contact the developer')

    # if len(negative_index) > 0 or len(positive_index) > 0:
    #     raise RuntimeError(
    #         'Something wrong happened. Please contact the developer')

    return np.concatenate(inners)

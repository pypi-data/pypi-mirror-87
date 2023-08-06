import matplotlib.pyplot as plt
import numpy as np


def create_pascal_label_colormap():
    colormap = np.zeros((256, 3), dtype=int)
    ind = np.arange(256, dtype=int)
    for shift in reversed(range(8)):
        for channel in range(3):
            colormap[:, channel] |= ((ind >> channel) & 1) << shift
        ind >>= 3
    return colormap

def label_to_color_image(label):
    if label.ndim != 2:
        raise ValueError('Expect 2-D input label')
    colormap = create_pascal_label_colormap()
    if np.max(label) >= len(colormap):
        raise ValueError('label value too large.')
    return colormap[label]

def vis_segmentation(image, seg_map, name='demo.jpg', if_save=False, if_show=True):

    seg_image = label_to_color_image(seg_map).astype(np.uint8)
    plt.figure()
    plt.imshow(image)
    plt.imshow(seg_image, alpha=0.7)
    plt.axis('off')

    if if_save:
        plt.savefig("vis_{}".format(name))

    if if_show:
        plt.show()
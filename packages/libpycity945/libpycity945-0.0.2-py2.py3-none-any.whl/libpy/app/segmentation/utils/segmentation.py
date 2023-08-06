"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 * author: 谢城   email: 2654229893@qq.com    github: https://gitee.com/city945/
 * date: 2020-11-28
 * desc: 语义分割任务用到的工具函数
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import numpy as np

# cityscapes 数据集描述 
num_classes = 19
colors = [
    [128, 64, 128],
    [244, 35, 232],
    [70, 70, 70],
    [102, 102, 156],
    [190, 153, 153],
    [153, 153, 153],
    [250, 170, 30],
    [220, 220, 0],
    [107, 142, 35],
    [152, 251, 152],
    [0, 130, 180],
    [220, 20, 60],
    [255, 0, 0],
    [0, 0, 142],
    [0, 0, 70],
    [0, 60, 100],
    [0, 80, 100],
    [0, 0, 230],
    [119, 11, 32],
]
class_names = ["unlabelled", "road", "sidewalk", "building", "wall", "fence", "pole",
                "traffic_light", "traffic_sign", "vegetation", "terrain", "sky", "person", 
                "rider", "car", "truck", "bus", "train", "motorcycle", "bicycle",
                ]
void_classes = [0, 1, 2, 3, 4, 5, 6, 9, 10, 14, 15, 16, 18, 29, 30, -1]
valid_classes = [7, 8, 11, 12, 13, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33]
label_colours = dict(zip(range(19), colors))
class_map = dict(zip(valid_classes, range(19)))
ignore_index = 250


def decode_segmap_color(temp):
    """把类别Id填成RGB值
    """
    r = temp.copy()
    g = temp.copy()
    b = temp.copy()
    for l in range(num_classes):
        r[temp == l] = label_colours[l][0]
        g[temp == l] = label_colours[l][1]
        b[temp == l] = label_colours[l][2]

    rgb = np.zeros((temp.shape[0], temp.shape[1], 3))
    rgb[:, :, 0] = r / 255.0
    rgb[:, :, 1] = g / 255.0
    rgb[:, :, 2] = b / 255.0
    return rgb

def decode_segmap_gray(temp):
    """把类别Id填成类别灰度值
    """
    ids = np.zeros((temp.shape[0], temp.shape[1]), dtype=np.uint8)
    for l in range(num_classes):
        ids[temp == l] = valid_classes[l]

    return ids

def encode_segmap(mask):
    """把无效的类别置0
    """
    for _voidc in void_classes:
        mask[mask == _voidc] = ignore_index
    for _validc in valid_classes:
        mask[mask == _validc] = class_map[_validc]

    return mask

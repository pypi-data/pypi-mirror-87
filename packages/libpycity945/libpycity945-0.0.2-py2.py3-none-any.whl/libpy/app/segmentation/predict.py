#coding:utf8

# predict 相当于拿真实场景的数据来预测，需求: 1. 真实数据的处理，不必构造数据集类 2. 应用接口，减少对其他模块的依赖，直接传入图片或文件夹路径 3. 保存预测图片，计算帧率 4. 应用阶段
"""
依赖文件:
1. HardNet.py 
2. segmentation.py 
"""

from .components import models
from .utils.segmentation import decode_segmap_color, decode_segmap_gray

import numpy as np
from argparse import ArgumentParser
import os
from PIL import Image
import torch
import time, timeit
import imageio

# torch.backends.cudnn.benchmarks = True

# 输入图片处理
def preprocess(path, args):
    img = np.array(Image.open(path).resize((args.input_size[1], args.input_size[0])))  # uint8 with RGB mode
    img = img[:, :, ::-1]  # RGB -> BGR
    img = img.astype(np.float64)

    value_scale = 255
    mean = [0.406, 0.456, 0.485]
    mean = [item * value_scale for item in mean]
    std = [0.225, 0.224, 0.229]
    std = [item * value_scale for item in std]
    img = (img - mean) / std # 默认做归一化
    # NHWC -> NCHW
    img = img.transpose(2, 0, 1)    
    img = torch.from_numpy(img).float()
    # 添加上batch维度
    img = torch.unsqueeze(img, 0)
    return img

def predict_img(args):
    # data 
    image_list = []
    if args.image_path:
        image_list.append(args.image_path)
    elif args.image_root:
        image_list = [os.path.join(args.image_root, filename) for filename in os.listdir(args.image_root)]
        print(f"找到{len(image_list)}张预测图片")
    else: 
        print("请输入待预测图片目录或文件路径")

    # model
    model = getattr(models, args.model_name)(19)
    checkpoints = torch.load(args.load_model_path)
    model.load_state_dict(checkpoints['model_state'])
    model.to(args.device)

    model.eval()
    start_time = timeit.default_timer()
    total_time = 0
    for i in range(len(image_list)):
        input = preprocess(image_list[i], args).to(args.device)
        torch.cuda.synchronize()
        start_time = time.perf_counter()
        outputs = model(input)
        torch.cuda.synchronize()
        elapsed_time = time.perf_counter() - start_time
        total_time += elapsed_time

        pred = np.squeeze(outputs.data.max(1)[1].cpu().numpy(), axis=0)
        decoded = decode_segmap_gray(pred)
        imageio.imwrite(f'{args.out_dir}/test{i}_gray.png', decoded)

        decoded = decode_segmap_color(pred)
        img_input = np.squeeze(input.cpu().numpy(),axis=0)
        img_input = img_input.transpose(1, 2, 0)
        blend = img_input * 0.2 + decoded * 0.8
        imageio.imwrite(f'{args.out_dir}/test{i}_rgb.png', blend) # ? 惊讶TODO 浮点负数杂绘制的图

    print("Total Frame Rate = %.2f fps" %(len(image_list)/total_time))


def predict(image_path=None, image_root=None, input_size=(512,1024), load_model_path="~/.cache/torch/HardNet.pt", out_dir="./", use_gpu=True, gpu_ids="0"):
    # args = object() # python 自定义类可以动态添加属性，而内置类不可以
    class Args():pass
    args = Args()
    args.model_name = "HardNet"
    args.input_size = input_size
    args.load_model_path = os.path.expanduser(load_model_path) # os.path.abspath(load_model_path) # abspath并不能很好替换~
    args.image_root = os.path.expanduser(image_root) if image_root else None
    args.image_path = os.path.expanduser(image_path) if image_path else None
    args.out_dir = os.path.expanduser(out_dir) 
    args.use_gpu = use_gpu
    args.gpu_ids = gpu_ids

    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_ids # 设置使用那几块卡 必须在 import torch 之前
    import torch
    args.device = torch.device('cuda') if args.use_gpu else torch.device('cpu')
    if not os.path.exists(args.out_dir): 
        os.makedirs(args.out_dir)
    
    # 处理模型文件
    if not os.path.exists(args.load_model_path): 
        print("未找到模型文件，download......")
        dirname = os.path.dirname(args.load_model_path)
        if not os.path.exists(dirname):os.makedirs(dirname)
        os.system(f"wget -P {dirname} http://101.200.172.26:8000/file/httpFiles/HardNet.pt  ")

    predict_img(args)

# def parse_args():
#     parser = ArgumentParser(description="应用接口，减少对其他模块的依赖，直接传入图片或文件夹路径")
#     parser.add_argument('--model_name',     default="HardNet",      type=str,   help="model name for predict")
#     parser.add_argument('--input_size',     default="512,1024",     type=str,   required=True,  help="input size") # nanjing 768*1536
#     parser.add_argument('--load_model_path',default=None,           type=str,   required=True, help="load model path")
#     parser.add_argument('--image_root',     default=None,           type=str,   help="image root dir for predict")
#     parser.add_argument('--image_path',     default=None,           type=str,   help="image path dir for predict")
#     parser.add_argument('--out_dir',        default="./out/predict",type=str,   help="Output picture directory")
#     parser.add_argument('--use_gpu',        default=True,           type=str,   help="use gpu or not")
#     parser.add_argument('--gpu_ids',        default="0",            type=str,   help="gpu ids")

#     args = parser.parse_args()
#     os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_ids # 设置使用那几块卡 必须在 import torch 之前
#     import torch
#     args.device = torch.device('cuda') if args.use_gpu else torch.device('cpu')
#     args.input_size = tuple(map(int, args.input_size.split(','))) 
#     if not os.path.exists(args.out_dir): 
#         os.makedirs(args.out_dir)
    
#     return args

# if __name__ == "__main__":
#     args = parse_args()
#     predict(args)
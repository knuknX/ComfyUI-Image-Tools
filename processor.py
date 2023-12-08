import cv2
import torch
import numpy as np
from rembg import remove
from .utils import tensorToNumpy
from .utils import numpyToTensor

def resize_image(image, target_width=512, target_height=768):
    # 如果是tensor就转成numpy
    if isinstance(image, torch.Tensor):
        image = tensorToNumpy(image) * 255.0
        image = image.astype(np.uint8)

    original_height, original_width = image.shape[:2]
    # 如果输入图片的高度超过768，则保持宽高比压缩图片到高度为768
    # 计算缩放比例
    scale = target_height / original_height
    # 等比例缩放图片
    new_width = int(original_width * scale)
    new_height = target_height
    image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # 压缩后的图片宽度处理
    if new_width > target_width:
        # 如果宽度超过512，从图片中间截取512宽度
        start_x = (new_width - target_width) // 2
        image = image[:, start_x:start_x + target_width]
    elif new_width < target_width:
        # 如果宽度小于512，用透明像素填充2侧到512
        pad_left = (target_width - new_width) // 2
        pad_right = target_width - new_width - pad_left

        # 确保图像是BGRA格式
        if len(image.shape) == 2:  # 灰度图像需要转换为颜色图像才能填充透明像素
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
        elif image.shape[2] == 3:  # RGB图像需要添加Alpha通道
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

        # 创建左右透明边框
        alpha_channel_left = np.zeros((new_height, pad_left, 4), dtype=image.dtype)
        alpha_channel_left[:, :, 3] = 255  # 设置Alpha通道为不透明
        alpha_channel_right = np.zeros((new_height, pad_right, 4), dtype=image.dtype)
        alpha_channel_right[:, :, 3] = 255  # 设置Alpha通道为不透明

        # 水平堆叠图像和透明边框
        image = np.hstack((alpha_channel_left, image, alpha_channel_right))

        # 修复透明通道，使其为透明
        image[:, :, 3] = 0
        image[:, pad_left:pad_left + new_width, 3] = 255

    return numpyToTensor(image)

def remove_background(image):
    # 如果是tensor就转成numpy
    if isinstance(image, torch.Tensor):
        image = tensorToNumpy(image) * 255.0
        image = image.astype(np.uint8)
    image = remove(image, bgcolor=(255, 255, 255, 255), alpha_matting_erode_size=1)
    image = image[:, :, :3]
    return numpyToTensor(image)

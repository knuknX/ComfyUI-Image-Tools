import cv2
import requests
import numpy as np
import torchvision.transforms as transforms
from .utils import numpyToTensor

# 从路径中加载图片
def load_from_path(path):
    print(path)
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if image.ndim == 3 else image
    return numpyToTensor(image_rgb)

def load_from_url(url):
    # 使用 requests 获取图像数据
    response = requests.get(url)
    # 将图像数据转换为 NumPy 数组
    img_array = np.frombuffer(response.content, dtype=np.uint8)
    # 使用 cv2.imdecode 解码图像
    transf = transforms.ToTensor()
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if image.ndim == 3 else image
    return transf(image_rgb).permute(1, 2, 0).unsqueeze(0)
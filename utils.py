import numpy as np
import cv2
import torchvision.transforms as transforms

# numpy转tensor
def numpyToTensor(numpy):
    transf = transforms.ToTensor()
    return transf(numpy)


# tensor转numpy
def tensorToNumpy(tensor):
    # 1. 移除批量维度
    tensor = tensor.squeeze(0)
    # 2. 从CHW转换为HWC
    tensor = tensor.permute(1, 2, 0)
    # 3. 转换为numpy ndarray
    image_np = tensor.numpy()
    # 4. 将像素值从[0, 1]缩放到[0, 255]
    image_np = (image_np * 255).astype(np.uint8)
    # 5. 如果是RGB格式，转换为BGR
    if image_np.shape[2] == 3:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    return image_np

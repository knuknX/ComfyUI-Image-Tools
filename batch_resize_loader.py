import os
import cv2
import numpy as np
from rembg import remove

def single_load_and_resize(input_image_path, output_image_path, target_width=512, target_height=768):
    # 读取图片
    image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)
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
            print(input_image_path+"image shape = 2")
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
        elif image.shape[2] == 3:  # RGB图像需要添加Alpha通道
            print(input_image_path+"image shape[2] = 3")
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

    # 去除背景
    image = remove(image, bgcolor=(255, 255, 255, 255), alpha_matting_erode_size=1)
    # 保存调整后的图片
    cv2.imwrite(output_image_path, image)

def batch_load_and_resize(input_dir_path, output_dir_path, output_prefix, target_width=512, target_height=768):
    count = 1
    # 遍历输入文件夹下的所有文件,并将他们全部转换成png格式放到临时文件夹中
    for filename in os.listdir(input_dir_path):
        filepath = os.path.join(input_dir_path, filename)
        tmppath = os.path.join(input_dir_path, 'tmp')
        if not os.path.exists(tmppath):
            os.makedirs(tmppath)
        # 检查文件是否是图片文件
        if os.path.isfile(filepath) and filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            # 打开图像
            img = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
            # 构建输出文件路径，将扩展名改为.png
            output_filepath = os.path.join(tmppath, str(count) + '.png')
            # 将图像保存为PNG格式
            cv2.imwrite(output_filepath, img)
        count = count + 1
    # 遍历临时文件夹下的所有文件,调整他们的大小
    count = 1
    result_files = []
    for filename in os.listdir(tmppath):
        target_file = os.path.join(output_dir_path,output_prefix+"_"+str(count)+".png")
        print(filename,"-->",target_file)
        filepath = os.path.join(tmppath, filename)
        single_load_and_resize(filepath,target_file,target_width,target_height)
        count = count + 1
        result_files.append(target_file)
    return result_files
import requests
from torchvision import transforms
import base64
import json
import torch
import io

def upload_to_chevereto(image, url, key):
    # 在第一个维度上均匀拆分为多个张量，每个张量对应一张图片
    chunk_tensors = torch.chunk(image, chunks=image.shape[0], dim=0)

    # 处理每张图片，这里仅打印每张图片的形状
    image_info_list = []
    for i, img_tensor in enumerate(chunk_tensors):
        print(f"Shape of image {i + 1}: {img_tensor.squeeze(0).permute(2, 0, 1).shape}")

        # 将 PyTorch Tensor 转换为base64
        image_data_from_tensor = transforms.ToPILImage()(img_tensor.squeeze(0).permute(2, 0, 1))
        byte_io = io.BytesIO()
        image_data_from_tensor.save(byte_io, format='PNG')
        base64_image = base64.b64encode(byte_io.getvalue()).decode('utf-8')

        # 设置请求参数
        params = {
            "key": key,
            "source": base64_image
        }

        # 发送POST请求
        response = requests.post(url, data=params)

        # 获取响应内容
        resp = response.text
        print("upload image:", resp)

        # 解析响应结果获取url
        resp_obj = json.loads(resp)
        image_obj = resp_obj.get("image")

        # 构造ImageDTO对象
        imageDTO = {
            "name": image_obj.get("name"),
            "extension": image_obj.get("extension"),
            "size": image_obj.get("size"),
            "width": image_obj.get("width"),
            "height": image_obj.get("height"),
            "date": image_obj.get("date"),
            "md5": image_obj.get("md5")
        }
        print(imageDTO)
        image_info_list.append(imageDTO)
    json_str = json.dumps(image_info_list)
    print(json_str)
    return json_str

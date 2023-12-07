from .batch_resize_loader import batch_load_and_resize
import torchvision.transforms as transforms
import cv2
import requests
import numpy as np

class BatchImageResizeProcessor:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                        "input_path": ("STRING", { "default": "" }),
                        "output_path": ("STRING", { "default": ""}),
                        "output_prefix": ("STRING", {"default": ""}),
                        "size": (["512*768", "512*512", "768*768"],)
                    },
                }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "batch_load"
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "Tools"

    def batch_load(self, input_path,  output_path, output_prefix, size):
        if size == "512*768":
            return (batch_load_and_resize(input_path,output_path,output_prefix,512,768),)
        if size == "512*512":
            return (batch_load_and_resize(input_path,output_path,output_prefix,512,512),)
        if size == "768*768":
            return (batch_load_and_resize(input_path,output_path,output_prefix,768,768),)
        return (None,)

class SingleImagePathLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                        "path": ("STRING", { "default": "" }),
                    },
                }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load"
    CATEGORY = "Tools"

    def load(self, path):
        transf = transforms.ToTensor()
        image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if image.ndim == 3 else image
        image = transf(image_rgb).permute(1,2,0).unsqueeze(0)
        return (image,)

class SingleImageUrlLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                        "url": ("STRING", { "default": "" }),
                    },
                }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load"
    CATEGORY = "Tools"

    def load(self, url):
        # 使用 requests 获取图像数据
        response = requests.get(url)
        # 将图像数据转换为 NumPy 数组
        img_array = np.frombuffer(response.content, dtype=np.uint8)
        # 使用 cv2.imdecode 解码图像
        transf = transforms.ToTensor()
        image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if image.ndim == 3 else image
        image = transf(image_rgb).permute(1,2,0).unsqueeze(0)
        return (image,)

NODE_CLASS_MAPPINGS = {
    "CDL.BatchImageResizeProcessor": BatchImageResizeProcessor,
    "CDL.SingleImagePathLoader": SingleImagePathLoader,
    "CDL.SingleImageUrlLoader": SingleImageUrlLoader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CDL.BatchImageResizeProcessor": "BatchImageResizeProcessor",
    "CDL.SingleImagePathLoader": "SingleImagePathLoader",
    "CDL.SingleImageUrlLoader": "SingleImageUrlLoader",
}

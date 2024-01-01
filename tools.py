import json

from .src.loader import load_from_path
from .src.loader import load_from_url
from .src.notify import post_notify
from .src.processor import resize_image
from .src.processor import remove_background
from .src.upload import upload_to_chevereto


# 单张图片路径加载器
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
        return (load_from_path(path),)

# 单张图片URL加载器
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
        return (load_from_url(url),)

# 图片标准尺寸调整处理器
class ImageStandardResizeProcessor:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                        "image": ("IMAGE",),
                        "size": (["512*768", "512*512", "768*768"],)
                    },
                }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "resize"
    CATEGORY = "Tools"
    def resize(self, image, size):
        if size == "512*768":
            return (resize_image(image,512,768),)
        if size == "512*512":
            return (resize_image(image,512,512),)
        if size == "768*768":
            return (resize_image(image,768,768),)
        return (image,)

# 图片背景移除处理器
class ImageBgRemoveProcessor:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                        "image": ("IMAGE",),
                    },
                }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "remove"
    CATEGORY = "Tools"
    def remove(self, image):
        return (remove_background(image),)

# 图片背景移除处理器
class BatchImagePathLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                        "path": ("STRING",{ "default": "" }),
                    },
                }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load"
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "Tools"
    def load(self, path):
        import os
        import glob
        def get_image_paths(folder_path, extensions=['jpg', 'jpeg', 'png', 'gif', 'webp']):
            image_paths = []
            for extension in extensions:
                pattern = os.path.join(folder_path, f'*.{extension}')
                image_paths.extend(glob.glob(pattern))
            return image_paths

        image_paths = get_image_paths(path)

        # 加載所有圖片
        images = []
        for image_path in image_paths:
            images.append(load_from_path(image_path))
        return (images,)

# 图片上传到chevereto
class ImageCheveretoUploader:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                        "image": ("IMAGE",),
                        "url": ("STRING", {"default": ""}),
                        "key": ("STRING", {"default": ""})
                    },
                }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "upload"
    CATEGORY = "Tools"
    def upload(self, image, url, key):
        return (upload_to_chevereto(image,url,key),)

# 发送通知消息
class JSONMessageNotifyTool:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                        "url": ("STRING", {"default": ""}),
                        "message": ("STRING", {"default": ""})
                    },
                }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "notify"
    CATEGORY = "Tools"
    def notify(self, url, message):
        return (post_notify(url, json_data=json.loads(message)),)

NODE_CLASS_MAPPINGS = {
    "SingleImagePathLoader": SingleImagePathLoader,
    "SingleImageUrlLoader": SingleImageUrlLoader,
    "ImageStandardResizeProcessor": ImageStandardResizeProcessor,
    "ImageBgRemoveProcessor": ImageBgRemoveProcessor,
    "BatchImagePathLoader": BatchImagePathLoader,
    "ImageCheveretoUploader": ImageCheveretoUploader,
    "JSONMessageNotifyTool": JSONMessageNotifyTool,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SingleImagePathLoader": "SingleImagePathLoader",
    "SingleImageUrlLoader": "SingleImageUrlLoader",
    "ImageStandardResizeProcessor": "ImageStandardResizeProcessor",
    "ImageBgRemoveProcessor": "ImageBgRemoveProcessor",
    "BatchImagePathLoader": "BatchImagePathLoader",
    "ImageCheveretoUploader": "ImageCheveretoUploader",
    "JSONMessageNotifyTool": "JSONMessageNotifyTool",
}

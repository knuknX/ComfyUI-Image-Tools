from .loader import load_from_path
from .loader import load_from_url
from .processor import resize_image
from .processor import remove_background

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
    OUTPUT_IS_LIST = (True,)
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
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "Tools"
    def remove(self, image):
        return (remove_background(image),)

NODE_CLASS_MAPPINGS = {
    "SingleImagePathLoader": SingleImagePathLoader,
    "SingleImageUrlLoader": SingleImageUrlLoader,
    "ImageStandardResizeProcessor": ImageStandardResizeProcessor,
    "ImageBgRemoveProcessor": ImageBgRemoveProcessor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SingleImagePathLoader": "SingleImagePathLoader",
    "SingleImageUrlLoader": "SingleImageUrlLoader",
    "ImageStandardResizeProcessor": "ImageStandardResizeProcessor",
    "ImageBgRemoveProcessor": ImageBgRemoveProcessor,
}

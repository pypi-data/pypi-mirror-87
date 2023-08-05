# coding:utf-8
from PIL import Image


def img_padding_resize(img, padding_size, interpolation=Image.BILINEAR):
    width, height = img.size
    scale = min(padding_size[0]/width, padding_size[1]/height)
    img = img.resize((int(width*scale), int(height*scale)), interpolation)
    background = Image.new('RGB', padding_size, (128, 128, 128)).convert('L')
    background.paste(img, (0, 0))
    return background

import re
import base64
from io import BytesIO
import cv2
import PIL
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import shapely
from shapely.geometry import Polygon

def four_to_eight(arr):
    return [arr[0], arr[1], arr[2], arr[1], arr[2], arr[3], arr[0], arr[3]]

def points2Polygon(point_arr):
    if 4 <= len(point_arr) < 8:
        point_arr = four_to_eight(point_arr)
    assert len(point_arr) >= 8
    a = np.array(point_arr[:8]).reshape(4, 2)
    poly = Polygon(a).convex_hull  # python四边形对象，会自动计算四个点，最后四个点顺序为：左上 左下 右下 右上 左上
    return poly

def polygon_intersection_ratio(poly1, poly2):
    intersect, intersection_area = polygon_intersection_area(poly1, poly2)
    rate1, rate2 = 0.0, 0.0
    if poly1.area != 0:
        rate1 = intersection_area/poly1.area
    if poly2.area != 0:
        rate2 = intersection_area/poly2.area
    return intersect, rate1, rate2

# 计算两个多边形区域的交
def polygon_intersection_area(poly1, poly2):
    if not poly1.intersects(poly2):  # 如果两四边形不相交
        return False, 0
    else:
        try:
            intersection_area = poly1.intersection(poly2).area  # 相交面积
            return True, intersection_area
        except shapely.geos.TopologicalError:
            print('shapely.geos.TopologicalError occured, iou set to 0')
            return False, 0

def clockwise_points(point_arr):
    poly = points2Polygon(point_arr)
    # 坐标顺序变为从y最小的点开始、顺时针
    b = list(poly.exterior.coords)
    # 左上角开始
    if b[2][0] > b[0][0] and b[2][1] > b[0][1]:
        c = np.asarray(b[::-1], dtype=np.int).reshape(-1)
    # 右上角开始
    else:
        c = np.asarray([b[1], b[0], b[3], b[2]], dtype=np.int).reshape(-1)
    d = c[:8]
    return d

def min_rect(arr, clockwise=False):
    arr = np.array(arr).reshape((-1, 2))
    rect = cv2.minAreaRect(arr) # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
    box = cv2.boxPoints(rect) # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
    box = np.round(box)
    if clockwise:
        box = np.array(clockwise_points(np.reshape(box, (-1))))
    box = np.reshape(box, (-1))
    box = np.array(box, dtype=np.int)
    return box

def draw_polygon(img, line_pairs, width=2, fill="red"):
    draw = ImageDraw.Draw(img)
    draw_polygon_from_draw(draw, line_pairs, width=width, fill=fill)

def draw_polygon_from_draw(draw, line_pairs, width=2, fill="red"):
    line_pairs = np.array(line_pairs).reshape((-1, 2))
    line_arr = [tuple(line_pair) for line_pair in line_pairs]
    line_arr.append(line_arr[0])
    draw.line(line_arr, width=width, fill=fill)

def parse_gt_file(path, sep=",\t"):
    gt_res = []
    with open(path, "r") as file:
        for line in file:
            arr = line.strip().split(sep, maxsplit=8)
            if len(arr) < 9:
                continue
            coo = [int(i) for i in arr[:8]]
            content = arr[8]
            pair = (coo, content)
            gt_res.append(pair)
    return gt_res

def write_gt_to_file(gt, file_path, sep=",\t"):
    with open(file_path, "w") as file:
        for index in range(len(gt)):
            ele = gt[index]
            coo = sep.join([str(e) for e in ele[0]])
            content = ele[1].replace("\n", "")
            content = re.sub("\s+", " ", content)
            file.write("{}{}{}\n".format(coo, sep, content))

def pil_to_cv(pil_img):
    return cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)

def cv_to_pil(cv_img):
    return Image.fromarray(cv_img)

def base64_to_cv2(b64str):
    data = base64.b64decode(b64str.encode('utf8'))
    data = np.fromstring(data, np.uint8)
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return data

def base64_to_pil(base64_str):
    imgdata = base64.b64decode(base64_str)
    image_data = BytesIO(imgdata)
    img = Image.open(image_data)
    return img

def pil_to_base64(pil_img, format='png'):
    if format == 'jpg' or format == 'jpeg':
        img = pil_img.convert('RGB')
    else:
        img = pil_img.convert('RGBA')
    output_buffer = BytesIO()
    img.save(output_buffer, format=format)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str.decode("utf-8")

def visualization(img, dets=None, gts=None, font_path='/System/Library/Fonts/PingFang.ttc', font_size=18, font_size_adaptive=False):
    '''
    运行若报错提示字体不存在，则调用时指定字体文件路径font_path
    '''
    origin_type = 0
    main_pic = None
    if isinstance(img, PIL.Image.Image):
        main_pic = img
        origin_type = 1
    elif isinstance(img, np.ndarray):
        main_pic = Image.fromarray(img)
        origin_type = 2

    if main_pic is None or origin_type == 0:
        return main_pic

    gt_part = None
    det_part = None
    if gts is not None:
        # 真值框开启文字大小自适应
        main_pic, gt_part = draw_pic(main_pic, gts, font_path, font_size, 'red', font_size_adaptive)
    if dets is not None:
        # 检测框不开启自适应
        main_pic, det_part = draw_pic(main_pic, dets, font_path, font_size, 'green', font_size_adaptive)

    result = main_pic
    if gt_part is not None:
        result = combine(gt_part, result)
    if det_part is not None:
        result = combine(result, det_part)

    if origin_type == 2:
        result = cv2.cvtColor(np.asarray(result), cv2.COLOR_RGB2BGR)

    return result

# 将两张图合到一张图上
def combine(left_img, right_img):
    w1, h1 = left_img.size
    w2, h2 = right_img.size
    canvas = Image.new('RGB', (w1 + w2, max(h1, h2)), (255, 255, 255))
    canvas.paste(left_img, (0, 0, w1, h1))
    canvas.paste(right_img, (w1, 0, w1 + w2, h2))
    return canvas

def draw_pic(img, tuples, font_path, font_size, color='red', size_fit_area=False):
    draw = ImageDraw.Draw(img)
    contrast = Image.new('RGB', img.size, (255, 255, 255))
    contrast_draw = ImageDraw.Draw(contrast)

    for index in range(len(tuples)):
        rectangle = tuples[index][0]
        content = tuples[index][1]
        draw_polygon_from_draw(draw, rectangle, width=2, fill=color)
        if font_size < 0:
            font_size = 18
        font = ImageFont.truetype(font_path, font_size)
        # 文字大小适配检测框（按文字区域高度）
        if size_fit_area:
            area_height = min(rectangle[7] - rectangle[1], rectangle[5] - rectangle[3])
            area_height = max(area_height, - area_height)
            new_font_size = min(int(area_height * 0.752812499999996), 40)
            font = ImageFont.truetype(font_path, new_font_size)
        contrast_draw.text((rectangle[0], rectangle[1]), text=content, fill=(0, 0, 0), font=font)
    contrast_draw.text((img.size[0] / 2 - 10, 0), text="〇", fill=color, font=ImageFont.truetype(font_path, 26))
    return img, contrast

import base64
import os

def get_file_binary(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def get_file_base64(filePath):
    b64 = base64.b64encode(get_file_binary(filePath))
    return str(b64, 'utf-8')

def walk_dir(dir_path):
    res = []
    for fp, fd, fs in os.walk(dir_path):
        for f in fs:
            res.append(os.path.join(fp, f))
    return res

def split_file(filepath):
    p, filename = os.path.split(filepath)
    fn, ext = os.path.splitext(filename)
    return p, fn, ext

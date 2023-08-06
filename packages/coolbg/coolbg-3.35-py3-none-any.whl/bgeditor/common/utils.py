import requests
import os
import tempfile
import uuid
from gbackup import Client
import numpy as np
def upload_file(path):
    public_folder_id = "1kl75TP6zJiuFBdjhJUw1GHhdcIEjueoE"
    file_name = os.path.basename(path)
    return Client("/u02/drive_config/public_config/coca_idrive.json", "upload", path, "").upload_file(file_name,path, public_folder_id)
def download_gdrive(id,path):
    Client("/u02/drive_config/public_config/coca_idrive.json", "download", path, "").download_file(id,path)
def download_file(url, root_dir=None, ext= None):
    rs = None
    try:
        if ext:
            file_name = str(uuid.uuid4()) + "." + ext
        else:
            file_name = os.path.basename(url)
        if not root_dir:
            rs = get_dir('download') + file_name
        else:
            rs = root_dir + "/" + file_name
        if "gdrive" in url:
            download_gdrive(url.split(";;")[-1],rs)
        else:
            r = requests.get(url)
            with open(rs, 'wb') as f:
                f.write(r.content)
    except:
        rs = None
        pass
    return rs
def cache_file(url):
    rs = None
    try:
        rs = get_dir('cached') + os.path.basename(url)
        if os.path.exists(rs):
            return rs #cached
        r = requests.get(url)
        with open(rs, 'wb') as f:
            f.write(r.content)
    except:
        rs = None
        pass
    return rs

def get_dir(dir):
    tmp_download_path = tempfile.gettempdir() + "/"+dir+"/"
    if not os.path.exists(tmp_download_path):
        os.makedirs(tmp_download_path)
    return tmp_download_path
def hex_to_rgb(hex_string):
    return np.array(list(int(hex_string.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)))

def change_color_alpha(img, hex_color):
    rgb_color = hex_to_rgb(hex_color)
    alpha_arr = img[:,:,3]
    new_img = np.zeros( (100, 100, 4), dtype='uint8')
    shape_alpha= np.shape(alpha_arr)
    for i in range(shape_alpha[0]):
        for j in range(shape_alpha[1]):
            if alpha_arr[i, j] != 0:
                new_img[i, j, 0] = rgb_color[0]
                new_img[i, j, 1] = rgb_color[1]
                new_img[i, j, 2] = rgb_color[2]
                new_img[i, j, 3] = alpha_arr[i, j]
    return new_img


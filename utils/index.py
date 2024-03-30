# 获得根路径
import os
import re


def get_root_path():
    # 获取文件目录
    cur_path = os.path.abspath(os.path.dirname(__file__))
    par_path = os.path.dirname(cur_path)
    # 获取项目根路径，内容为当前项目的名字
    root_path = par_path
    return root_path


def address_conversion(url: str, num: int):
    urls = []
    for i in range(num):
        address = url.replace('_p0', f'_p{i}')
        urls.append(
            f'https://i.pximg.net/img-original{address[address.find('/img/'):address.find('_custom1200.jpg')]}.jpg' if address.find(
                '_custom1200.jpg') > -1 else f'https://i.pximg.net/img-original{address[address.find('/img/'):address.find('_square1200.jpg')]}.jpg')

    return urls


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")


def name_processing(name: str, replace=''):
    return re.sub(re.compile('[/\\\\:*?"<>|]')
                  , replace,
                  name
                  )

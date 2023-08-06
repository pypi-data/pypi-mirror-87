# coding=utf-8

# @Time: 2020/3/5 10:57
# @Auther: liyubin

from PIL import Image
import math
import operator
from functools import reduce
import base64

"""
check photo
"""


def resize_photo(filename):
    """
    resize photo
    :param filename:
    :return:
    """
    img = Image.open(filename)
    width = img.size[0]
    height = img.size[1]
    region = img.resize((int(width * 0.5), int(height * 0.5)), Image.ANTIALIAS)
    region.save(filename)


def base64_photo(filename, resize=False):
    """
    photo base64
    :param filename:
    :return:
    """
    if resize:
        resize_photo(filename)
    with open(filename, 'rb')as fp:
        base64_data = 'data:image/png;base64,' + base64.b64encode(fp.read()).decode()
    return base64_data


def compare(pic1, pic2):
    """
    :param pic1: file1
    :param pic2: file2
    :return: differ
    """
    image1 = Image.open(pic1)
    image2 = Image.open(pic2)

    histogram1 = image1.histogram()
    histogram2 = image2.histogram()

    differ = math.sqrt(
        reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, histogram1, histogram2))) / len(histogram1))

    print(differ)
    return differ


if __name__ == '__main__':

    differ = compare(r'./1.png', r'./2.png')
    if differ == 0.0:
        print('ok: ', differ)
    elif differ < 3.16:
        print('小于3.16: ', differ)
    else:
        print('fail: ', differ)



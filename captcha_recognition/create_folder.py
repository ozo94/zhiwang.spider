# coding=utf-8
from PIL import Image, ImageDraw, ImageChops
import os
from pretreat_img import *
from cut_img import *


# 生成存放样本的文件夹
def new_char_folder():
    # 0-9
    for k in range(48, 58):
        try:
            os.mkdir('../img/%c' % k)
        except:
            pass

    # A-Z
    for k in range(65, 91):
        try:
            os.mkdir('../img/%c' % k)
        except:
            pass


# 生成样本字符,然后手动将对应字符移动到上面生成的文件夹中
# 每个文件夹手动移动10个以上
def new_char_example():
    new_char_folder()
    for s in range(300):
        image = Image.open('../img/raw/%d.gif' % s)
        image = pretreat_image(image)

        image.save('../img/%d.png' % s)
        image_char_list = cut_all_char(image)
        for k in range(5):
            image_char_list[k].save('../img/%d_%d.png' % (s, k))


if __name__ == '__main__':
    new_char_example()
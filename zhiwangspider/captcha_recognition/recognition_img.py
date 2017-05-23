# coding=utf-8

from PIL import Image,ImageDraw,ImageChops
import os
from pretreat_img import *
from cut_img import *
from load_img import *

def  compare2imbw(imbw1,imbw2):
    #out = abs(imbw1, imbw2) 相同的点变为0,不同的变为255
    image = ImageChops.difference(imbw1,imbw2)
    # 统计相同的点的个数
    # 直方图统计,返回长度为256的list
    a = image.histogram()
    # a = image.getbbox()
    same_pixel = a[0]

    Width,Height=imbw1.size
    all_pixel = Width*Height
    res =  same_pixel/float(all_pixel)
    return res


# 与样本比较,设置一个评分体系
# 分别取最大的?个相似度相加,再取最大的对应的字符

def distinguish_one_char(char_example,image_char):
    global char_set
    score_set=[]
    for image_list in char_example:
        score_set.append([])
        for image in image_list:
            score_set[-1].append( compare2imbw(image,image_char) )

    # 对于score_set[k],取分值最高的5个相加
    char_num=len(char_set)
    for k in range(char_num):
        # 从小到大排序
        score_set[k].sort()
        # 逆序
        score_set[k].reverse()

        # 调试打印节点1
        # print(char_set[k],score_set[k][0:1])

        # 取前5
        score_set[k] = score_set[k][0:1]
        # 前5相加,保存在score_set[k]中
        score_set[k] = sum(score_set[k])

    # 获得相似度最大的字符,并返回
    # index 返回找到的第一个值的位置
    a = score_set.index( max(score_set) )

    # 调试打印节点2
    # print(char_set[a])
    return char_set[a]

def distinguish_all_char(char_example,image_char_list):
    s = ""
    for image_char in image_char_list:
        # image_char.show()
        s += distinguish_one_char(char_example,image_char)
    return s

def distinguish_captcha(image):
    # 预处理图片,返回0/255二值图像
    img = pretreat_image(image)
    # 切割二值图像
    image_char_list = cut_all_char(img)

    # 加载样本数据
    char_example = load_char_example()

    # 比对识别各个字符
    result = distinguish_all_char(char_example,image_char_list)
    return result

if __name__ == '__main__':
    for i in range(30):
        image = Image.open('../img/test/%d.gif' %i)
        s = distinguish_captcha(image)
        print(s)



# coding=utf-8
from PIL import Image,ImageDraw,ImageChops
import os


# 验证码预处理,主要是降噪
# 预处理结束后返回0/255二值图像
# 降噪
def pretreat_image(image):
    image = image.resize((126,44))
    # 将图片转换成灰度图片
    image = image.convert("L")
    # 二值化,得到0/255二值图片
    # 阀值threshold = 180
    image = iamge2imbw(image,120)
    # 对二值图片进行降噪
    # N = 4
    clear_noise(image,4)
    # 去除外边框
    # 原图大小:63*22
    # 左上右下,左 <= x < 右
    box = (   10,   4,  120,  40 )
    image = image.crop(box)
    return image

# 灰度图像二值化,返回0/255二值图像
def iamge2imbw(image,threshold):
    # 设置二值化阀值
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    # 像素值变为0,1
    image = image.point(table,'1')
    # 像素值变为0,255
    image = image.convert('L')
    return image
# 根据一个点A的灰度值(0/255值),与周围的8个点的值比较
# 降噪率N: N=1,2,3,4,5,6,7
# 当A的值与周围8个点的相等数小于N时,此点为噪点
# 如果确认是噪声,用该点的上面一个点的值进行替换
def get_near_pixel(image,x,y,N):
    pix = image.getpixel((x,y))

    near_dots = 0
    if pix == image.getpixel((x - 1,y - 1)):
        near_dots += 1
    if pix == image.getpixel((x - 1,y)):
        near_dots += 1
    if pix == image.getpixel((x - 1,y + 1)):
        near_dots += 1
    if pix == image.getpixel((x,y - 1)):
        near_dots += 1
    if pix == image.getpixel((x,y + 1)):
        near_dots += 1
    if pix == image.getpixel((x + 1,y - 1)):
        near_dots += 1
    if pix == image.getpixel((x + 1,y)):
        near_dots += 1
    if pix == image.getpixel((x + 1,y + 1)):
        near_dots += 1

    if near_dots < N:
        # 确定是噪声,用上面一个点的值代替
        return image.getpixel((x,y-1))
    else:
        return None

# 降噪处理
def clear_noise(image,N):
    draw = ImageDraw.Draw(image)

    # 外面一圈变白色
    Width,Height=image.size
    for x in range(Width):
        draw.point((x,0),255)
        draw.point((x,Height-1),255)
    for y in range(Height):
        draw.point((0,y),255)
        draw.point((Width-1,y),255)

    # 内部降噪
    for x in range(1,Width - 1):
        for y in range(1,Height - 1):
            color = get_near_pixel(image,x,y,N)
            if color != None:
                draw.point((x,y),color)

if __name__ == '__main__':
     for i in range(10):
        image = Image.open('../img/raw/%d.gif' %i)
        image = pretreat_image(image)
        image.show()
import os
import PIL.Image as Image
import numpy as np
import time

def rgb2gray(rgbfile, pngfile):
    I = Image.open(rgbfile)
    # I.show()
    L = I.convert('L')
    # L.show()
    L.save(pngfile)


def replace_color(img, src_clr, dst_clr):
    ''' 通过矩阵操作颜色替换程序
    @param	img:	图像矩阵
    @param	src_clr:	需要替换的颜色(r,g,b)
    @param	dst_clr:	目标颜色		(r,g,b)
    @return				替换后的图像矩阵
    '''

    img_arr = np.asarray(img, dtype=np.double)

    r_img = img_arr[:, :, 0].copy()
    g_img = img_arr[:, :, 1].copy()
    b_img = img_arr[:, :, 2].copy()

    img = r_img * 256 * 256 + g_img * 256 + b_img
    src_color = src_clr[0] * 256 * 256 + src_clr[1] * 256 + src_clr[2]  # 编码

    r_img[img == src_color] = dst_clr[0]
    g_img[img == src_color] = dst_clr[1]
    b_img[img == src_color] = dst_clr[2]

    dst_img = np.array([r_img, g_img, b_img], dtype=np.uint8)
    dst_img = dst_img.transpose(1, 2, 0)

    return dst_img


# 遍历文件夹
def walkFile(rgbpath, graypath):
    list = [];
    for root, dirs, files in os.walk(rgbpath):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            if f.endswith(".png") or f.endswith(".tif"):

                #to do 这里默认选择白色替换成(1，1，1)仅替换一次, 以后应该遍历所有颜色，从(0,0,0)开始重新赋值(1,1,1)、(2,2,2)递增
                img = Image.open(os.path.join(root, f)).convert('RGB')
                res_img = img.copy()
                dst_img = replace_color(img, (255, 255, 255), (1, 1, 1))
                res_img = dst_img
                res_img = Image.fromarray(res_img)
                res_img.save(os.path.join(graypath, f))


                rgb2gray(os.path.join(graypath, f), os.path.join(graypath, f))


if __name__ == "__main__":
    tifpath = input("plase input rgb forder path,eg: E:\\ai\\rgb_images\n")
    pngpath = input("plase input gray forder path,eg: E:\\ai\\gray_images\n")
    print('is running...')
    walkFile(tifpath, pngpath)
    print('finish')

import os
import PIL.Image as Image


def rgb2gray(rgbfile, pngfile):
    I = Image.open(rgbfile)
    # I.show()
    L = I.convert('L')
    # L.show()
    L.save(pngfile)


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
                rgb2gray(os.path.join(root, f), os.path.join(graypath, f))


if __name__ == "__main__":
    tifpath = input("plase input rgb forder path,eg: E:\\ai\\rgb_images\n")
    pngpath = input("plase input gray forder path,eg: E:\\ai\\gray_images\n")
    print('is running...')
    walkFile(tifpath, pngpath)
    print('finish')

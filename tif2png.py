#注意有写图片转不成功要报错，大小为0，要手动把对应的image和label都删掉
from osgeo import gdal
import os
import PIL.Image as Image

def tifFile2PngFile(tiffile, pngfile):
    file_path=tiffile
    ds=gdal.Open(file_path)
    driver=gdal.GetDriverByName('PNG')
    dst_ds = driver.CreateCopy(pngfile, ds)
    if dst_ds == None:
        print('error:'+tiffile)
    dst_ds = None
    src_ds = None

# 遍历文件夹
def walkFile(tifpath, pngpath):
    list = [];
    for root, dirs, files in os.walk(tifpath):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            if f.endswith(".tif"):
                name = os.path.splitext(f)[0]
                tifFile2PngFile(os.path.join(root, f),os.path.join(pngpath, name+'.png'))

if __name__ == "__main__":
    tifpath = input("plase input tif forder path,eg: E:\\ai\\tif_images\n")
    pngpath = input("plase input png forder path,eg: E:\\ai\\png_images\n")
    print('is running...')
    walkFile(tifpath, pngpath)
    print('finish')
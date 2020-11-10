from osgeo import gdal
import os
import numpy as np
import cv2
import PIL.Image as Image

'''
input:原图的tif文件和预测的单通道png图像
out:合成新的tif,带有坐标信息
'''


class GRID:
    # 读图像文件
    def read_img(self, filename):
        dataset = gdal.Open(filename)  # 打开文件

        im_width = dataset.RasterXSize  # 栅格矩阵的列数
        im_height = dataset.RasterYSize  # 栅格矩阵的行数

        im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
        im_proj = dataset.GetProjection()  # 地图投影信息
        im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 将数据写成数组，对应栅格矩阵

        del dataset  # 关闭对象，文件dataset
        return im_proj, im_geotrans, im_data, im_width, im_height

    # 写文件，以写成tif为例
    def write_img(self, filename, im_proj, im_geotrans, im_data):

        # 判断栅格数据的数据类型
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

        # 判读数组维数
        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        else:
            im_bands, (im_height, im_width) = 1, im_data.shape

        # 创建文件
        driver = gdal.GetDriverByName("GTiff")  # 数据类型必须有，因为要计算需要多大内存空间
        dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影

        if im_bands == 1:
            dataset.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
        else:
            for i in range(im_bands):
                dataset.GetRasterBand(i + 1).WriteArray(im_data[i])

        del dataset

    # 读图像文件
    def doTiff(self, path, referencepath, outpath, name):

        os.chdir(referencepath)  # 切换路径到待处理图像所在文件夹
        run = GRID()
        # 第一步
        proj, geotrans, data1, row1, column1 = run.read_img(name+'.tif')  # 读数据,获取tif图像的信息

        os.chdir(path)  # 切换路径到待处理图像所在文件夹
        img_path = name+'.png'  # 读取png图像数据
        data2 = cv2.imread(img_path, 0) #1:彩色，0：灰度，-1：alaph

        data = np.array((data2), dtype=data1.dtype)  # 数据格式
        run.write_img(os.path.join(outpath,name+'.tif'), proj, geotrans, data)  # 生成tif

# 遍历文件夹
def walkFile(path, referencepath, outpath):
    run = GRID()
    list = [];
    for root, dirs, files in os.walk(path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            if f.endswith(".png"):
                im = Image.open(os.path.join(root,f))
                name = os.path.splitext(f)[0]
                run.doTiff(path,referencepath,outpath,name)
                # im.save(os.path.join(outpath,name+'.tif'))  # or 'test.tif'

if __name__ == "__main__":
    path = input("plase input png path,eg: E:\\ai\\png_images\n")
    referencepath = input("plase input reference tif path,eg: E:\\ai\\ref_images\n")
    outpath = input("plase input tif outpath,eg: E:\\ai\\out_images\n")
    print('is running...')
    walkFile(path, referencepath, outpath)
    print('finish')




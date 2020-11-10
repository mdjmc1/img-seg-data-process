import numpy as np
import gdal
import os
import sys
from  multiprocessing import Pool

NP2GDAL_CONVERSION = {
  "uint8": 1,
  "int8": 1,
  "uint16": 2,
  "int16": 3,
  "uint32": 4,
  "int32": 5,
  "float32": 6,
  "float64": 7,
  "complex64": 10,
  "complex128": 11,
}
def split(rasterpath,outpath,dex,i, j,size,lap,cols,rows,gdaltype,datatype,gt,proj,nodata):
    dataset = gdal.Open(rasterpath)
    if (i+size > cols) | (j+size>rows):
        #x向越界
        if (i+size > cols) & (j+size<=rows):
            data0 = dataset.GetRasterBand(1).ReadAsArray(i,j, cols-i,size)
        #y向越界
        elif (i+size <= cols) & (j+size>rows):
            data0 = dataset.GetRasterBand(1).ReadAsArray(i , j, size,rows-j)
        #xy方向均越界
        else:
            #print(cols-i*size,rows-j*size)
            data0 = dataset.GetRasterBand(1).ReadAsArray(i , j , cols-i,rows-j)
    else:
        data0 = dataset.GetRasterBand(1).ReadAsArray(i, j , size,size)
    #如果第一个波段的最大值等于最小值，认为是无效值，不对其创建分片
    if data0.max() == data0.min():
        return

    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    bandsNum = dataset.RasterCount
    basename = os.path.basename(rasterpath)
    newbasename = basename[:basename.rfind(".")]
    dirpath = os.path.dirname(rasterpath)
    dst_ds = driver.Create(outpath + newbasename+'_%s%s.tif' % (dex[int(i/(size-lap))], dex[int(j/(size-lap))]), size, size, bandsNum, gdaltype)
    gtnew = (gt[0] + i  * gt[1], gt[1], gt[2], gt[3] + j * gt[5], gt[4], gt[5])
    dst_ds.SetGeoTransform(gtnew)
    dst_ds.SetProjection(proj)
    for k in range(bandsNum):
        if (i+size > cols) | (j+size>rows):
            # x向越界
            if (i+size > cols) & (j+size<=rows):
                data2 = dataset.GetRasterBand(k+1).ReadAsArray(i , j , cols - i , size)
            # y向越界
            elif (i+size <= cols) & (j+size>rows):
                data2 = dataset.GetRasterBand(k+1).ReadAsArray(i , j , size, rows - j )
            # xy方向均越界
            else:
                data2 = dataset.GetRasterBand(k+1).ReadAsArray(i , j , cols - i , rows - j )
            smally,smallx=data2.shape
            if nodata==None:
                data1=np.zeros((size,size),dtype=datatype)
            else:
                data1 = np.ones((size, size), dtype=datatype)*nodata
            data1[0:smally,0:smallx]=data2

        else:
            data1=dataset.GetRasterBand(k+1).ReadAsArray(i,j,size,size)

        dst_ds.GetRasterBand(k+1).WriteArray(data1)
        if nodata != None:
            dst_ds.GetRasterBand(k + 1).SetNoDataValue(nodata)
    dataset=None
    dst_ds=None

if __name__=="__main__":
    args=sys.argv
    try:
        rasterpath = args[1]
        outpath = args[2]
        parelle = int(args[3])
        # 分片的像元行列数，输出为正方形的
        size = int(args[4])
        lap=int(args[5])
    except:
        print("""Usage:python 此文件的路径 栅格路径 输出文件夹 并行度 输出图像的行列数 重叠像元数\nUsage:python ./splitImage.py  aa.tif ./output 8 1024 10""")
        raise


    # 区分每块的位置，000到999
    dex = ["%.3d" % i for i in range(1000)]

    if not os.path.exists(outpath):
        os.makedirs(outpath)
    if not outpath.endswith(os.path.sep):
        outpath = outpath + os.path.sep
    dataset=gdal.Open(rasterpath)
    proj=dataset.GetProjection()
    gt=dataset.GetGeoTransform()
    datatype=dataset.GetRasterBand(1).ReadAsArray(0,0,1,1).dtype.name
    #获取无效值，认为每个波段的无效值是相同的
    nodata=dataset.GetRasterBand(1).GetNoDataValue()
    #numpy的数据类型，转换为gdal的数据类型
    gdaltype=NP2GDAL_CONVERSION[datatype]
    #总行列数
    cols,rows=dataset.RasterXSize,dataset.RasterYSize
    dataset=None
    #获取分片的行数和列数
    numx=int(np.ceil((cols-size)/(size-lap)+1))
    numy=int(np.ceil((rows-size)/(size-lap)+1))

    #numx,numy=int(np.ceil(cols/size)),int(np.ceil(rows/size))

    pool = Pool(parelle)
    numxs=[(size-lap)*(i-1) for i in range(1,numx+1)]
    numys = [(size - lap) * (i - 1) for i in range(1, numy + 1)]
    #直接传入左上角的索引
    for i in numxs:
        for j in numys:
            pool.apply_async(split, args=(rasterpath,outpath,dex,i, j,size,lap,cols,rows,gdaltype,datatype,gt,proj,nodata))
    pool.close()
    pool.join()


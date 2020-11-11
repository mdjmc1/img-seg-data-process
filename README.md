# 图像语义分割数据处理步骤
## 安装环境：
* nodejs、conda、国内源配置
* 最好创建一个单独的conda环境，用conda安装gdal、opencv-python依赖
## 影像切割
### 1. 把tif文件的边长，按照512或1024的整数倍进行裁切(arcgis中做)
在arcmap打开tif影像，右键->data->export data->raster size(colouns,rows)
修改成512/1024的整数倍。保存导出
### 2. 切tif瓦片
这里使用splitImageMuti.py(多进程版）进行影像切割
输入切割前大tif路径，输入小tif输出目录

eg:E:\split\images\test.tif;E:\split\tiles

## 生成预测txt
获取目录中影像文件存入txt
调用createInferenceTxt.py，输入参数为瓦片目录

## 分类结果合并
### 1. 把png结果转成tif格式
这里png转tif用到png2tif.py
参数为：png目录;参考tif目录（源影像小瓦片目录）;输出小瓦片目录

eg:
E:\project\ai\PaddleSeg\visual_yzc_256
E:\project\ai\PaddleSeg\dataset\yzx_cuntun_png_tif\images
E:\project\ai\PaddleSeg\visual_yzc_256_tif2
### 2. 合并tif为一张图
用到mergeImage.py、gdal_merge_my.py *(根据gdal_merge.py修改而来，解决文件名过长问题)*    
执行mergeImage.py，参数为小瓦片目录、合成后tif文件路径

eg:
E:\project\ai\PaddleSeg\visual_yzc_256_tif2
E:\project\ai\PaddleSeg\visual_merge\visual_yzc_256.tif


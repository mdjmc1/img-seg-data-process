# 图像语义分割数据处理步骤
本文档为paddleseg的数据处理操作说明，是我个人的学习笔记，供大家参考

本文涵盖训练数据的处理、预测数据的处理、生成结果的处理三个方面，记录了处理流程、注意事项

## 安装环境：
* nodejs、conda、国内源配置
* 最好创建一个单独的conda环境，用conda安装gdal、opencv-python依赖
## 影像切割

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

## 注意事项：
1. 标签必须是灰度，不能是rgb。
2. tif转png可能会有转错的，要把错误的影像和相应的标签都删掉。
3. 生成的标签txt中要用正斜杠替换反斜杠，不然会报错
4. 标签的分类和代码中NUM_CLASSES的数要对应。如果只分割建筑，则NUM_CLASSES=2
5. 标签的分类必须从0开始依次递增，不能跳跃随便写
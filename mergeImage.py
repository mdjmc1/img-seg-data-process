import os
import sys
# args=sys.argv
# if len(args)!=4:
#     print("usage:python thispy folder_path outtif nodata")
#     sys.exit(1)
# path=args[1]
# outtif=args[2]
# nodata=eval(args[3])

# path='E:\\split\\切片'
# outtif='E:\\split\\合并后\\out.tif'


def main():
    path = input("plase input path,eg: E:\\split\\tiles \n")
    outtif = input("plase input outtif,eg: E:\\split\\images\\out.tif \n")

    if not path or not outtif:
        print("error:请输入正确的path和outtif")
        exit()
    nodata=0

    tifs=[os.path.join(path,i) for i in os.listdir(path) if i.endswith(".tif")]

    # print(tifs)
    #将 gdal_merge.py复制到当前目录下
    # os.system("python gdal_merge_my.py -init %s -n %s -a_nodata %s -o %s %s"%(nodata,nodata,nodata,outtif," ".join(tifs)))
    os.system("python gdal_merge_my.py -init 0 -n 0 -a_nodata 0 -o %s  %s\*.tif"%(outtif,path))

    # os.system("node -v")

if __name__=="__main__":
    main()

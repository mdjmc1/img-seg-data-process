import numpy as np
import os
import sys

# 遍历文件夹
def walkFile(file):
    list = [];
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            # 当前文件的父路径
            forder = root[root.rindex('\\') + 1: len(root)]
            rPath = os.path.join(forder, f).replace('\\', '/')
            list.append(rPath)
        file_path_txt = os.path.join(os.getcwd(),'detection.txt')
        with open(file_path_txt, "w") as f:
            line = ''
            for item in list:
                try:
                    line = item + '\n'
                except:
                    line = item + '\n'

                f.write(line)
        # # 遍历所有的文件夹
        # for d in dirs:
        #     print(os.path.join(root, d))


def main():
    path = input("plase input tiles path,eg: E:\\ai\\images\n")
    walkFile(path)

if __name__=="__main__":
    main()


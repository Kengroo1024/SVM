import os
import re


'''
将txt数据转化为csv文件
'''


def format(folder_path: str, save_path: str) -> None:
    '''从folderPath目录下递归读取文件，转换为csv格式文件后储存至savePath
    '''

    cwd = os.getcwd()
    os.chdir(folder_path)

    for root, subdirs, files in os.walk("."):
        if not os.path.exists(os.path.join(cwd, save_path, root)):
            os.makedirs(os.path.join(cwd, save_path, root))
        for file in files:
            strg = str()
            with open(os.path.join(cwd, folder_path, root, file), "r") as f:
                for k in f.readlines()[9:]:
                    strg = strg + re.sub(';', ',', k)
            path = os.path.join(
                cwd, save_path, root, os.path.splitext(file)[0]+".csv")

            with open(path, "w") as f:
                f.write(strg)
    os.chdir(cwd)
    return None


if __name__ == '__main__':
    format("raw_data", "data_json")

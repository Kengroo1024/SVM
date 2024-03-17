import os
import re


'''
将txt数据转化为csv文件
'''


def format(folderPath: str, savePath: str) -> None:
    '''从folderPath递归读取文件，并储存至savePath
    '''

    cwd = os.getcwd()
    os.chdir(folderPath)

    for path, folders, files in os.walk("."):
        os.makedirs(os.path.join(cwd, savePath, path))
        for file in files:
            strg = str()
            with open(os.path.join(cwd, savePath, path, file), "r") as f:
                for k in f.readlines()[9:]:
                    strg = strg + re.sub(';', ',', k)
            save = os.path.join(
                cwd, savePath, path, os.path.splitext(file)[0]+".csv")

            with open(save, "w") as f:
                f.write(strg)
    os.chdir(cwd)
    return None


if __name__ == '__main__':
    format("raw_data", "data_cav")

import os
import re


'''
将txt数据转化为csv文件
'''

if __name__ == '__main__':
    os.chdir("raw_data")

    for tree in os.walk("."):
        os.makedirs(os.path.join(os.getcwd(), "data_csv", tree[0]))
        for file in tree[-1]:
            strg = str()
            with open(os.path.join(tree[0], file), "r") as f:
                for k in f.readlines()[9:]:
                    strg = strg + re.sub(';', ',', k)
            path = os.path.join(os.getcwd(), "data_csv",
                                tree[0], os.path.splitext(file)[0]+".csv")
            with open(path, "w") as f:
                f.write(strg)

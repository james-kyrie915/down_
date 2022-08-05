import tarfile
import time
import zipfile
import os
import sys

tar_path = r"""E:\Pycharm_file\Data_collection\para\decompress\tar"""
zip_path = r"""E:\Pycharm_file\Data_collection\para\decompress\zip"""


def tar_file():
    tar = tarfile.open('log1.tar.gz')
    # names = tar.getnames()
    # for name in names:
    #     tar.extract(name, tar_path)
    tar.extractall(path=tar_path)
    tar.close()


def zip_file():
    f = zipfile.ZipFile("log2.zip", 'r')
    f.extractall(path=zip_path)
    # for file in f.namelist():
    #     f.extract(file, zip_path)
    f.close()


begin = time.time()

a = "a/b/c/e/c/a/d/e/f"
words = a.split('/')
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(sorted(counts.items(), key=lambda x: x[1], reverse=True))
print(type(counts))
for key in counts:
    print(key)
    print(counts[key])
print(counts.items())
# zip_file()
# tar_file()


end = time.time()
print(end - begin)



import os

"""
删除缓存和数据文件
"""

dir = os.path.dirname(__file__)

for root, dirs, files in os.walk(dir):
    for file in files:  
        if file.endswith(".dat"):
            os.remove(os.path.join(root, file))
        if file.endswith(".pyc"):
            os.remove(os.path.join(root, file))

for root, dirs, files in os.walk(dir):
    for dir in dirs:
        if dir == "__pycache__":
            os.removedirs(os.path.join(root, dir))
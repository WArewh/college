import os

def clear(dir):
    """
    删除缓存和数据文件
    """
    for root, dirs, files in os.walk(work_dir):
        for file in files:  
            if file.endswith(".dat"):
                os.remove(os.path.join(root, file))
            if file.endswith(".pyc"):
                os.remove(os.path.join(root, file))

    for root, dirs, files in os.walk(work_dir):
        for dir in dirs:
            if dir == "__pycache__":
                os.removedirs(os.path.join(root, dir))

utils_dir = os.path.dirname(__file__)
work_dir = os.path.dirname(utils_dir)
clear(work_dir)

import os
import urllib.request

def download_file(url: str, save: str) -> None:
    """
    下载指定文件

    参数:
        url (str): 下载链接
        save (str): 本地存储路径(绝对路径)
    """
    
    if not os.path.exists(save):
        urllib.request.urlretrieve(url, save)
    

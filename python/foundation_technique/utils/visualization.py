import matplotlib.pyplot as plt

def plot_histogram(
    x: list,
    num: int=-1,
    title: str="",
    xlabel: str="",
    ylabel: str=""
    ) -> None:
    """
    直方图
    
    参数:
        x (list): 横轴数据
        num (int ,optional): 图表标识符，-1表示创建新的窗口
        title (string ,optional): 标题
        xlabel (string ,optional): x轴名称
        ylabel (string ,optional): y轴名称
    """
    if num == -1:
        plt.figure()
    else:
        plt.figure(num)
    
    plt.hist(x)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

def plot_curve(
    x: list,
    y: list,
    num: int=-1,
    label: str="",
    title: str="",
    xlabel: str="",
    ylabel: str=""
    ) -> None:
    """
    曲线
    
    参数:
        x (list): 横轴数据
        y (list): 竖轴数据
        num (int ,optional): 图表标识符，-1表示创建新的窗口
        label (string ,optional): 标签
        title (string ,optional): 标题
        xlabel (string ,optional): x轴名称
        ylabel (string ,optional): y轴名称
    """
    if num == -1:
        plt.figure()
    else:
        plt.figure(num)
    
    plt.plot(x, y, label=label)

    if label != "":
        plt.legend()

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

def plot_scatter(
    x: list,
    y: list,
    num: int=-1,
    label: str=""
    ) -> None:
    """
    散点图
    
    参数:
        x (list): 横轴数据
        y (list): 竖轴数据
        num (int ,optional): 图表标识符，-1表示创建新的窗口
        label (string ,optional): 标签
    """
    if num == -1:
        plt.figure()
    else:
        plt.figure(num)

    plt.scatter(x, y, label=label)

    if label != "":
        plt.legend()


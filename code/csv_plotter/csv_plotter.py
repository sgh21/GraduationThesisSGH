import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import CSS4_COLORS

def list_csv_files(folder_path):
    """列出指定文件夹中的所有CSV文件"""
    csv_files = []
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.lower().endswith('.csv'):
                csv_files.append(os.path.join(folder_path, file))
    return csv_files

def get_available_styles():
    """获取可用的matplotlib样式"""
    return plt.style.available

def get_available_colors():
    """获取可用的颜色列表"""
    return list(CSS4_COLORS.keys())

def read_csv_data(csv_file, x_col=1, y_col=2, skiprows=1, x_divisor=None):
    """
    读取CSV文件中的数据
    
    参数:
    - csv_file: CSV文件路径
    - x_col: X轴数据所在列索引
    - y_col: Y轴数据所在列索引
    - skiprows: 跳过的行数
    - x_divisor: X轴数据除数（例如将迭代次数转换为epoch）
    
    返回:
    - x_data, y_data: 处理后的X和Y轴数据
    """
    try:
        df = pd.read_csv(csv_file, header=None, skiprows=skiprows)
        x_data = df.iloc[1:, x_col].astype(float)
        y_data = df.iloc[1:, y_col].astype(float)
        
        # 如果指定了除数，将X轴数据除以该值
        if x_divisor and x_divisor > 0:
            x_data = x_data / x_divisor
            
        return x_data, y_data
    except Exception as e:
        print(f"读取CSV文件 {csv_file} 时出错: {str(e)}")
        return None, None

def smooth_data(data, window_size):
    """
    使用移动平均对数据进行平滑处理
    
    参数:
    - data: 需要平滑的数据
    - window_size: 平滑窗口大小
    
    返回:
    - 平滑后的数据
    """
    if window_size <= 1:
        return data
    
    # 转换为numpy数组
    data_array = np.array(data)
    
    # 使用卷积进行平滑
    weights = np.ones(window_size) / window_size
    # 使用 'same' 模式保持长度不变
    smoothed = np.convolve(data_array, weights, mode='same')
    
    # 处理边界
    # 在信号的开始和结束部分，窗口无法完全覆盖，需要特殊处理
    half_window = int(window_size / 2)
    
    # 左边界
    for i in range(half_window):
        window_end = min(i + half_window + 1, len(data_array))
        if i < window_end:
            smoothed[i] = np.mean(data_array[:window_end])
    
    # 右边界
    data_len = len(data_array)
    for i in range(data_len - half_window, data_len):
        if i >= 0:
            smoothed[i] = np.mean(data_array[max(0, i - half_window):])
    
    return smoothed

def plot_csv_data(csv_files, plot_config, output_folder=None):
    """
    绘制CSV数据并保存图像
    
    参数:
    - csv_files: CSV文件路径列表
    - plot_config: 绘图配置字典，包含样式、标题、标签等
    - output_folder: 输出文件夹，默认为CSV文件所在文件夹
    
    返回:
    - 生成的图像文件路径列表
    """
    if not csv_files:
        return []
    
    # 设置绘图样式
    try:
        plt.style.use(plot_config.get('style', 'default'))
    except Exception:
        plt.style.use('default')
    
    # 设置字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei'] + plt.rcParams['font.sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 自定义字体设置
    font_config = plot_config.get('font', {})
    font = {
        'family': font_config.get('family', 'serif'),
        'serif': font_config.get('serif', 'Times New Roman'),
        'weight': font_config.get('weight', 'normal'),
        'size': font_config.get('size', 12),
    }
    plt.rc('font', **font)
    
    # 创建图像文件路径列表
    generated_files = []
    
    # 处理每个CSV文件
    for i, csv_file in enumerate(csv_files):
        x_col = plot_config.get('x_col', 1)
        y_col = plot_config.get('y_col', 2)
        skiprows = plot_config.get('skiprows', 1)
        x_divisor = plot_config.get('x_divisor', None)
        
        # 读取数据
        x_data, y_data = read_csv_data(csv_file, x_col, y_col, skiprows, x_divisor)
        if x_data is None or y_data is None:
            continue
        
        # 如果需要平滑数据
        if plot_config.get('smooth', False) and plot_config.get('smooth_window', 1) > 1:
            window_size = int(plot_config.get('smooth_window', 3))
            y_data = smooth_data(y_data, window_size)
        
        # 创建图像
        fig_num = i + 1
        plt.figure(fig_num, figsize=plot_config.get('figsize', (8, 6)))
        
        # 获取颜色 - 支持为每个CSV单独指定颜色
        colors = plot_config.get('colors', ['blue', 'red', 'green', 'purple', 'orange'])
        file_colors = plot_config.get('file_colors', {})
        
        # 如果特定文件有指定颜色，使用该颜色；否则使用默认颜色列表
        color = file_colors.get(os.path.basename(csv_file), colors[i % len(colors)])
        
        # 绘制曲线
        plt.plot(x_data, y_data, 
                 color=color, 
                 linewidth=plot_config.get('linewidth', 2),
                 linestyle=plot_config.get('linestyle', '-'),
                 marker=plot_config.get('marker', None),
                 markersize=plot_config.get('markersize', 5))
        
        # 设置标题和标签
        if 'use_title' in plot_config and plot_config['use_title'] and 'title' in plot_config:
            if isinstance(plot_config['title'], list) and len(plot_config['title']) > i:
                plt.title(plot_config['title'][i])
            elif isinstance(plot_config['title'], str):
                # 从文件名中提取基本名称，用于标题
                base_name = os.path.basename(csv_file).split('.')[0]
                plt.title(f"{plot_config['title']} - {base_name}")
        
        plt.xlabel(plot_config.get('xlabel', 'X轴'))
        plt.ylabel(plot_config.get('ylabel', 'Y轴'))
        
        # 设置网格
        plt.grid(plot_config.get('grid', True), linestyle='--', alpha=0.7)
        
        # 设置坐标轴范围
        if 'xlim' in plot_config:
            plt.xlim(plot_config['xlim'])
        if 'ylim' in plot_config:
            plt.ylim(plot_config['ylim'])
            
        # 添加图例
        if 'legend' in plot_config:
            if isinstance(plot_config['legend'], list) and len(plot_config['legend']) > i:
                plt.legend([plot_config['legend'][i]])
            else:
                # 从文件名中提取基本名称，用于图例
                base_name = os.path.basename(csv_file).split('.')[0]
                plt.legend([base_name])
        
        # 调整布局
        plt.tight_layout()
        
        # 确定输出文件夹
        if not output_folder:
            output_folder = os.path.dirname(csv_file)
        
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # 确定输出文件名
        base_name = os.path.basename(csv_file).split('.')[0]
        output_file = os.path.join(output_folder, f"{base_name}_plot.{plot_config.get('format', 'png')}")
        
        # 保存图像
        plt.savefig(output_file, format=plot_config.get('format', 'png'), 
                   dpi=plot_config.get('dpi', 300), bbox_inches='tight')
        
        generated_files.append(output_file)
    
    # 显示所有图像
    if plot_config.get('show', True):
        plt.show()
    
    # 关闭所有图像
    plt.close('all')
    
    return generated_files

if __name__ == "__main__":
    # 简单测试
    folder_path = ".\experiments"
    csv_files = list_csv_files(folder_path)
    
    plot_config = {
        'style': 'seaborn-v0_8-whitegrid',
        'title': '训练曲线',
        'xlabel': 'epochs',
        'ylabel': '损失值',
        'colors': ['blue', 'red', 'green'],
        'linewidth': 2,
        'format': 'svg',
        'x_divisor': 1000,  # 将x轴数据除以1000
        'smooth': True,     # 开启平滑
        'smooth_window': 5, # 平滑窗口大小
        'font': {
            'family': 'serif',
            'serif': 'Times New Roman',
            'weight': 'normal',
            'size': 14,
        }
    }
    
    plot_csv_data(csv_files, plot_config)
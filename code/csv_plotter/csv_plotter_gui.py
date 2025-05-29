import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import csv_plotter
import threading

class CSVPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV 可视化工具")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # 初始化变量
        self.csv_files = []
        self.selected_colors = ["blue", "red", "green", "purple", "orange"]
        self.file_colors = {}  # 存储文件和颜色的映射关系

        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Microsoft YaHei", 10))
        self.style.configure("TLabel", font=("Microsoft YaHei", 10))
        self.style.configure("TCheckbutton", font=("Microsoft YaHei", 10))
        self.style.configure("TRadiobutton", font=("Microsoft YaHei", 10))
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建组件
        self.create_widgets()
        
    def create_widgets(self):
        # 创建选项卡
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建各选项卡框架
        self.file_frame = ttk.Frame(self.notebook, padding=10)
        self.style_frame = ttk.Frame(self.notebook, padding=10)
        self.axis_frame = ttk.Frame(self.notebook, padding=10)
        self.color_frame = ttk.Frame(self.notebook, padding=10)
        self.output_frame = ttk.Frame(self.notebook, padding=10)
        self.smooth_frame = ttk.Frame(self.notebook, padding=10)  # 新增平滑选项卡
        
        # 添加选项卡
        self.notebook.add(self.file_frame, text="文件选择")
        self.notebook.add(self.style_frame, text="样式设置")
        self.notebook.add(self.axis_frame, text="坐标轴设置")
        self.notebook.add(self.color_frame, text="颜色设置")
        self.notebook.add(self.smooth_frame, text="平滑设置")  # 新增平滑选项卡
        self.notebook.add(self.output_frame, text="输出设置")
        
        # 创建各选项卡内容
        self.create_file_tab()
        self.create_style_tab()
        self.create_axis_tab()
        self.create_color_tab()
        self.create_smooth_tab()  # 新增平滑选项卡内容
        self.create_output_tab()
        
        # 创建底部按钮
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_frame.pack(fill=tk.X, pady=10)
        
        self.btn_plot = ttk.Button(self.btn_frame, text="生成图表", command=self.plot_csv_files)
        self.btn_plot.pack(side=tk.RIGHT, padx=5)
        
        self.btn_reset = ttk.Button(self.btn_frame, text="重置设置", command=self.reset_settings)
        self.btn_reset.pack(side=tk.RIGHT, padx=5)
        
        # 创建状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def create_file_tab(self):
        # 文件夹选择
        folder_frame = ttk.Frame(self.file_frame)
        folder_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(folder_frame, text="CSV文件夹:").pack(side=tk.LEFT, padx=5)
        self.folder_var = tk.StringVar()
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var, width=50)
        self.folder_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.btn_browse = ttk.Button(folder_frame, text="浏览...", command=self.browse_folder)
        self.btn_browse.pack(side=tk.LEFT, padx=5)
        
        # CSV文件列表
        file_list_frame = ttk.LabelFrame(self.file_frame, text="CSV文件列表")
        file_list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建列表框和滚动条
        list_scroll = ttk.Scrollbar(file_list_frame)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(file_list_frame, selectmode=tk.EXTENDED, 
                                       yscrollcommand=list_scroll.set, font=("Microsoft YaHei", 9))
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        list_scroll.config(command=self.file_listbox.yview)
        
        # 文件操作按钮
        file_btn_frame = ttk.Frame(self.file_frame)
        file_btn_frame.pack(fill=tk.X, pady=5)
        
        self.btn_refresh = ttk.Button(file_btn_frame, text="刷新列表", command=self.refresh_file_list)
        self.btn_refresh.pack(side=tk.LEFT, padx=5)
        
        self.btn_select_all = ttk.Button(file_btn_frame, text="全选", command=self.select_all_files)
        self.btn_select_all.pack(side=tk.LEFT, padx=5)
        
        self.btn_deselect_all = ttk.Button(file_btn_frame, text="取消全选", command=self.deselect_all_files)
        self.btn_deselect_all.pack(side=tk.LEFT, padx=5)
        
        # 新增：为选中文件设置颜色按钮
        self.btn_set_file_color = ttk.Button(file_btn_frame, text="为选中文件设置颜色", command=self.set_file_color)
        self.btn_set_file_color.pack(side=tk.LEFT, padx=5)
        
        # 数据列设置
        col_frame = ttk.LabelFrame(self.file_frame, text="数据列设置")
        col_frame.pack(fill=tk.X, pady=10)
        
        # X列
        x_col_frame = ttk.Frame(col_frame)
        x_col_frame.pack(fill=tk.X, pady=5)
        ttk.Label(x_col_frame, text="X轴数据列索引:").pack(side=tk.LEFT, padx=5)
        self.x_col_var = tk.IntVar(value=1)
        ttk.Spinbox(x_col_frame, from_=0, to=100, textvariable=self.x_col_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Y列
        y_col_frame = ttk.Frame(col_frame)
        y_col_frame.pack(fill=tk.X, pady=5)
        ttk.Label(y_col_frame, text="Y轴数据列索引:").pack(side=tk.LEFT, padx=5)
        self.y_col_var = tk.IntVar(value=2)
        ttk.Spinbox(y_col_frame, from_=0, to=100, textvariable=self.y_col_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # 跳过行数
        skip_frame = ttk.Frame(col_frame)
        skip_frame.pack(fill=tk.X, pady=5)
        ttk.Label(skip_frame, text="跳过起始行数:").pack(side=tk.LEFT, padx=5)
        self.skiprows_var = tk.IntVar(value=1)
        ttk.Spinbox(skip_frame, from_=0, to=100, textvariable=self.skiprows_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # X轴除数
        divisor_frame = ttk.Frame(col_frame)
        divisor_frame.pack(fill=tk.X, pady=5)
        ttk.Label(divisor_frame, text="X轴数据除数:").pack(side=tk.LEFT, padx=5)
        self.x_divisor_var = tk.StringVar(value="1000")
        ttk.Entry(divisor_frame, textvariable=self.x_divisor_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(divisor_frame, text="(将迭代次数转换为 epochs，留空表示不使用)").pack(side=tk.LEFT, padx=5)
        
    def create_style_tab(self):
        # 绘图样式设置
        style_frame = ttk.LabelFrame(self.style_frame, text="绘图样式")
        style_frame.pack(fill=tk.X, pady=10)
        
        # 绘图样式下拉框
        style_select_frame = ttk.Frame(style_frame)
        style_select_frame.pack(fill=tk.X, pady=5)
        ttk.Label(style_select_frame, text="绘图样式:").pack(side=tk.LEFT, padx=5)
        
        self.style_var = tk.StringVar()
        self.style_combobox = ttk.Combobox(style_select_frame, textvariable=self.style_var, 
                                          values=csv_plotter.get_available_styles())
        self.style_combobox.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.style_var.set("seaborn-v0_8-whitegrid")
        
        # 线条设置
        line_frame = ttk.LabelFrame(self.style_frame, text="线条设置")
        line_frame.pack(fill=tk.X, pady=10)
        
        # 线宽
        width_frame = ttk.Frame(line_frame)
        width_frame.pack(fill=tk.X, pady=5)
        ttk.Label(width_frame, text="线宽:").pack(side=tk.LEFT, padx=5)
        self.linewidth_var = tk.DoubleVar(value=2.0)
        ttk.Spinbox(width_frame, from_=0.5, to=5.0, increment=0.5, textvariable=self.linewidth_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # 线型
        linestyle_frame = ttk.Frame(line_frame)
        linestyle_frame.pack(fill=tk.X, pady=5)
        ttk.Label(linestyle_frame, text="线型:").pack(side=tk.LEFT, padx=5)
        self.linestyle_var = tk.StringVar(value="-")
        ttk.Combobox(linestyle_frame, textvariable=self.linestyle_var, 
                    values=["-", "--", "-.", ":", "None"]).pack(side=tk.LEFT, padx=5)
        
        # 标记
        marker_frame = ttk.Frame(line_frame)
        marker_frame.pack(fill=tk.X, pady=5)
        ttk.Label(marker_frame, text="数据点标记:").pack(side=tk.LEFT, padx=5)
        self.marker_var = tk.StringVar(value="None")
        ttk.Combobox(marker_frame, textvariable=self.marker_var, 
                    values=["None", ".", "o", "v", "^", "<", ">", "s", "p", "*", "h", "H", "+", "x", "D"]).pack(side=tk.LEFT, padx=5)
        
        # 字体设置
        font_frame = ttk.LabelFrame(self.style_frame, text="字体设置")
        font_frame.pack(fill=tk.X, pady=10)
        
        # 字体家族
        font_family_frame = ttk.Frame(font_frame)
        font_family_frame.pack(fill=tk.X, pady=5)
        ttk.Label(font_family_frame, text="字体家族:").pack(side=tk.LEFT, padx=5)
        self.font_family_var = tk.StringVar(value="serif")
        ttk.Combobox(font_family_frame, textvariable=self.font_family_var, 
                    values=["serif", "sans-serif", "monospace"]).pack(side=tk.LEFT, padx=5)
        
        # 字体大小
        font_size_frame = ttk.Frame(font_frame)
        font_size_frame.pack(fill=tk.X, pady=5)
        ttk.Label(font_size_frame, text="字体大小:").pack(side=tk.LEFT, padx=5)
        self.font_size_var = tk.IntVar(value=14)
        ttk.Spinbox(font_size_frame, from_=8, to=24, textvariable=self.font_size_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # 是否显示网格
        grid_frame = ttk.Frame(self.style_frame)
        grid_frame.pack(fill=tk.X, pady=5)
        self.grid_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(grid_frame, text="显示网格", variable=self.grid_var).pack(side=tk.LEFT, padx=5)
        
    def create_axis_tab(self):
        # 坐标轴设置
        title_frame = ttk.LabelFrame(self.axis_frame, text="标题设置")
        title_frame.pack(fill=tk.X, pady=10)
        
        # 图表标题
        chart_title_frame = ttk.Frame(title_frame)
        chart_title_frame.pack(fill=tk.X, pady=5)
        ttk.Label(chart_title_frame, text="图表标题:").pack(side=tk.LEFT, padx=5)
        self.title_var = tk.StringVar(value="训练曲线")
        ttk.Entry(chart_title_frame, textvariable=self.title_var).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # X轴标签
        x_title_frame = ttk.Frame(title_frame)
        x_title_frame.pack(fill=tk.X, pady=5)
        ttk.Label(x_title_frame, text="X轴标签:").pack(side=tk.LEFT, padx=5)
        self.xlabel_var = tk.StringVar(value="epochs")
        ttk.Entry(x_title_frame, textvariable=self.xlabel_var).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Y轴标签
        y_title_frame = ttk.Frame(title_frame)
        y_title_frame.pack(fill=tk.X, pady=5)
        ttk.Label(y_title_frame, text="Y轴标签:").pack(side=tk.LEFT, padx=5)
        self.ylabel_var = tk.StringVar(value="损失值")
        ttk.Entry(y_title_frame, textvariable=self.ylabel_var).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 坐标轴范围设置
        range_frame = ttk.LabelFrame(self.axis_frame, text="坐标轴范围 (留空表示自动)")
        range_frame.pack(fill=tk.X, pady=10)
        
        # X轴范围
        x_range_frame = ttk.Frame(range_frame)
        x_range_frame.pack(fill=tk.X, pady=5)
        ttk.Label(x_range_frame, text="X轴范围:").pack(side=tk.LEFT, padx=5)
        ttk.Label(x_range_frame, text="最小值").pack(side=tk.LEFT, padx=5)
        self.xmin_var = tk.StringVar(value="")
        ttk.Entry(x_range_frame, textvariable=self.xmin_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(x_range_frame, text="最大值").pack(side=tk.LEFT, padx=5)
        self.xmax_var = tk.StringVar(value="")
        ttk.Entry(x_range_frame, textvariable=self.xmax_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Y轴范围
        y_range_frame = ttk.Frame(range_frame)
        y_range_frame.pack(fill=tk.X, pady=5)
        ttk.Label(y_range_frame, text="Y轴范围:").pack(side=tk.LEFT, padx=5)
        ttk.Label(y_range_frame, text="最小值").pack(side=tk.LEFT, padx=5)
        self.ymin_var = tk.StringVar(value="")
        ttk.Entry(y_range_frame, textvariable=self.ymin_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(y_range_frame, text="最大值").pack(side=tk.LEFT, padx=5)
        self.ymax_var = tk.StringVar(value="")
        ttk.Entry(y_range_frame, textvariable=self.ymax_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # 图例设置
        legend_frame = ttk.LabelFrame(self.axis_frame, text="图例设置")
        legend_frame.pack(fill=tk.X, pady=10)
        
        # 是否显示图例
        show_legend_frame = ttk.Frame(legend_frame)
        show_legend_frame.pack(fill=tk.X, pady=5)
        self.show_legend_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(show_legend_frame, text="显示图例", variable=self.show_legend_var).pack(side=tk.LEFT, padx=5)
        
        # 图例位置
        legend_loc_frame = ttk.Frame(legend_frame)
        legend_loc_frame.pack(fill=tk.X, pady=5)
        ttk.Label(legend_loc_frame, text="图例位置:").pack(side=tk.LEFT, padx=5)
        self.legend_loc_var = tk.StringVar(value="best")
        ttk.Combobox(legend_loc_frame, textvariable=self.legend_loc_var, 
                   values=["best", "upper right", "upper left", "lower left", "lower right", 
                           "right", "center left", "center right", "lower center", "upper center", "center"]).pack(side=tk.LEFT, padx=5)
    
    def create_color_tab(self):
        # 颜色设置
        color_list_frame = ttk.LabelFrame(self.color_frame, text="预设颜色列表")
        color_list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建选定颜色列表
        selected_color_frame = ttk.Frame(color_list_frame)
        selected_color_frame.pack(fill=tk.X, pady=5)
        ttk.Label(selected_color_frame, text="已选颜色:").pack(side=tk.LEFT, padx=5)
        
        self.selected_color_var = tk.StringVar(value=", ".join(self.selected_colors))
        ttk.Entry(selected_color_frame, textvariable=self.selected_color_var, state="readonly").pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 添加颜色按钮
        color_btn_frame = ttk.Frame(color_list_frame)
        color_btn_frame.pack(fill=tk.X, pady=5)
        
        self.btn_add_color = ttk.Button(color_btn_frame, text="添加颜色", command=self.add_color)
        self.btn_add_color.pack(side=tk.LEFT, padx=5)
        
        self.btn_reset_colors = ttk.Button(color_btn_frame, text="重置颜色", command=self.reset_colors)
        self.btn_reset_colors.pack(side=tk.LEFT, padx=5)
        
        # 创建颜色列表
        colors_frame = ttk.Frame(color_list_frame)
        colors_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        color_scroll = ttk.Scrollbar(colors_frame)
        color_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.color_listbox = tk.Listbox(colors_frame, selectmode=tk.SINGLE, 
                                    yscrollcommand=color_scroll.set, font=("Microsoft YaHei", 9))
        self.color_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        color_scroll.config(command=self.color_listbox.yview)
        
        # 填充颜色列表
        available_colors = csv_plotter.get_available_colors()
        for color in available_colors:
            self.color_listbox.insert(tk.END, color)
            
        # 创建颜色样例
        color_sample_frame = ttk.LabelFrame(self.color_frame, text="颜色预览")
        color_sample_frame.pack(fill=tk.X, pady=10)
        
        self.color_canvas = tk.Canvas(color_sample_frame, height=50, bg="white")
        self.color_canvas.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # 添加文件特定颜色区域
        file_color_frame = ttk.LabelFrame(self.color_frame, text="文件特定颜色")
        file_color_frame.pack(fill=tk.X, pady=10)
        
        # 显示已设置的文件颜色
        self.file_color_text = tk.Text(file_color_frame, height=5, font=("Microsoft YaHei", 9))
        self.file_color_text.pack(fill=tk.X, expand=True, padx=5, pady=5)
        self.file_color_text.config(state="disabled")
        
        # 重置文件颜色按钮
        file_color_btn_frame = ttk.Frame(file_color_frame)
        file_color_btn_frame.pack(fill=tk.X, pady=5)
        
        self.btn_reset_file_colors = ttk.Button(file_color_btn_frame, text="重置文件颜色", command=self.reset_file_colors)
        self.btn_reset_file_colors.pack(side=tk.LEFT, padx=5)
        
        # 绘制颜色示例 - 确保所有组件都创建完毕后再调用
        self.root.after(100, self.update_color_preview)
        
        # 双击颜色列表事件绑定
        self.color_listbox.bind("<Double-1>", self.on_color_double_click)
    
    def create_smooth_tab(self):
        # 平滑设置
        smooth_options_frame = ttk.LabelFrame(self.smooth_frame, text="数据平滑设置")
        smooth_options_frame.pack(fill=tk.X, pady=10)
        
        # 是否启用平滑
        enable_smooth_frame = ttk.Frame(smooth_options_frame)
        enable_smooth_frame.pack(fill=tk.X, pady=5)
        self.smooth_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(enable_smooth_frame, text="启用数据平滑", variable=self.smooth_var, 
                       command=self.toggle_smooth_options).pack(side=tk.LEFT, padx=5)
        
        # 平滑窗口大小设置
        window_size_frame = ttk.Frame(smooth_options_frame)
        window_size_frame.pack(fill=tk.X, pady=5)
        ttk.Label(window_size_frame, text="平滑窗口大小:").pack(side=tk.LEFT, padx=5)
        self.smooth_window_var = tk.IntVar(value=3)
        self.smooth_window_spinbox = ttk.Spinbox(
            window_size_frame, from_=2, to=50, textvariable=self.smooth_window_var, width=5)
        self.smooth_window_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 平滑说明
        smooth_info_frame = ttk.LabelFrame(self.smooth_frame, text="平滑算法说明")
        smooth_info_frame.pack(fill=tk.X, pady=10)
        
        smooth_info_text = "平滑算法使用移动平均法处理数据，使曲线更加平滑。\n\n" + \
                         "平滑窗口大小越大，曲线越平滑，但可能会丢失更多细节。\n" + \
                         "推荐窗口大小范围为3-10。\n\n" + \
                         "注意：平滑处理仅影响曲线的显示效果，不会修改原始数据。"
        
        ttk.Label(smooth_info_frame, text=smooth_info_text, justify="left").pack(padx=10, pady=10, anchor="w")
        
        # 初始状态禁用平滑窗口设置
        self.toggle_smooth_options()
        
    def create_output_tab(self):
        # 输出设置
        output_folder_frame = ttk.LabelFrame(self.output_frame, text="输出文件夹")
        output_folder_frame.pack(fill=tk.X, pady=10)
        
        # 使用原文件夹选项
        use_original_frame = ttk.Frame(output_folder_frame)
        use_original_frame.pack(fill=tk.X, pady=5)
        self.use_original_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(use_original_frame, text="使用原CSV文件所在文件夹", 
                       variable=self.use_original_var, command=self.toggle_output_folder).pack(side=tk.LEFT, padx=5)
        
        # 自定义输出文件夹
        custom_folder_frame = ttk.Frame(output_folder_frame)
        custom_folder_frame.pack(fill=tk.X, pady=5)
        ttk.Label(custom_folder_frame, text="自定义输出文件夹:").pack(side=tk.LEFT, padx=5)
        self.output_folder_var = tk.StringVar()
        self.output_folder_entry = ttk.Entry(custom_folder_frame, textvariable=self.output_folder_var, width=50, state="disabled")
        self.output_folder_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.btn_output_browse = ttk.Button(custom_folder_frame, text="浏览...", command=self.browse_output_folder, state="disabled")
        self.btn_output_browse.pack(side=tk.LEFT, padx=5)
        
        # 输出格式设置
        format_frame = ttk.LabelFrame(self.output_frame, text="输出格式")
        format_frame.pack(fill=tk.X, pady=10)
        
        format_select_frame = ttk.Frame(format_frame)
        format_select_frame.pack(fill=tk.X, pady=5)
        ttk.Label(format_select_frame, text="图像格式:").pack(side=tk.LEFT, padx=5)
        self.format_var = tk.StringVar(value="svg")
        ttk.Combobox(format_select_frame, textvariable=self.format_var, 
                    values=["png", "jpg", "svg", "pdf"]).pack(side=tk.LEFT, padx=5)
        
        # DPI设置
        dpi_frame = ttk.Frame(format_frame)
        dpi_frame.pack(fill=tk.X, pady=5)
        ttk.Label(dpi_frame, text="图像DPI (分辨率):").pack(side=tk.LEFT, padx=5)
        self.dpi_var = tk.IntVar(value=300)
        ttk.Spinbox(dpi_frame, from_=72, to=600, textvariable=self.dpi_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # 图像尺寸设置
        size_frame = ttk.LabelFrame(self.output_frame, text="图像尺寸 (英寸)")
        size_frame.pack(fill=tk.X, pady=10)
        
        # 宽度
        width_frame = ttk.Frame(size_frame)
        width_frame.pack(fill=tk.X, pady=5)
        ttk.Label(width_frame, text="宽度:").pack(side=tk.LEFT, padx=5)
        self.fig_width_var = tk.DoubleVar(value=8.0)
        ttk.Spinbox(width_frame, from_=1.0, to=20.0, increment=0.5, textvariable=self.fig_width_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # 高度
        height_frame = ttk.Frame(size_frame)
        height_frame.pack(fill=tk.X, pady=5)
        ttk.Label(height_frame, text="高度:").pack(side=tk.LEFT, padx=5)
        self.fig_height_var = tk.DoubleVar(value=6.0)
        ttk.Spinbox(height_frame, from_=1.0, to=20.0, increment=0.5, textvariable=self.fig_height_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # 是否显示图像
        show_frame = ttk.Frame(self.output_frame)
        show_frame.pack(fill=tk.X, pady=5)
        self.show_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(show_frame, text="绘图完成后显示图像", variable=self.show_var).pack(side=tk.LEFT, padx=5)
        
    def browse_folder(self):
        folder_path = filedialog.askdirectory(title="选择CSV文件所在文件夹")
        if folder_path:
            self.folder_var.set(folder_path)
            self.refresh_file_list()
    
    def refresh_file_list(self):
        folder_path = self.folder_var.get()
        if folder_path and os.path.exists(folder_path):
            self.file_listbox.delete(0, tk.END)
            csv_files = csv_plotter.list_csv_files(folder_path)
            for file in csv_files:
                self.file_listbox.insert(tk.END, os.path.basename(file))
            self.csv_files = csv_files
            self.status_var.set(f"找到 {len(csv_files)} 个CSV文件")
        else:
            self.status_var.set("文件夹不存在或为空")
    
    def select_all_files(self):
        self.file_listbox.select_set(0, tk.END)
    
    def deselect_all_files(self):
        self.file_listbox.selection_clear(0, tk.END)
    
    def toggle_output_folder(self):
        if self.use_original_var.get():
            self.output_folder_entry.config(state="disabled")
            self.btn_output_browse.config(state="disabled")
        else:
            self.output_folder_entry.config(state="normal")
            self.btn_output_browse.config(state="normal")
    
    def browse_output_folder(self):
        folder_path = filedialog.askdirectory(title="选择输出文件夹")
        if folder_path:
            self.output_folder_var.set(folder_path)
    
    def toggle_smooth_options(self):
        """根据是否启用平滑来切换平滑选项的状态"""
        if self.smooth_var.get():
            self.smooth_window_spinbox.config(state="normal")
        else:
            self.smooth_window_spinbox.config(state="disabled")
    
    def set_file_color(self):
        """为选中的文件设置颜色"""
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "请选择至少一个文件")
            return
            
        # 选择颜色
        color = colorchooser.askcolor(title="选择曲线颜色")
        if color[1]:  # 如果用户选择了颜色（没有取消）
            for idx in selected_indices:
                if idx < len(self.csv_files):
                    file_name = os.path.basename(self.csv_files[idx])
                    self.file_colors[file_name] = color[1]
            
            self.update_file_color_display()
    
    def update_file_color_display(self):
        """更新显示文件颜色的文本框"""
        self.file_color_text.config(state="normal")
        self.file_color_text.delete(1.0, tk.END)
        
        if self.file_colors:
            for file_name, color in self.file_colors.items():
                self.file_color_text.insert(tk.END, f"{file_name}: {color}\n")
        else:
            self.file_color_text.insert(tk.END, "未设置任何文件特定颜色")
            
        self.file_color_text.config(state="disabled")
    
    def reset_file_colors(self):
        """重置所有文件特定颜色"""
        self.file_colors = {}
        self.update_file_color_display()
        messagebox.showinfo("提示", "已重置所有文件特定颜色")
    
    def add_color(self):
        selection = self.color_listbox.curselection()
        if selection:
            color = self.color_listbox.get(selection[0])
            if color not in self.selected_colors:
                self.selected_colors.append(color)
                self.selected_color_var.set(", ".join(self.selected_colors))
                self.update_color_preview()
    
    def reset_colors(self):
        self.selected_colors = ["blue", "red", "green", "purple", "orange"]
        self.selected_color_var.set(", ".join(self.selected_colors))
        self.update_color_preview()
    
    def update_color_preview(self):
        self.color_canvas.delete("all")
        width = self.color_canvas.winfo_width() or 300
        height = self.color_canvas.winfo_height() or 50
        
        if not self.selected_colors:
            return
            
        block_width = width / len(self.selected_colors)
        
        for i, color in enumerate(self.selected_colors):
            x0 = i * block_width
            x1 = (i + 1) * block_width
            self.color_canvas.create_rectangle(x0, 0, x1, height, fill=color, outline="")
            
            # 计算文本颜色 (黑或白，取决于背景色)
            try:
                r, g, b = self.color_canvas.winfo_rgb(color)
                r, g, b = r/65535, g/65535, b/65535
                luminance = 0.299 * r + 0.587 * g + 0.114 * b
                text_color = "black" if luminance > 0.5 else "white"
            except:
                text_color = "black"
                
            self.color_canvas.create_text((x0 + x1) / 2, height / 2, text=color, fill=text_color)
    
    def on_color_double_click(self, event):
        self.add_color()
    
    def reset_settings(self):
        # 重置所有设置为默认值
        self.style_var.set("seaborn-v0_8-whitegrid")
        self.linewidth_var.set(2.0)
        self.linestyle_var.set("-")
        self.marker_var.set("None")
        self.font_family_var.set("serif")
        self.font_size_var.set(14)
        self.grid_var.set(True)
        self.title_var.set("训练曲线")
        self.xlabel_var.set("epochs")
        self.ylabel_var.set("损失值")
        self.xmin_var.set("")
        self.xmax_var.set("")
        self.ymin_var.set("")
        self.ymax_var.set("")
        self.show_legend_var.set(True)
        self.legend_loc_var.set("best")
        self.reset_colors()
        self.reset_file_colors()  # 重置文件颜色
        self.use_original_var.set(True)
        self.toggle_output_folder()
        self.format_var.set("svg")
        self.dpi_var.set(300)
        self.fig_width_var.set(8.0)
        self.fig_height_var.set(6.0)
        self.show_var.set(True)
        # 重置平滑设置
        self.smooth_var.set(False)
        self.smooth_window_var.set(3)
        self.toggle_smooth_options()
        
        self.status_var.set("已重置所有设置为默认值")

    # def plot_csv_files(self):
    #     # 获取选中的文件
    #     selected_indices = self.file_listbox.curselection()
    #     if not selected_indices:
    #         messagebox.showwarning("警告", "请选择至少一个CSV文件")
    #         return
            
    #     selected_files = [self.csv_files[i] for i in selected_indices]
        
    #     # 创建参数设置弹窗
    #     params_window = tk.Toplevel(self.root)
    #     params_window.title("图表参数设置")
    #     params_window.geometry("500x500")
    #     params_window.resizable(True, True)
    #     params_window.transient(self.root)  # 设置为主窗口的子窗口
    #     params_window.grab_set()  # 模态窗口
        
    #     # 创建主框架 - 包含滚动区域和底部按钮
    #     main_frame = ttk.Frame(params_window)
    #     main_frame.pack(fill=tk.BOTH, expand=True)
        
    #     # 创建滚动框架以容纳设置选项
    #     scroll_frame = ttk.Frame(main_frame)
    #     scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    #     canvas = tk.Canvas(scroll_frame)
    #     scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    #     scrollable_frame = ttk.Frame(canvas)
        
    #     scrollable_frame.bind(
    #         "<Configure>",
    #         lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    #     )
        
    #     canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    #     canvas.configure(yscrollcommand=scrollbar.set)
        
    #     canvas.pack(side="left", fill="both", expand=True)
    #     scrollbar.pack(side="right", fill="y")
        
    #     # 添加设置选项
    #     ttk.Label(scrollable_frame, text="图表标题设置", font=("Microsoft YaHei", 11, "bold")).pack(padx=10, pady=5, anchor="w")
        
    #     # 标题设置
    #     title_frame = ttk.Frame(scrollable_frame)
    #     title_frame.pack(fill=tk.X, padx=10, pady=5)
        
    #     use_title_var = tk.BooleanVar(value=bool(self.title_var.get()))
    #     ttk.Checkbutton(title_frame, text="使用标题", variable=use_title_var).pack(side=tk.LEFT, padx=5)
        
    #     temp_title_var = tk.StringVar(value=self.title_var.get())
    #     title_entry = ttk.Entry(title_frame, textvariable=temp_title_var, width=30)
    #     title_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
    #     # 更新标题状态
    #     def update_title_state():
    #         if use_title_var.get():
    #             title_entry.config(state="normal")
    #         else:
    #             title_entry.config(state="disabled")
        
    #     use_title_var.trace_add("write", lambda *args: update_title_state())
    #     update_title_state()
        
    #     # 分隔线
    #     ttk.Separator(scrollable_frame, orient="horizontal").pack(fill=tk.X, padx=10, pady=10)
        
    #     # 添加轴标签设置
    #     ttk.Label(scrollable_frame, text="坐标轴标签", font=("Microsoft YaHei", 11, "bold")).pack(padx=10, pady=5, anchor="w")
        
    #     # X轴标签
    #     x_label_frame = ttk.Frame(scrollable_frame)
    #     x_label_frame.pack(fill=tk.X, padx=10, pady=5)
    #     ttk.Label(x_label_frame, text="X轴标签:").pack(side=tk.LEFT, padx=5)
    #     temp_xlabel_var = tk.StringVar(value=self.xlabel_var.get())
    #     ttk.Entry(x_label_frame, textvariable=temp_xlabel_var).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
    #     # Y轴标签
    #     y_label_frame = ttk.Frame(scrollable_frame)
    #     y_label_frame.pack(fill=tk.X, padx=10, pady=5)
    #     ttk.Label(y_label_frame, text="Y轴标签:").pack(side=tk.LEFT, padx=5)
    #     temp_ylabel_var = tk.StringVar(value=self.ylabel_var.get())
    #     ttk.Entry(y_label_frame, textvariable=temp_ylabel_var).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
    #     # 分隔线
    #     ttk.Separator(scrollable_frame, orient="horizontal").pack(fill=tk.X, padx=10, pady=10)
        
    #     # 图例设置
    #     ttk.Label(scrollable_frame, text="图例设置", font=("Microsoft YaHei", 11, "bold")).pack(padx=10, pady=5, anchor="w")
        
    #     legend_frame = ttk.Frame(scrollable_frame)
    #     legend_frame.pack(fill=tk.X, padx=10, pady=5)
    #     temp_show_legend_var = tk.BooleanVar(value=self.show_legend_var.get())
    #     ttk.Checkbutton(legend_frame, text="显示图例", variable=temp_show_legend_var).pack(side=tk.LEFT, padx=5)
        
    #     # 图例位置
    #     legend_loc_frame = ttk.Frame(scrollable_frame)
    #     legend_loc_frame.pack(fill=tk.X, padx=10, pady=5)
    #     ttk.Label(legend_loc_frame, text="图例位置:").pack(side=tk.LEFT, padx=5)
    #     temp_legend_loc_var = tk.StringVar(value=self.legend_loc_var.get())
    #     ttk.Combobox(legend_loc_frame, textvariable=temp_legend_loc_var, 
    #             values=["best", "upper right", "upper left", "lower left", "lower right", 
    #                     "right", "center left", "center right", "lower center", "upper center", "center"]).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
    #     # 分隔线
    #     ttk.Separator(scrollable_frame, orient="horizontal").pack(fill=tk.X, padx=10, pady=10)
        
    #     # 输出设置
    #     ttk.Label(scrollable_frame, text="输出设置", font=("Microsoft YaHei", 11, "bold")).pack(padx=10, pady=5, anchor="w")
        
    #     # 图像格式
    #     format_frame = ttk.Frame(scrollable_frame)
    #     format_frame.pack(fill=tk.X, padx=10, pady=5)
    #     ttk.Label(format_frame, text="图像格式:").pack(side=tk.LEFT, padx=5)
    #     temp_format_var = tk.StringVar(value=self.format_var.get())
    #     ttk.Combobox(format_frame, textvariable=temp_format_var, 
    #                 values=["png", "jpg", "svg", "pdf"]).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
    #     # 底部按钮区域 - 独立于滚动区域
    #     btn_frame = ttk.Frame(main_frame)
    #     btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
    #     # 确定和取消按钮
    #     def on_cancel():
    #         params_window.destroy()
        
    #     def on_confirm():
    #         # 更新主界面的设置 - 特别处理标题
    #         # 保存是否使用标题的选择
    #         self.use_title = use_title_var.get()
            
    #         if self.use_title:
    #             self.title_var.set(temp_title_var.get())
    #         else:
    #             self.title_var.set("")  # 不使用标题
                
    #         self.xlabel_var.set(temp_xlabel_var.get())
    #         self.ylabel_var.set(temp_ylabel_var.get())
    #         self.show_legend_var.set(temp_show_legend_var.get())
    #         self.legend_loc_var.set(temp_legend_loc_var.get())
    #         self.format_var.set(temp_format_var.get())
            
    #         # 关闭参数窗口
    #         params_window.destroy()
            
    #         # 继续处理绘图
    #         self._continue_plot_csv_files(selected_files)
        
    #     ttk.Button(btn_frame, text="取消", command=on_cancel).pack(side=tk.RIGHT, padx=5)
    #     ttk.Button(btn_frame, text="确定", command=on_confirm).pack(side=tk.RIGHT, padx=5)
        
    #     # 等待窗口关闭
    #     self.root.wait_window(params_window)
    def plot_csv_files(self):
        """处理选中的CSV文件并绘图"""
        # 获取选中的文件
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "请选择至少一个CSV文件")
            return
                
        selected_files = [self.csv_files[i] for i in selected_indices]
        
        # 如果选中文件过多，提示确认
        if len(selected_files) > 10:
            if not messagebox.askyesno("确认", f"您选择了{len(selected_files)}个文件，绘制可能需要一些时间。是否继续？"):
                return
        
        # 创建参数设置弹窗
        params_window = tk.Toplevel(self.root)
        params_window.title("图表参数设置")
        params_window.geometry("600x600")
        params_window.resizable(True, True)
        params_window.transient(self.root)  # 设置为主窗口的子窗口
        params_window.grab_set()  # 模态窗口
        
        # 创建主框架 - 包含滚动区域和底部按钮
        main_frame = ttk.Frame(params_window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动框架以容纳设置选项
        scroll_frame = ttk.Frame(main_frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(scroll_frame)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 添加设置选项
        ttk.Label(scrollable_frame, text="图表标题设置", font=("Microsoft YaHei", 11, "bold")).pack(padx=10, pady=5, anchor="w")
        
        # 标题设置
        title_frame = ttk.Frame(scrollable_frame)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        use_title_var = tk.BooleanVar(value=bool(self.title_var.get()))
        ttk.Checkbutton(title_frame, text="使用标题", variable=use_title_var).pack(side=tk.LEFT, padx=5)
        
        temp_title_var = tk.StringVar(value=self.title_var.get())
        title_entry = ttk.Entry(title_frame, textvariable=temp_title_var, width=30)
        title_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 更新标题状态
        def update_title_state():
            if use_title_var.get():
                title_entry.config(state="normal")
            else:
                title_entry.config(state="disabled")
        
        use_title_var.trace_add("write", lambda *args: update_title_state())
        update_title_state()
        
        # 分隔线
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill=tk.X, padx=10, pady=10)
        
        # 添加轴标签设置
        ttk.Label(scrollable_frame, text="坐标轴标签", font=("Microsoft YaHei", 11, "bold")).pack(padx=10, pady=5, anchor="w")
        
        # X轴标签
        x_label_frame = ttk.Frame(scrollable_frame)
        x_label_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(x_label_frame, text="X轴标签:").pack(side=tk.LEFT, padx=5)
        temp_xlabel_var = tk.StringVar(value=self.xlabel_var.get())
        ttk.Entry(x_label_frame, textvariable=temp_xlabel_var).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Y轴标签
        y_label_frame = ttk.Frame(scrollable_frame)
        y_label_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(y_label_frame, text="Y轴标签:").pack(side=tk.LEFT, padx=5)
        temp_ylabel_var = tk.StringVar(value=self.ylabel_var.get())
        ttk.Entry(y_label_frame, textvariable=temp_ylabel_var).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 分隔线
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill=tk.X, padx=10, pady=10)
        
        # 添加颜色设置部分
        ttk.Label(scrollable_frame, text="曲线颜色设置", font=("Microsoft YaHei", 11, "bold")).pack(padx=10, pady=5, anchor="w")
        
        # 文件特定颜色设置
        file_colors_dict = {}  # 用于存储临时设置的文件颜色
        file_colors_dict.update(self.file_colors)  # 复制当前的文件颜色设置
        
        # 创建文件颜色设置区域
        color_listbox_frame = ttk.Frame(scrollable_frame)
        color_listbox_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 左侧是文件列表，右侧是颜色预览
        file_list_frame = ttk.LabelFrame(color_listbox_frame, text="选择要设置颜色的文件")
        file_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        file_scroll = ttk.Scrollbar(file_list_frame)
        file_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        file_color_listbox = tk.Listbox(file_list_frame, selectmode=tk.SINGLE,
                                    yscrollcommand=file_scroll.set, 
                                    height=6, width=30)
        file_color_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        file_scroll.config(command=file_color_listbox.yview)
        
        # 添加文件到列表中
        for file_path in selected_files:
            file_name = os.path.basename(file_path)
            file_color_listbox.insert(tk.END, file_name)
        
        # 颜色选择按钮和颜色预览
        color_select_frame = ttk.Frame(color_listbox_frame)
        color_select_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # 当前选中文件的颜色
        current_color_var = tk.StringVar(value="#0000FF")  # 默认蓝色
        color_preview = tk.Canvas(color_select_frame, width=50, height=20, bg=current_color_var.get())
        color_preview.pack(pady=5)
        
        # 更新颜色预览
        def update_color_preview(color):
            color_preview.config(bg=color)
        
        # 选择颜色按钮
        def select_color_for_file():
            selected = file_color_listbox.curselection()
            if not selected:
                messagebox.showwarning("警告", "请先选择一个文件")
                return
            
            file_name = file_color_listbox.get(selected[0])
            current = file_colors_dict.get(file_name, "#0000FF")
            
            color = colorchooser.askcolor(color=current, title=f"为 {file_name} 选择颜色")
            if color[1]:  # 用户选择了颜色
                file_colors_dict[file_name] = color[1]
                update_color_preview(color[1])
                # 在列表中标记已设置颜色的文件
                file_color_listbox.itemconfig(selected[0], bg="#F0F0F0", fg=color[1])
        
        ttk.Button(color_select_frame, text="选择颜色", command=select_color_for_file).pack(pady=5)
        
        # 清除颜色按钮
        def clear_file_color():
            selected = file_color_listbox.curselection()
            if not selected:
                messagebox.showwarning("警告", "请先选择一个文件")
                return
                
            file_name = file_color_listbox.get(selected[0])
            if file_name in file_colors_dict:
                del file_colors_dict[file_name]
                file_color_listbox.itemconfig(selected[0], bg="white", fg="black")
                update_color_preview("#FFFFFF")  # 默认白色
        
        ttk.Button(color_select_frame, text="清除颜色", command=clear_file_color).pack(pady=5)
        
        # 更新当前选中文件的颜色预览
        def on_file_select(event):
            selected = file_color_listbox.curselection()
            if selected:
                file_name = file_color_listbox.get(selected[0])
                if file_name in file_colors_dict:
                    update_color_preview(file_colors_dict[file_name])
                else:
                    update_color_preview("#FFFFFF")  # 默认白色
        
        file_color_listbox.bind('<<ListboxSelect>>', on_file_select)
        
        # 分隔线
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill=tk.X, padx=10, pady=10)
        
        # 添加平滑设置
        ttk.Label(scrollable_frame, text="曲线平滑设置", font=("Microsoft YaHei", 11, "bold")).pack(padx=10, pady=5, anchor="w")
        
        # 是否启用平滑
        smooth_frame = ttk.Frame(scrollable_frame)
        smooth_frame.pack(fill=tk.X, padx=10, pady=5)
        
        temp_smooth_var = tk.BooleanVar(value=self.smooth_var.get())
        ttk.Checkbutton(smooth_frame, text="启用数据平滑", variable=temp_smooth_var).pack(side=tk.LEFT, padx=5)
        
        # 平滑窗口大小
        smooth_window_frame = ttk.Frame(scrollable_frame)
        smooth_window_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(smooth_window_frame, text="平滑窗口大小:").pack(side=tk.LEFT, padx=5)
        temp_smooth_window_var = tk.IntVar(value=self.smooth_window_var.get())
        smooth_window_spin = ttk.Spinbox(
            smooth_window_frame, from_=2, to=50, textvariable=temp_smooth_window_var, width=5
        )
        smooth_window_spin.pack(side=tk.LEFT, padx=5)
        
        # 平滑说明
        smooth_info_frame = ttk.LabelFrame(scrollable_frame, text="平滑算法说明")
        smooth_info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(smooth_info_frame, text="使用移动平均算法平滑数据。较大的窗口将产生更平滑的曲线，但可能会丢失数据细节。", 
                wraplength=500, justify="left").pack(padx=5, pady=5, anchor="w")
        
        # 根据是否启用平滑来更新窗口大小输入框的状态
        def toggle_smooth_window_state():
            if temp_smooth_var.get():
                smooth_window_spin.config(state="normal")
            else:
                smooth_window_spin.config(state="disabled")
        
        temp_smooth_var.trace_add("write", lambda *args: toggle_smooth_window_state())
        toggle_smooth_window_state()  # 初始化状态
        
        # 分隔线
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill=tk.X, padx=10, pady=10)
        
        # 图例设置
        ttk.Label(scrollable_frame, text="图例设置", font=("Microsoft YaHei", 11, "bold")).pack(padx=10, pady=5, anchor="w")
        
        legend_frame = ttk.Frame(scrollable_frame)
        legend_frame.pack(fill=tk.X, padx=10, pady=5)
        temp_show_legend_var = tk.BooleanVar(value=self.show_legend_var.get())
        ttk.Checkbutton(legend_frame, text="显示图例", variable=temp_show_legend_var).pack(side=tk.LEFT, padx=5)
        
        # 图例位置
        legend_loc_frame = ttk.Frame(scrollable_frame)
        legend_loc_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(legend_loc_frame, text="图例位置:").pack(side=tk.LEFT, padx=5)
        temp_legend_loc_var = tk.StringVar(value=self.legend_loc_var.get())
        ttk.Combobox(legend_loc_frame, textvariable=temp_legend_loc_var, 
                values=["best", "upper right", "upper left", "lower left", "lower right", 
                        "right", "center left", "center right", "lower center", "upper center", "center"]).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 分隔线
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill=tk.X, padx=10, pady=10)
        
        # 输出设置
        ttk.Label(scrollable_frame, text="输出设置", font=("Microsoft YaHei", 11, "bold")).pack(padx=10, pady=5, anchor="w")
        
        # 图像格式
        format_frame = ttk.Frame(scrollable_frame)
        format_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(format_frame, text="图像格式:").pack(side=tk.LEFT, padx=5)
        temp_format_var = tk.StringVar(value=self.format_var.get())
        ttk.Combobox(format_frame, textvariable=temp_format_var, 
                    values=["png", "jpg", "svg", "pdf"]).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 底部按钮区域 - 独立于滚动区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # 确定和取消按钮
        def on_cancel():
            params_window.destroy()
        
        def on_confirm():
            # 更新主界面的设置 - 特别处理标题
            # 保存是否使用标题的选择
            self.use_title = use_title_var.get()
            
            if self.use_title:
                self.title_var.set(temp_title_var.get())
            else:
                self.title_var.set("")  # 不使用标题
                
            self.xlabel_var.set(temp_xlabel_var.get())
            self.ylabel_var.set(temp_ylabel_var.get())
            self.show_legend_var.set(temp_show_legend_var.get())
            self.legend_loc_var.set(temp_legend_loc_var.get())
            self.format_var.set(temp_format_var.get())
            
            # 更新平滑设置
            self.smooth_var.set(temp_smooth_var.get())
            self.smooth_window_var.set(temp_smooth_window_var.get())
            
            # 更新文件颜色设置
            self.file_colors.clear()
            self.file_colors.update(file_colors_dict)
            
            # 关闭参数窗口
            params_window.destroy()
            
            # 继续处理绘图
            self._continue_plot_csv_files(selected_files)
        
        ttk.Button(btn_frame, text="取消", command=on_cancel).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="确定", command=on_confirm).pack(side=tk.RIGHT, padx=5)
        
        # 等待窗口关闭
        self.root.wait_window(params_window)
    def _continue_plot_csv_files(self, selected_files):
        """继续执行绘图过程"""
        # 获取X轴除数
        x_divisor = None
        if self.x_divisor_var.get().strip():
            try:
                x_divisor = float(self.x_divisor_var.get())
            except ValueError:
                messagebox.showwarning("警告", "X轴除数必须是有效的数字")
                return
        
        # 获取X和Y轴范围
        xlim = None
        if self.xmin_var.get().strip() and self.xmax_var.get().strip():
            try:
                xlim = (float(self.xmin_var.get()), float(self.xmax_var.get()))
            except ValueError:
                messagebox.showwarning("警告", "X轴范围必须是有效的数字")
                return
                
        ylim = None
        if self.ymin_var.get().strip() and self.ymax_var.get().strip():
            try:
                ylim = (float(self.ymin_var.get()), float(self.ymax_var.get()))
            except ValueError:
                messagebox.showwarning("警告", "Y轴范围必须是有效的数字")
                return
        
        # 构建绘图配置
        plot_config = {
            'style': self.style_var.get(),
            'use_title': hasattr(self, 'use_title') and self.use_title,  # 明确指定是否使用标题
            'title': self.title_var.get(),
            'xlabel': self.xlabel_var.get(),
            'ylabel': self.ylabel_var.get(),
            'colors': self.selected_colors,
            'linewidth': self.linewidth_var.get(),
            'linestyle': self.linestyle_var.get(),
            'marker': None if self.marker_var.get() == "None" else self.marker_var.get(),
            'grid': self.grid_var.get(),
            'format': self.format_var.get(),
            'dpi': self.dpi_var.get(),
            'figsize': (self.fig_width_var.get(), self.fig_height_var.get()),
            'show': self.show_var.get(),
            'x_col': self.x_col_var.get(),
            'y_col': self.y_col_var.get(),
            'skiprows': self.skiprows_var.get(),
            'x_divisor': x_divisor,
            'font': {
                'family': self.font_family_var.get(),
                'serif': 'Times New Roman',
                'weight': 'normal',
                'size': self.font_size_var.get(),
            },
            # 添加平滑相关的配置
            'smooth': self.smooth_var.get(),
            'smooth_window': self.smooth_window_var.get(),
            # 添加文件特定颜色的配置
            'file_colors': self.file_colors
        }
        
        # 如果需要图例
        if self.show_legend_var.get():
            plot_config['legend'] = [os.path.basename(f).split('.')[0] for f in selected_files]
            plot_config['legend_loc'] = self.legend_loc_var.get()
            
        # 坐标轴范围
        if xlim:
            plot_config['xlim'] = xlim
        if ylim:
            plot_config['ylim'] = ylim
            
        # 确定输出文件夹
        output_folder = None
        if not self.use_original_var.get():
            output_folder = self.output_folder_var.get()
            if not output_folder or not os.path.exists(output_folder):
                messagebox.showwarning("警告", "请选择有效的输出文件夹")
                return
        
        # 禁用界面按钮，防止多次点击
        self.btn_plot.config(state="disabled")
        self.status_var.set("正在生成图表...")
        self.root.update()
        
        # 在单独的线程中执行绘图，避免界面卡死
        def plot_thread():
            try:
                generated_files = csv_plotter.plot_csv_data(selected_files, plot_config, output_folder)
                
                # 更新状态
                self.root.after(0, lambda: self.status_var.set(f"已生成 {len(generated_files)} 个图表"))
                
                # 如果生成成功，弹出成功消息
                if generated_files:
                    self.root.after(0, lambda: messagebox.showinfo("成功", f"已成功生成 {len(generated_files)} 个图表"))
            except Exception as e:
                # 如果出错，显示错误消息
                self.root.after(0, lambda: messagebox.showerror("错误", f"生成图表时出错: {str(e)}"))
            finally:
                # 重新启用界面按钮
                self.root.after(0, lambda: self.btn_plot.config(state="normal"))
        
        # 启动绘图线程
        threading.Thread(target=plot_thread, daemon=True).start()
def main():
    root = tk.Tk()
    app = CSVPlotterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
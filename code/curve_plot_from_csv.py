import pandas as pd
import matplotlib.pyplot as plt

# 读取第一个CSV文件
csv_file_path1 = '.\experiments\MAE\mae_base_pretrain\mae_vit_base_patch16_bs128_mr75_blr1e-3_vision_0411-train_loss.csv'  # 替换为第一个CSV文件的路径
df1 = pd.read_csv(csv_file_path1, header=None, skiprows=1)

# 提取第一个CSV文件的x和y轴数据
x_data1 = df1.iloc[1:, 1].astype(float)
# 将x除以1000转化为epochs
x_data1 = x_data1 / 1000
y_data1 = df1.iloc[1:, 2].astype(float)

# 读取第二个CSV文件
csv_file_path2 = '.\experiments\CrossMAE\cross_bs48_0411-train_loss.csv'  # 替换为第二个CSV文件的路径
df2 = pd.read_csv(csv_file_path2, header=None, skiprows=1)

# 提取第二个CSV文件的x和y轴数据
x_data2 = df2.iloc[1:, 1].astype(float)
# 将x除以1000转化为epochs
x_data2 = x_data2 / 1000
y_data2 = df2.iloc[1:, 2].astype(float)

# 设置绘图风格，使用科学论文常见的线条样式和颜色
# plt.style.use('seaborn-whitegrid')
plt.style.use('seaborn-v0_8-whitegrid')  # 新的命名格式

# 设置字体和字号
font = {'family': 'serif',
        'serif': 'Times New Roman',
        'weight': 'normal',
        'size': 15,
        }
plt.rc('font', **font)

# 绘制第一幅图像
plt.figure(1)
plt.plot(x_data1, y_data1,color='blue', linewidth=2)
plt.xlabel('epochs')
plt.ylabel('TrainLoss')
# plt.title('MAE Pretrain Loss')

plt.tight_layout()
# 调整布局使得图像不溢出
plt.savefig('MAEPretrainLoss.svg', format='svg', bbox_inches='tight')

# 绘制第二幅图像
plt.figure(2)
plt.plot(x_data2, y_data2, color='red', linewidth=2)
plt.xlabel('epochs')
plt.ylabel('SmoothL1Loss')
# plt.title('Finetune SmoothL1Loss')

plt.tight_layout()
# 调整布局使得图像不溢出
plt.savefig('FinetuneSmoothL1Loss.svg', format='svg', bbox_inches='tight')

# 显示图形
plt.show()

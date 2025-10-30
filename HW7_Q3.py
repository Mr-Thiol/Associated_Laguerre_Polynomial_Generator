import numpy as np
import matplotlib.pyplot as plt
from scipy.special import genlaguerre, factorial

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 氢原子径向波函数 (原子单位, Z=1)
def radial_wavefunction(n, l, r, Z=1):
    """
    计算氢原子的径向波函数 R_nl(r)
    n: 主量子数
    l: 角量子数
    r: 径向距离 (原子单位)
    Z: 核电荷数
    """
    # 归一化常数
    rho = 2 * Z * r / n
    
    # 归一化系数
    norm = np.sqrt((2*Z/n)**3 * factorial(n-l-1) / (2*n*factorial(n+l)))
    
    # 连带拉盖尔多项式
    laguerre = genlaguerre(n-l-1, 2*l+1)
    
    # 径向波函数
    R = norm * np.exp(-rho/2) * rho**l * laguerre(rho)
    
    return R

# 设置径向距离范围
r = np.linspace(0, 25, 1000)

# 创建图形
plt.figure(figsize=(12, 8))

# 定义要绘制的轨道
orbitals = [
    (1, 0, '1s'),
    (2, 0, '2s'),
    (2, 1, '2p'),
    (3, 0, '3s'),
    (3, 1, '3p'),
    (3, 2, '3d')
]

# 绘制每个轨道的径向函数
for n, l, label in orbitals:
    R = radial_wavefunction(n, l, r, Z=1)
    plt.plot(r, R, label=label, linewidth=2)

# 设置图形属性
plt.xlabel(r'$r$ (原子单位 $a_0$)', fontsize=12)
plt.ylabel(r'$R(r)$', fontsize=12)
plt.title('氢原子轨道径向波函数 (Z=1)', fontsize=14, fontweight='bold')
plt.legend(fontsize=11, loc='best')
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.xlim(0, 27)

# 显示图形
plt.tight_layout()
plt.savefig("R(r)-r plot.png")
plt.show()
"""
连带拉盖尔多项式生成器

该程序使用Sympy计算连带拉盖尔多项式 L_n^l(x)，并使用matplotlib渲染LaTeX公式。

公式: L_n^l(x) = Σ(k=0 to n) [(-1)^k * C(n+l, n-k) * x^k / k!]

依赖:
- tkinter: GUI界面
- sympy: 符号数学计算
- matplotlib: LaTeX渲染
"""

import tkinter as tk
from tkinter import messagebox
import traceback

# Sympy 库用于数学计算
from sympy import symbols, summation, binomial, factorial, latex, expand

# Matplotlib 库用于在 Tkinter 中渲染 LaTeX
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Sympy 符号定义 (全局) ---
x = symbols('x')
k = symbols('k', integer=True, nonnegative=True)


class LaguerreApp:
    """连带拉盖尔多项式生成器主应用类"""
    
    # 类常量
    MAX_SAFE_N = 20
    DEFAULT_WINDOW_SIZE = "800x600"
    LATEX_FONT_SIZE = 12
    MAX_LINE_LENGTH = 80
    
    def __init__(self, root):
        self.root = root
        self.current_latex = ""  # 存储当前LaTeX字符串
        
        self._setup_window()
        self._create_widgets()
        self._initialize_canvas()
        self._bind_shortcuts()
    
    def _setup_window(self):
        """初始化窗口设置"""
        self.root.title("连带拉盖尔多项式生成器")
        self.root.geometry(self.DEFAULT_WINDOW_SIZE)
    
    def _create_widgets(self):
        """创建所有UI控件"""
        self._create_control_panel()
    
    def _create_control_panel(self):
        """创建输入控件面板"""
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        # n 输入
        tk.Label(control_frame, text="n (整数):").pack(side=tk.LEFT, padx=5)
        self.n_entry = tk.Entry(control_frame, width=8)
        self.n_entry.pack(side=tk.LEFT, padx=5)
        self.n_entry.insert(0, "3")  # 默认值
        
        # l 输入
        tk.Label(control_frame, text="l (整数):").pack(side=tk.LEFT, padx=5)
        self.l_entry = tk.Entry(control_frame, width=8)
        self.l_entry.pack(side=tk.LEFT, padx=5)
        self.l_entry.insert(0, "1")  # 默认值
        
        # 生成按钮
        self.generate_button = tk.Button(
            control_frame, 
            text="生成 (Enter)", 
            command=self.generate_polynomial,
            bg="#4CAF50",
            fg="white",
            padx=10
        )
        self.generate_button.pack(side=tk.LEFT, padx=10)
        
        # 复制按钮
        self.copy_button = tk.Button(
            control_frame, 
            text="复制LaTeX", 
            command=self.copy_latex,
            padx=10
        )
        self.copy_button.pack(side=tk.LEFT, padx=5)
        
        # 退出按钮
        self.exit_button = tk.Button(
            control_frame, 
            text="退出 (Esc)", 
            command=self.quit_app,
            padx=10
        )
        self.exit_button.pack(side=tk.LEFT, padx=5)
    
    def _initialize_canvas(self):
        """初始化matplotlib画布"""
        # 创建带滚动条的框架
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建matplotlib图形
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')
        
        # 创建画布
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加垂直滚动条
        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 显示初始公式
        initial_latex = r"L_n^l(x) = \sum_{k=0}^{n} (-1)^k \binom{n+l}{n-k} \frac{x^k}{k!}"
        self.render_latex(initial_latex, is_formula=True)
    
    def _bind_shortcuts(self):
        """绑定键盘快捷键"""
        # Enter键生成
        self.n_entry.bind('<Return>', lambda e: self.generate_polynomial())
        self.l_entry.bind('<Return>', lambda e: self.generate_polynomial())
        
        # Escape键退出
        self.root.bind('<Escape>', lambda e: self.quit_app())
        
        # Ctrl+C 复制
        self.root.bind('<Control-c>', lambda e: self.copy_latex())
    
    def generate_polynomial(self):
        """生成多项式的主函数"""
        try:
            # 获取并验证输入
            n = int(self.n_entry.get())
            l = int(self.l_entry.get())
            
            if n < 0 or l < 0:
                messagebox.showerror("输入错误", "n 和 l 必须是非负整数。")
                return
            
            # 对大数值给出警告
            if n > self.MAX_SAFE_N:
                response = messagebox.askokcancel(
                    "警告", 
                    f"n={n} 可能需要较长计算时间，甚至导致内存不足。\n\n建议使用 n ≤ {self.MAX_SAFE_N}\n\n是否继续？"
                )
                if not response:
                    return
            
            # 显示计算中的提示
            self.render_latex(r"\text{正在计算中，请稍候...}", is_formula=True)
            self.root.update()  # 强制更新UI
            
            # 执行计算
            self._compute_and_display(n, l)
            
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的整数。")
        except MemoryError:
            messagebox.showerror("内存错误", "计算结果过大，请尝试较小的n值。")
            self.render_latex(r"\text{计算失败：内存不足}", is_formula=True)
        except KeyboardInterrupt:
            messagebox.showinfo("已取消", "计算已被用户取消。")
        except Exception as e:
            messagebox.showerror("计算错误", f"生成多项式时出错:\n{str(e)}")
            print("详细错误信息:")
            print(traceback.format_exc())
            self.render_latex(r"\text{计算出错}", is_formula=True)
    
    def _compute_and_display(self, n, l):
        """执行Sympy计算并显示结果"""
        try:
            # 使用Sympy计算连带拉盖尔多项式
            L_x = summation(
                (-1) ** k * binomial(n + l, n - k) * x ** k / factorial(k), 
                (k, 0, n)
            )
            L_x_expanded = L_x.doit().expand()
            
            # 生成LaTeX字符串
            latex_str = latex(L_x_expanded)
            
            # 智能换行：在运算符处添加换行
            if len(latex_str) > self.MAX_LINE_LENGTH:
                latex_str = self._format_long_latex(latex_str)
            
            # 保存当前LaTeX
            self.current_latex = latex_str
            
            # 创建带标题的完整LaTeX
            title = f"L_{{{n}}}^{{{l}}}(x) = "
            full_latex = title + latex_str
            
            # 渲染结果
            self.render_latex(full_latex, is_formula=True)
            
            # 显示成功消息
            self.root.title(f"连带拉盖尔多项式生成器 - L_{n}^{l}(x)")
            
        except Exception as e:
            raise Exception(f"Sympy计算失败: {str(e)}")
    
    def _format_long_latex(self, latex_str):
        """格式化长LaTeX字符串，添加换行"""
        # 在加减号处添加空格，便于换行
        latex_str = latex_str.replace('+', ' + ')
        latex_str = latex_str.replace('-', ' - ')
        
        # 对于特别长的表达式，在运算符处强制换行
        if len(latex_str) > self.MAX_LINE_LENGTH * 2:
            latex_str = latex_str.replace(' + ', ' +\n')
            latex_str = latex_str.replace(' - ', ' -\n')
        
        return latex_str
    
    def render_latex(self, latex_str, is_formula=False):
        """在matplotlib画布上渲染LaTeX字符串"""
        try:
            # 清除之前的内容
            self.ax.clear()
            self.ax.axis('off')
            
            # 检查LaTeX字符串长度，决定渲染策略
            if len(latex_str) > 2000:
                # 超长内容：分段渲染
                self._render_long_latex(latex_str, is_formula)
            else:
                # 正常长度：直接渲染
                self._render_normal_latex(latex_str, is_formula)
            
            # 调整布局
            self.fig.tight_layout()
            
            # 重新绘制
            self.canvas.draw()
            
        except Exception as e:
            # 如果渲染失败，尝试降级方案
            print("LaTeX渲染失败，尝试降级方案...")
            print(f"错误: {str(e)}")
            try:
                self._render_as_text(latex_str)
            except:
                messagebox.showerror("渲染错误", 
                    f"LaTeX渲染失败。\n\n建议：\n1. 尝试较小的n值\n2. 使用'复制LaTeX'按钮获取代码\n3. 在专业LaTeX编辑器中查看\n\n错误: {str(e)}")
                print("完整错误信息:")
                print(traceback.format_exc())
    
    def _render_normal_latex(self, latex_str, is_formula):
        """渲染正常长度的LaTeX"""
        # 根据长度动态调整字体大小
        fontsize = self.LATEX_FONT_SIZE
        if len(latex_str) > 500:
            fontsize = 10
        if len(latex_str) > 1000:
            fontsize = 8
        
        self.ax.text(
            0.5, 0.5, 
            f"${latex_str}$" if is_formula else latex_str,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=fontsize,
            transform=self.ax.transAxes
        )
    
    def _render_long_latex(self, latex_str, is_formula):
        """渲染超长LaTeX - 分段显示"""
        # 将LaTeX分成多行
        lines = self._split_latex_into_lines(latex_str)
        
        # 计算垂直位置
        num_lines = len(lines)
        fontsize = max(6, 12 - num_lines // 5)  # 动态调整字体大小
        
        # 从上到下渲染每一行
        for i, line in enumerate(lines):
            y_pos = 0.95 - (i * 0.9 / max(num_lines, 1))
            
            self.ax.text(
                0.05, y_pos,
                f"${line}$" if is_formula else line,
                horizontalalignment='left',
                verticalalignment='top',
                fontsize=fontsize,
                transform=self.ax.transAxes
            )
    
    def _split_latex_into_lines(self, latex_str, max_len=100):
        """将长LaTeX字符串分割成多行"""
        lines = []
        current_line = ""
        
        # 按运算符分割
        parts = latex_str.replace(' + ', '|+|').replace(' - ', '|-|').split('|')
        
        for part in parts:
            if len(current_line) + len(part) < max_len:
                current_line += part
            else:
                if current_line:
                    lines.append(current_line)
                current_line = part
        
        if current_line:
            lines.append(current_line)
        
        return lines if lines else [latex_str]
    
    def _render_as_text(self, latex_str):
        """降级方案：渲染为纯文本"""
        self.ax.clear()
        self.ax.axis('off')
        
        # 移除LaTeX命令，显示基本内容
        text_content = latex_str.replace('\\', '').replace('{', '').replace('}', '')
        
        self.ax.text(
            0.5, 0.5,
            f"渲染失败，显示纯文本:\n\n{text_content[:500]}...",
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=10,
            transform=self.ax.transAxes,
            wrap=True
        )
        
        self.canvas.draw()
    
    def copy_latex(self):
        """复制当前LaTeX到剪贴板"""
        if self.current_latex:
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(self.current_latex)
                messagebox.showinfo("成功", "LaTeX代码已复制到剪贴板！")
            except Exception as e:
                messagebox.showerror("复制失败", f"无法复制到剪贴板:\n{str(e)}")
        else:
            messagebox.showwarning("无内容", "没有可复制的LaTeX代码。请先生成多项式。")
    
    def quit_app(self):
        """安全关闭应用程序"""
        print("退出按钮被按下，正在关闭应用...")
        self.root.destroy()


# --- 程序主入口 ---
if __name__ == "__main__":
    print("启动GUI应用...")
    root = tk.Tk()
    app = LaguerreApp(root)
    root.mainloop()
    print("应用已成功退出。")
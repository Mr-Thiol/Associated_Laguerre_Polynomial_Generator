import tkinter as tk
from tkinter import messagebox
# Sympy 库用于数学计算
from sympy import symbols, summation, binomial, factorial, latex, expand

# Matplotlib 库用于在 Tkinter 中渲染 LaTeX
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Sympy 符号定义 (全局) ---
x = symbols('x')
k = symbols('k', integer=True, nonnegative=True)

class LaguerreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("连带拉盖尔多项式生成器")
        self.root.geometry("700x500") 
        
        # --- 存储状态的变量 ---
        self.current_fontsize = 14 
        self.last_latex_str = ""   
        # --- 用于存储纯 LaTeX 代码的变量 ---
        self.current_raw_latex = r"L_n^l(x) = \sum_{k=0}^{n} (-1)^k \binom{n+l}{n-k} \frac{x^k}{k!}"

        # --- 1. 创建输入控件 ---
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10) # 顶部留出空间

        tk.Label(control_frame, text="n (整数):").pack(side=tk.LEFT, padx=5)
        self.n_entry = tk.Entry(control_frame, width=5)
        self.n_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="l (整数):").pack(side=tk.LEFT, padx=5)
        self.l_entry = tk.Entry(control_frame, width=5)
        self.l_entry.pack(side=tk.LEFT, padx=5)
        
        # --- 字体大小控制 ---
        tk.Label(control_frame, text="字体:").pack(side=tk.LEFT, padx=(10, 0))
        self.zoom_out_button = tk.Button(control_frame, text="-", command=self.zoom_out, width=2)
        self.zoom_out_button.pack(side=tk.LEFT, padx=(5, 2))
        
        self.zoom_in_button = tk.Button(control_frame, text="+", command=self.zoom_in, width=2)
        self.zoom_in_button.pack(side=tk.LEFT, padx=2)

        # --- 功能按钮 ---
        self.generate_button = tk.Button(control_frame, text="生成", command=self.generate_polynomial)
        self.generate_button.pack(side=tk.LEFT, padx=(10, 5)) # 增加左边距
        
        # --- 复制 LaTeX 按钮 ---
        self.copy_button = tk.Button(control_frame, text="复制LaTeX", command=self.copy_latex)
        self.copy_button.pack(side=tk.LEFT, padx=5)
        
        self.exit_button = tk.Button(control_frame, text="退出", command=self.quit_app)
        self.exit_button.pack(side=tk.LEFT, padx=5)

        # --- 2. 创建 LaTeX 渲染区域 ---
        self.fig = Figure(dpi=100, constrained_layout=True)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off') 
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        initial_latex = r"Associated Laguerre Polynomials:" + \
                      r" $L_n^l(x) = \sum_{k=0}^{n} (-1)^k \binom{n+l}{n-k} \frac{x^k}{k!}$"
        
        self.render_latex(initial_latex) 


    def generate_polynomial(self):
        """
        按钮的回调函数：获取输入，计算多项式，并渲染 LaTeX
        """
        try:
            # --- 3. 获取和验证输入 ---
            n = int(self.n_entry.get())
            l = int(self.l_entry.get())
            
            if n < 0 or l < 0:
                 messagebox.showerror("输入错误", "n 和 l 必须是非负整数。")
                 return
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的整数。")
            return

        try:
            # --- 4. 核心 Sympy 逻辑 ---
            L_x = summation((-1) ** k * binomial(n + l, n - k) * x** k / (factorial(k)), (k, 0, n))
            L_x_expanded = L_x.doit().expand()

            # 生成 LaTeX 字符串
            latex_str = latex(L_x_expanded)
            
            # --- 存储纯 LaTeX 以便复制 ---
            self.current_raw_latex = latex_str
            
            # 智能换行策略 (仅用于显示)
            latex_str = latex_str.replace("+", " + ")
            latex_str = latex_str.replace("-", " - ")
            
            final_str = f"${latex_str}$"

            # --- 5. 渲染 LaTeX ---
            self.render_latex(final_str)

        except Exception as e:
            messagebox.showerror("计算错误", f"生成多项式时出错: {e}")

    def render_latex(self, text_str):
        """
        在 Matplotlib 画布上渲染一个包含 mathtext 的字符串
        """
        self.last_latex_str = text_str
        
        try:
            self.ax.clear() 
            self.ax.axis('off') 
            self.ax.text(0.5, 0.5, f"{text_str}",
                         horizontalalignment='center',
                         verticalalignment='center',
                         fontsize=self.current_fontsize, 
                         wrap=True) 
            
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("渲染错误", f"渲染 LaTeX 时出错: {e}")

    # --- 复制 LaTeX 到剪贴板 ---
    def copy_latex(self):
        """将 self.current_raw_latex 复制到剪贴板"""
        if not self.current_raw_latex:
            print("No raw LaTeX to copy.")
            messagebox.showinfo("提示", "没有可复制的 LaTeX。请先生成一个多项式。")
            return
            
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_raw_latex)
            print(f"Copied to clipboard: {self.current_raw_latex}")
            
            # --- 提供视觉反馈 ---
            original_text = self.copy_button.cget("text")
            self.copy_button.config(text="已复制!", state="disabled")
            # 2秒后恢复按钮
            self.root.after(2000, lambda: self.copy_button.config(text=original_text, state="normal"))
            
        except tk.TclError:
            print("Failed to copy to clipboard (TclError).")
            messagebox.showwarning("复制失败", "无法访问剪贴板。")
        except Exception as e:
            print(f"Failed to copy to clipboard: {e}")
            messagebox.showerror("复制失败", f"发生未知错误: {e}")

    # --- 字体大小控制 ---
    def zoom_in(self):
        """增大字体并重新渲染"""
        self.current_fontsize += 2
        print(f"Font size set to {self.current_fontsize}")
        self.render_latex(self.last_latex_str)

    def zoom_out(self):
        """减小字体并重新渲染"""
        if self.current_fontsize > 6: # 设置一个最小字体大小
            self.current_fontsize -= 2
            print(f"Font size set to {self.current_fontsize}")
            self.render_latex(self.last_latex_str)

    # --- 退出按钮的回调函数 ---
    def quit_app(self):
        """安全关闭 Tkinter 窗口"""
        print("Exit button pressed. Closing application.")
        self.root.destroy()

# --- 程序主入口 ---
if __name__ == "__main__":
    print("Startup GUI...")
    root = tk.Tk()
    app = LaguerreApp(root)
    root.mainloop()
    print("Exit Successfully.")
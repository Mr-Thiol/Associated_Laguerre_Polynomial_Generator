# Quantum Chemistry, Homework 7, Question 2：连带拉盖尔多项式生成器 (Associated Laguerre Polynomial Generator)

这是一个使用 Python、Tkinter、SymPy 和 Matplotlib 开发的桌面 GUI 应用程序，用于生成指定阶数 $n$ 和 $l$ 的连带拉盖尔多项式：

$L_n^l(x) = \displaystyle\sum_{k=0}^{n} (-1)^k \binom{n+l}{n-k} \frac{x^k}{k!}$。

![screenshot](.//screenshot.png)

## 核心功能

* **数学计算**: 使用 `SymPy` 库精确计算多项式的展开形式。
* **LaTeX 渲染**: 使用 `Matplotlib` 在 GUI 界面中高质量渲染数学公式。
* **交互式 GUI**: 使用 `Tkinter` 构建，包含：
    * 字体大小缩放 (`+` / `-`) 按钮。
    * 一键复制生成的 LaTeX 源代码到剪贴板。
    * 安全的退出按钮。

---

## 如何使用

有两种方式来运行这个程序：

### 方式 A：直接下载 (推荐)

为 Windows 用户提供的可执行文件 (.exe)，无需安装 Python 或任何库。

1.  访问本仓库的 **[Releases 页面](https://github.com/Mr-Thiol/Associated_Laguerre_Polynomial_Generator/releases)**。
2.  下载最新版本（如 `v1.0.0`）下的 `laguerre_gui.exe` 文件。
3.  双击运行。

### 方式 B：从源代码运行 (开发者)

如果你想自己修改或运行代码，你需要一个 Conda 环境。

1.  **克隆仓库**
    ```bash
    git clone [https://github.com/Mr-Thiol/Associated_Laguerre_Polynomial_Generator](https://github.com/Mr-Thiol/Associated_Laguerre_Polynomial_Generator)
    cd laguerre-polynomial-generator
    ```

2.  **创建 Conda 环境**
    使用 `environment.yml` 文件自动创建并激活环境：
    ```bash
    conda env create -f environment.yml
    conda activate laguerre_env 
    ```
    *(或者手动安装: `conda create -n laguerre python=3.10 tk sympy matplotlib`)*

3.  **运行脚本**
    ```bash
    python laguerre_gui.py
    ```

---

## Acknowledgement

Thank you, Gemini 2.5 Pro!

Gemini has taught me how to polish my code, generate .exe file, and commit my work to GitHub. Thank you again! :+1:

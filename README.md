Engligh README is below Chinese one. ([Here](#conjuctions-linking-game))
# 联结词连连看
联结词连连看小游戏，完全使用 Python 编写。

这个项目本来是我的《数据结构与算法综合实训》的实验项目，为了能更好帮助 Python 学习者学习这个强大而有趣的语言，我决定在课程结束后将本项目开源。

## 从代码中运行
本项目使用 Python 3.12 开发。请确保至少使用 Python 3.10 或更高版本。

1. 安装依赖包

    ```bash
    pip install -r requirements.txt
    ```

2. 运行 `main.py`

    ```bash
    python main.py
    ```

## 编译
### 使用 PyInstaller 编译
1. 安装 `pyinstaller`：

    ```bash
    pip install pyinstaller
    ```

2. 运行

    ```bash
    pyinstaller --noconsole main.py
    ```

    如果您想打包为一个文件，也可以运行以下命令：

    ```bash
    pyinstaller --onefile --noconsole main.py
    ```

3. 将 `assets/`, `saves/` 文件夹复制到构建位置。

4. 运行 `main.exe`.

### 使用 Nuitka 编译（推荐）

**Nuitka 与 Python 3.13 不兼容**。建议使用 Python 3.12 环境。

1. 安装 `Nuitka`：

    ```bash
    pip install nuitka
    ```

2. 执行以下命令：

    ```bash
    python -m nuitka --standalone --disable-console --include-data-dir=./assets=./assets --include-data-dir=./saves=./saves main.py
    ```

    如果您想打包成一个文件，也可以运行以下命令：

    ```bash
    python -m nuitka --standalone --onefile --disable-console --include-data-dir=./assets=./assets --include-data-dir=./saves=./saves main.py
    ```

    输出文件夹位于 `main.dist`。

3. 运行 `main.dist` 中的 `main.exe`.

## 许可证
所有代码均采用 [MIT 许可](LICENSE)。

本项目中使用的资产采用各自的许可证。

# Conjuctions Linking game
Small conjuction linking game fully written in Python.

## Run from code
The game is developed in Python 3.12. Make sure you have at least Python 3.10 or above.

1. Install the requirements:

    ```bash
    pip install -r requirements.txt
    ```

2. Run `main.py`:

    ```bash
    python main.py
    ```

## Compile
### Compile with PyInstaller
1. Install `pyinstaller`:

    ```bash
    pip install pyinstaller
    ```

2. Run:

    ```bash
    pyinstaller --noconsole main.py
    ```

    Or run this if you want to pack the game into one file:
    ```bash
    pyinstaller --onefile --noconsole main.py
    ```

3. Copy `assets/`, `saves/` folder to the build location.

4. Run `main.exe`.

### Compile with Nuitka (recommended)
1. Install `Nuitka`:

    ```bash
    pip install nuitka
    ```

2. Run:

    ```bash
    python -m nuitka --standalone --disable-console --include-data-dir=./assets=./assets --include-data-dir=./saves=./saves main.py
    ```

    Or run this if you want to pack the game into one file:
    ```bash
    python -m nuitka --standalone --onefile --disable-console --include-data-dir=./assets=./assets --include-data-dir=./saves=./saves main.py
    ```

    The output folder is in `main.dist`.

3. Run `main.exe` in `main.dist`.


## License
All code is under [MIT License](LICENSE).

Assets used in this project are licensed under their respective licenses.
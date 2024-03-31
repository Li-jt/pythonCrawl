# **python 爬虫**

## python：v3.12

## 配置文件：config.ini

## 运行目录：src/index.py

### 导出整个环境的依赖包：pip freeze > requirements.txt

### 导出整个项目的依赖包： pipreqs . --force --ignore ".venv"

### 安装依赖文件： pip install -r requirements.txt

### 打包命令：Pyinstaller -D -w -i pixiv.png main.py


# pipreqs 控制台参数
    –debug     打印调试信息
    –ignore    …忽略额外的目录
    –encoding  使用编码参数打开文件
    –savepath  保存给定文件中的需求列表
    –print     输出标准输出中的需求列表
    –force     覆盖现有的requirements.txt
    –diff      将requirements.txt中的模块与项目导入进行比较。
    –clean     通过删除未在项目中导入的模块来清理requirements.txt。
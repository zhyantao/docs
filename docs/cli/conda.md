# Conda

[官方速查表](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html)

## 快速开始

| 操作                      | 命令                         |
| ------------------------- | ---------------------------- |
| 检查 Conda 是否安装及版本 | `conda info`                 |
| 更新 Conda 到最新版本     | `conda update -n base conda` |
| 更新所有包到最新版本      | `conda update anaconda`      |
| 列出所有环境              | `conda env list`             |

## 配置工作环境

| 操作                           | 命令                                                 |
| ------------------------------ | ---------------------------------------------------- |
| 创建新环境（指定 Python 版本） | `conda create --name ENVNAME python=3.6`             |
| 激活环境                       | `conda activate ENVNAME`                             |
| 激活本地环境                   | `conda activate /path/to/environment-dir`            |
| 取消激活当前环境               | `conda deactivate`                                   |
| 列出当前环境的包               | `conda list`                                         |
| 列出指定环境的包               | `conda list --name ENVNAME`                          |
| 列出当前环境的历史版本         | `conda list --revisions`                             |
| 列出指定环境的历史版本         | `conda list --name ENVNAME --revisions`              |
| 回退环境到指定版本             | `conda install --name ENVNAME --revision REV_NUMBER` |
| 删除环境                       | `conda remove --name ENVNAME --all`                  |

## 共享工作环境

| 操作                                | 命令                                            |
| ----------------------------------- | ----------------------------------------------- |
| 复制环境                            | `conda create --clone ENVNAME --name NEWENV`    |
| 导出环境到 YAML 文件                | `conda env export --name ENVNAME > envname.yml` |
| 从 YAML 文件创建环境                | `conda env create --file envname.yml`           |
| 从当前目录 environment.yml 创建环境 | `conda env create`                              |
| 导出精确包列表（跨平台）            | `conda list --explicit > pkgs.txt`              |
| 从包列表文件创建环境                | `conda create --name NEWENV --file pkgs.txt`    |

## 使用包和频道

| 操作                   | 命令                                                          |
| ---------------------- | ------------------------------------------------------------- |
| 搜索包                 | `conda search PKGNAME=3.1 "PKGNAME [version='>=3.1.0,<3.2']"` |
| 使用 Anaconda 模糊搜索 | `anaconda search FUZZYNAME`                                   |
| 从指定频道安装包       | `conda install conda-forge::PKGNAME`                          |
| 安装指定版本包         | `conda install PKGNAME==3.1.4`                                |
| 安装多个可选版本之一   | `conda install "PKGNAME[version='3.1.2\|3.1.4']"`             |
| 安装版本区间内的包     | `conda install "PKGNAME>2.5,<3.2"`                            |
| 添加频道               | `conda config --add channels CHANNELNAME`                     |

## 其他有用提示

| 操作                     | 命令                                                 |
| ------------------------ | ---------------------------------------------------- |
| 查看包详细信息           | `conda search PKGNAME --info`                        |
| 清理缓存                 | `conda clean --all`                                  |
| 从环境中删除包           | `conda uninstall PKGNAME --name ENVNAME`             |
| 更新环境中所有包         | `conda update --all --name ENVNAME`                  |
| 使用脚本安装（无需确认） | `conda install --yes PKG1 PKG2`                      |
| 测试 Conda 配置          | `conda config --show`、`conda config --show-sources` |

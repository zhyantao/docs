======
Conda
======

`Conda Cheatsheet <https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html>`_

快速开始
--------

- 确认 Conda 已经正常安装，检查版本： ``conda info``
- 更新 Conda 到最新版本： ``conda update -n base conda``
- 将 Conda 管理的所有 Packages 都更新到最新版本： ``conda update anaconda``
- **列出**\ 当前已有的环境：``conda env list``

配置工作环境
------------

- **创建**\ 新工作环境，并指定 Python 版本： ``conda create --name ENVNAME python=3.6``
- 激活一个 Conda 工作环境： ``conda activate ENVNAME``
- 激活本地磁盘存放的一个工作环境： ``conda activate /path/to/environment-dir``
- 取消激活当前工作环境： ``conda deactivate``
- 列出当前工作环境下的所有 Packages 及他们的版本： ``conda list``
- 列出指定工作环境的所有 Packages 及他们的版本： ``conda list --name ENVNAME``
- 列出当前工作环境的所有历史版本： ``conda list --revisions``
- 列出指定工作环境的所有历史版本： ``conda list --name ENVNAME --revisions``
- 将一个工作环境回退到之前的一个版本： ``conda install --name ENVNAME --revision REV_NUMBER``
- **删除**\ 一个工作环境： ``conda remove --name ENVNAME --all``

共享工作环境
------------

- 复制一个指定的工作环境： ``conda create --clone ENVNAME --name NEWENV``
- 导出一个工作环境到 YAML 文件中： ``conda env export --name ENVNAME > envname.yml``
- 根据 YAML 文件创建一个新的工作环境： ``conda env create --file envname.yml``
- 根据当前目录下的 environment.yml 文件创建一个新的工作环境： ``conda env create``
- 导出一个带有指定 Package 版本的工作环境到另一个操作系统： ``conda list --explicit > pkgs.txt``
- 根据指定的 Packages 版本创建一个新的工作环境： ``conda create --name NEWENV --file pkgs.txt``

使用 Packages 和 Channels
--------------------------

- 在当前 Channels 中查找 Package： ``conda search PKGNAME=3.1 "PKGNAME [version='>=3.1.0,<3.2']"``
- 使用 Anaconda 在当前 Channels 中查找 Package ：\ ``anaconda search FUZZYNAME``
- 从一个指定的 Channel 安装 Package ：\ ``conda install conda-forge::PKGNAME``
- 安装指定版本的 Package （3.1.4） :  ``conda install PKGNAME==3.1.4``
- 安装指定版本中的某一个版本（OR）： ``conda install "PKGNAME[version='3.1.2|3.1.4']"``
- 安装指定区间的所有版本（AND）： ``conda install "PKGNAME>2.5,<3.2"``
- 创建一个 Channel ：\ ``conda config --add channels CHANNELNAME``

其他有用的提示
--------------

- 查看 Package 版本的细节： ``conda search PKGNAME --info``
- 删除无用缓存文件（包含无用 Packages）： ``conda clean --all``
- 从一个工作环境中删除一个 Package ：\ ``conda uninstall PKGNAME --name ENVNAME``
- 更新一个工作环境中的所有 Packages ：\ ``conda update --all --name ENVNAME``
- 使用脚本文件运行命令： ``conda install --yes PKG1 PKG2``
- 测试 Conda 配置和服务： ``conda config --show 、conda config --show-sources``

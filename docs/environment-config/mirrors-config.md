
# 软件包及镜像源管理

本文提到的各种类型的源（比如 pip，npm，apt，yum），都可以通过国内一些公司或高校的镜像站中找到。比如常用的镜像站有：

- 阿里巴巴官方镜像站：<https://developer.aliyun.com/mirror/> 
- 腾讯软件源：<https://mirrors.cloud.tencent.com/>
- 网易开源镜像站：<http://uni.mirrors.163.com/>
- 清华大学开源软件镜像站：<https://mirrors.tuna.tsinghua.edu.cn/>
- 中科大镜像站：<http://mirrors.ustc.edu.cn/>
- 浙江大学开源镜像站：<http://mirrors.zju.edu.cn/>

## pip 源

镜像站中的 PyPI 即为 pip 源。pip 是 Python 包管理工具，该工具提供了对 Python 包的查找、下载、安装、卸载的功能。


（1）**永久使用国内镜像源**：Windows 用户修改文件 `C:\Users\%USERNAME%\pip\pip.ini`（如果没有则新建），
Linux 用户修改文件 `~/.config/pip/pip.conf`（如果没有则新建），然后在相关文件中添加如下内容。
注意，`trusted-host` 非必须，使用时提示不受信任可添加 `--trusted-host=mirrors.aliyun.com`。

```bash
[global]
index-url=http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
```

（2）**临时使用国内镜像源**，只需要在命令后面加上 `-i` 参数：

```bash
pip install pythonModuleName -i https://mirror.baidu.com/pypi/simple
```

```{admonition} 其他公司或高校提供的镜像源
:class: dropdown

- 官方源：<https://pypi.python.org/pypi>
- 豆瓣源：<https://pypi.doubanio.com/simple/>
- 阿里云源：<http://mirrors.aliyun.com/pypi/simple/>
- 中科大源：<https://mirrors.ustc.edu.cn/pypi/web/simple/>
- 百度源：<https://mirror.baidu.com/pypi/simple>
- 清华源：<https://pypi.tuna.tsinghua.edu.cn/simple/>
- 更多：<https://blog.csdn.net/u011433858/article/details/80398947>
```

（3）**离线安装第三方库**。从 <https://pypi.org/> 搜索相应的版本并下载。
使用如下命令进行安装。

```bash
pip install /path/to/file.whl
```

（4）**如果使用的是 conda 管理各个版本的 Python**，可以修改文件
`C:\Users\%USERNAME%\.condarc`（如果没有则新建），添加如下内容：

```bash
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```

## apt/yum 源

不同的 Linux 系统提供了不同的软件包管理器，其中典型的两种是：

- 高级打包工具（英语：Advanced Packaging Tools，缩写为 APT）
- YUM（全称为 Yellow dog Updater, Modified）

软件包管理器可以自动地下载、配置、安装、卸载自家的软件包，比如 deb 和 rpm。
软件包管理器会自动地处理软件包之间的依赖关系，给用户提供了极大方便。

更新镜像源后，不要忘记更新缓存：

```bash
sudo apt-get clean all
sudo apt-get update
```

从镜像源中**获取不到**的软件安装包，可以从 <https://pkgs.org/> 查一下，然后用离线的方式安装。
Ubuntu 用 dpkg 命令安装，CentOS 用 rpm 命令安装。

当然，你也可以选择使用下载**源代码的方式安装**：

```bash
./configure --prefix=/path/to/install/
make
sudo make install
```

## npm 源

npm 是 JavaScript 世界的包管理工具，并且是 Node.js 平台的默认包管理工具。
通过 npm 可以安装、共享、分发代码，管理项目依赖关系。默认源是 <https://www.npmjs.com/>。

（1）**临时改变镜像源**

```bash
# 方法一：通过 config 命令
npm config set registry http://registry.cnpmjs.org
npm info express

# 方法二：通过 npm 命令
npm --registry http://registry.cnpmjs.org info express
```

（2）**永久修改镜像源**

1. 打开配置文件：`~/.npmrc`
2. 写入配置：`registry=https://registry.npm.taobao.org`


## 制作本地源

1. 安装好 Linux 操作系统
2. 将安装镜像 iso 文件上传至虚拟机任意目录
3. 使用如下命令完成后续操作：

```bash
mkdir /dev/local_CentOS
mount -o loop /home/CentOS-6.10-x86_64-bin-DVD1.iso /dev/local_CentOS/
mkdir /mnt/local_yum
cp -r /dev/local_CentOS/* /mnt/local_yum
cd /etc/yum.repos.d/
rename .repo .repo.bak *.repo
cp CentOS-Base.repo.bak CentOS_local.repo
cp CentOS-Media.repo.bak CentOS-local.repo
vim CentOS-local.repo 
yum clean all
yum repolist
umount /dev/local_CentOS
rm /dev/local_CentOS/ -rf
```

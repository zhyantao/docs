# Mirrors

## apt/yum 源

软件包管理器 apt 和 yum 可以自动地下载、配置、安装、卸载自家的软件包，分别对应 `.deb` 和 `.rpm`。软件包管理器会自动地处理软件包之间的依赖关系，给用户提供了极大方便。

如果使用的是 macOS，对应的 ARM64 架构，需要使用 ubuntu-ports，参考 <https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu-ports/>。

**(1) 以 Ubuntu 为例，更新镜像源**

::::{tab-set}
:::{tab-item} 阿里云源

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo tee /etc/apt/sources.list <<EOF
deb https://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

# deb https://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
# deb-src https://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
EOF
```

:::
:::{tab-item} 清华源

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo tee /etc/apt/sources.list <<EOF
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse

deb http://security.ubuntu.com/ubuntu/ focal-security main restricted universe multiverse
# deb-src http://security.ubuntu.com/ubuntu/ focal-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
# # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
EOF
```

:::
:::{tab-item} 腾讯源

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo tee /etc/apt/sources.list <<EOF
deb http://mirrors.cloud.tencent.com/ubuntu/ focal main restricted universe multiverse
deb http://mirrors.cloud.tencent.com/ubuntu/ focal-security main restricted universe multiverse
deb http://mirrors.cloud.tencent.com/ubuntu/ focal-updates main restricted universe multiverse
#deb http://mirrors.cloud.tencent.com/ubuntu/ focal-proposed main restricted universe multiverse
#deb http://mirrors.cloud.tencent.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.cloud.tencent.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.cloud.tencent.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.cloud.tencent.com/ubuntu/ focal-updates main restricted universe multiverse
#deb-src http://mirrors.cloud.tencent.com/ubuntu/ focal-proposed main restricted universe multiverse
#deb-src http://mirrors.cloud.tencent.com/ubuntu/ focal-backports main restricted universe multiverse
EOF
```

:::
:::{tab-item} 中科大源

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo tee /etc/apt/sources.list <<EOF
# 默认注释了源码仓库，如有需要可自行取消注释
deb https://mirrors.ustc.edu.cn/ubuntu/ focal main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal main restricted universe multiverse

deb https://mirrors.ustc.edu.cn/ubuntu/ focal-security main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-security main restricted universe multiverse

deb https://mirrors.ustc.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-updates main restricted universe multiverse

deb https://mirrors.ustc.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-backports main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.ustc.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
EOF
```

:::
:::{tab-item} 浙大源

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo tee /etc/apt/sources.list <<EOF
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.zju.edu.cn/ubuntu/ focal main restricted universe multiverse
# deb-src https://mirrors.zju.edu.cn/ubuntu/ focal main restricted universe multiverse
deb https://mirrors.zju.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
# deb-src https://mirrors.zju.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
deb https://mirrors.zju.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
# deb-src https://mirrors.zju.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
deb https://mirrors.zju.edu.cn/ubuntu/ focal-security main restricted universe multiverse
# deb-src https://mirrors.zju.edu.cn/ubuntu/ focal-security main restricted universe multiverse
# 预发布软件源，不建议启用
# deb https://mirrors.zju.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
# deb-src https://mirrors.zju.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
EOF
```

:::
:::{tab-item} 网易源

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo tee /etc/apt/sources.list <<EOF
deb http://mirrors.163.com/ubuntu/ focal main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ focal-security main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ focal-updates main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ focal-proposed main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ focal-backports main restricted universe multiverse
EOF
```

:::
::::

:::{dropdown} 切换 Ubuntu 版本或找不到安装包

如要用于其他版本，把 `focal` 换成其他版本代号即可: 22.04：`jammy`；20.04：`focal`；18.04：`bionic`；16.04：`xenial`；14.04：`trusty`。

若官方源找不到安装包，有两种方法可以解决这个问题：

- 从 <https://pkgs.org/> 下载，手动安装：Ubuntu 用 `dpkg` 命令安装，CentOS 用 `rpm` 命令安装。
- 从源代码的安装：

```bash
./configure --prefix=/path/to/install/
make
sudo make install
```

:::

**(2) 更新缓存**

```bash
sudo apt-get clean all
sudo apt-get update
```

**(3) 卸载软件**

如果使用 `apt` 命令安装了软件，卸载软件的方式如下：

::::{tab-set}
:::{tab-item} 卸载 APP

```bash
sudo apt-get remove <package_name>
```

:::
:::{tab-item} 卸载 APP 和依赖

```bash
sudo apt-get -y autoremove <package_name>
```

:::
:::{tab-item} 删除用户数据

```bash
sudo apt-get -y purge <package_name>
```

:::
:::{tab-item} 卸载 APP 和依赖并删除用户数据

```bash
sudo apt-get -y autoremove --purge <package_name>
```

:::
::::

## pip 源

`pip` 是 Python 包管理工具，该工具提供了对 Python 包的查找、下载、安装、卸载的功能。

**(1) 永久切换镜像源**

::::::{tab-set}
:::::{tab-item} Linux
::::{tab-set}
:::{tab-item} 阿里云源

```bash
mkdir -p ~/.config/pip
tee ~/.config/pip/pip.conf <<EOF
[global]
index-url=http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
EOF
```

:::
:::{tab-item} 清华源

```bash
mkdir -p ~/.config/pip
tee ~/.config/pip/pip.conf <<EOF
[global]
index-url=https://pypi.tuna.tsinghua.edu.cn/simple/
[install]
trusted-host=pypi.tuna.tsinghua.edu.cn
EOF
```

:::
:::{tab-item} 百度源

```bash
mkdir -p ~/.config/pip
tee ~/.config/pip/pip.conf <<EOF
[global]
index-url=https://mirror.baidu.com/pypi/simple
[install]
trusted-host=mirror.baidu.com
EOF
```

:::
:::{tab-item} 中科大源

```bash
mkdir -p ~/.config/pip
tee ~/.config/pip/pip.conf <<EOF
[global]
index-url=https://mirrors.ustc.edu.cn/pypi/web/simple/
[install]
trusted-host=mirrors.ustc.edu.cn
EOF
```

:::
:::{tab-item} 豆瓣源

```bash
mkdir -p ~/.config/pip
tee ~/.config/pip/pip.conf <<EOF
[global]
index-url=https://pypi.doubanio.com/simple/
[install]
trusted-host=pypi.doubanio.com
EOF
```

:::
:::{tab-item} 官方源

```bash
mkdir -p ~/.config/pip
tee ~/.config/pip/pip.conf <<EOF
[global]
index-url=https://pypi.python.org/pypi
[install]
trusted-host=pypi.python.org
EOF
```

:::
::::
:::::
:::::{tab-item} Windows
::::{tab-set}
:::{tab-item} 阿里云源

```powershell
New-Item -ItemType Directory -Path $HOME\pip -Force
$iniContent = @"
[global]
index-url=http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
"@
$iniContent | Add-Content -Path ($HOME + "\pip\pip.ini") -PassThru | Out-Host
```

:::
:::{tab-item} 清华源

```powershell
New-Item -ItemType Directory -Path $HOME\pip -Force
$iniContent = @"
[global]
index-url=https://pypi.tuna.tsinghua.edu.cn/simple/
[install]
trusted-host=pypi.tuna.tsinghua.edu.cn
"@
$iniContent | Add-Content -Path ($HOME + "\pip\pip.ini") -PassThru | Out-Host
```

:::
:::{tab-item} 百度源

```powershell
New-Item -ItemType Directory -Path $HOME\pip -Force
$iniContent = @"
[global]
index-url=https://mirror.baidu.com/pypi/simple
[install]
trusted-host=mirror.baidu.com
"@
$iniContent | Add-Content -Path ($HOME + "\pip\pip.ini") -PassThru | Out-Host
```

:::
:::{tab-item} 中科大源

```powershell
New-Item -ItemType Directory -Path $HOME\pip -Force
$iniContent = @"
[global]
index-url=https://mirrors.ustc.edu.cn/pypi/web/simple/
[install]
trusted-host=mirrors.ustc.edu.cn
"@
$iniContent | Add-Content -Path ($HOME + "\pip\pip.ini") -PassThru | Out-Host
```

:::
:::{tab-item} 豆瓣源

```powershell
New-Item -ItemType Directory -Path $HOME\pip -Force
$iniContent = @"
[global]
index-url=https://pypi.doubanio.com/simple/
[install]
trusted-host=pypi.doubanio.com
"@
$iniContent | Add-Content -Path ($HOME + "\pip\pip.ini") -PassThru | Out-Host
```

:::
:::{tab-item} 官方源

```powershell
New-Item -ItemType Directory -Path $HOME\pip -Force
$iniContent = @"
[global]
index-url=https://pypi.python.org/pypi
[install]
trusted-host=pypi.python.org
"@
$iniContent | Add-Content -Path ($HOME + "\pip\pip.ini") -PassThru | Out-Host
```

:::
::::
:::::
::::::

**(2) requirements.txt**

导出 `requirements.txt` 中列出的软件包，对应在本机上已经安装的版本号：

```bash
while IFS= read -r line || [[ -n $line ]]; do
    package=$(echo "$line" | awk -F '==' '{print $1}')
    required_version=$(echo "$line" | awk '{print $2}')
    installed_version=$(pip show "$package" 2>/dev/null | grep Version | awk -F': ' '{print $2}' | tr -d '[:space:]')
    if [[ -n "$installed_version" ]]; then
        echo "$package==$installed_version"
    else
        echo "$package is not installed."
    fi
done <requirements.txt
```

**(3) 第三方镜像源**

若官方源找不到安装包，从 <https://pypi.org/> 下载版本后，使用下面的命令安装：

```bash
pip install /path/to/file.whl
```

**(4) Conda 管理安装包**

::::{tab-set}
:::{tab-item} Linux / macOS

```bash
tee ~/.condarc <<EOF
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
EOF
```

:::
:::{tab-item} Windows

```powershell
New-Item -ItemType Directory -Path $HOME\.condarc -Force
$iniContent = @"
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
"@
$iniContent | Add-Content -Path ($HOME + "\.condarc") -PassThru | Out-Host
```

:::
::::

## Python 源

使用 [deadsnakes](https://github.com/deadsnakes)，可以在 Linux 上轻松地安装多个 Python 版本：

```bash
# 添加 PPA (Personal Package Archives) 源，此源可安装多个 Python 版本
sudo add-apt-repository ppa:deadsnakes/ppa

# 制定需要安装的 Python 版本号
PYTHON_VERSION=python3.13

# 安装另一个版本的 Python
sudo apt install $PYTHON_VERSION $PYTHON_VERSION-dev \
    $PYTHON_VERSION-venv $PYTHON_VERSION-distutils \
    $PYTHON_VERSION-lib2to3 $PYTHON_VERSION-gdbm \
    $PYTHON_VERSION-tk

# 使用新版本的 Python
mkdir -p ~/venv
$PYTHON_VERSION -m venv ~/venv/$PYTHON_VERSION --without-pip
source ~/venv/$PYTHON_VERSION/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | $PYTHON_VERSION
```

## MSYS2 源

::::{tab-set}
:::{tab-item} 中科大源

```bash
# modify config files
sed -i "s#mirror.msys2.org/#mirrors.ustc.edu.cn/msys2/#g" /etc/pacman.d/mirrorlist*

# verify the modification
head -n 6 /etc/pacman.d/mirrorlist.msys

# clear cache
pacman -Scc

# update mirrors
pacman -Sy
```

:::
:::{tab-item} 清华源

```bash
# modify config files
sed -i "s#mirror.msys2.org/#mirrors.tuna.tsinghua.edu.cn/msys2/#g" /etc/pacman.d/mirrorlist*

# verify the modification
head -n 6 /etc/pacman.d/mirrorlist.msys

# clear cache
pacman -Scc

# update mirrors
pacman -Syu
```

:::
::::

## npm 源

`npm` 是 JavaScript 世界的包管理工具，并且是 Node.js 平台的默认包管理工具。
通过 `npm` 可以安装、共享、分发代码，管理项目依赖关系。默认源是 <https://www.npmjs.com/>。

```bash
sudo apt install npm
sudo npm install n -g

# 设置淘宝镜像源
npm config set registry https://registry.npmmirror.com
```

升级或降级到指定版本的 `npm` 和 `nodejs`

```bash
# 升级到最新版本
sudo npm install -g npm@latest
sudo n latest

# 降级到指定版本
sudo npm install npm@8.1.2 -g
sudo n v16.13.2
```

## Maven 源

如果使用 IDEA 默认的国外镜像源比较慢（会导致下载 Maven Wrapper 失败），可尝试使用国内镜像源：

- 阿里云：<https://developer.aliyun.com/mirror/>
- 腾讯云：<https://mirrors.cloud.tencent.com/>
- 网易 163：<http://uni.mirrors.163.com/>

编辑或新建 `C:\Users\%USERNAME%\.m2\settings.xml`，文件内容如下（使用阿里云镜像）：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.2.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.2.0
                              https://maven.apache.org/xsd/settings-1.2.0.xsd">
  <mirrors>
    <mirror>
      <id>aliyunmaven</id>
      <mirrorOf>*</mirrorOf>
      <name>阿里云公共仓库</name>
      <url>https://maven.aliyun.com/repository/public</url>
    </mirror>
  </mirrors>
  <profiles>
    <profile>
      <id>jdk-1.8</id>
      <activation>
        <jdk>1.8</jdk>
      </activation>
      <repositories>
        <repository>
          <id>spring</id>
          <url>https://maven.aliyun.com/repository/spring</url>
          <releases><enabled>true</enabled></releases>
          <snapshots><enabled>true</enabled></snapshots>
        </repository>
      </repositories>
    </profile>
  </profiles>
</settings>
```

## Docker 源

1、为 Ubuntu 系统配置 Docker 仓库源与镜像加速

::::{tab-set}
:::{tab-item} 中科大源
:sync: ustc

```bash
# 设置 GPG 公钥
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 设置 Docker 仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

:::
:::{tab-item} 阿里云源
:sync: aliyun

```bash
# 设置 GPG 公钥
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 设置 Docker 仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

:::
:::{tab-item} 清华源
:sync: tuna

```bash
# 设置 GPG 公钥
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 设置 Docker 仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

:::
::::

2、为 Docker 配置镜像加速器

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.mirrors.sjtug.sjtu.edu.cn",
    "https://mirror.baidubce.com",
    "http://hub-mirror.c.163.com"
  ]
}
EOF

sudo systemctl restart docker
sudo docker info
```

3、为 Containerd 配置镜像加速端点

```bash
sudo tee /etc/containerd/config.toml <<EOF
[plugins."io.containerd.grpc.v1.cri".registry]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
    [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
      endpoint = [
        "https://docker.m.daocloud.io",
        "https://docker.mirrors.sjtug.sjtu.edu.cn",
        "https://mirror.baidubce.com",
        "http://hub-mirror.c.163.com"
      ]
EOF

sudo systemctl daemon-reload
sudo systemctl restart containerd
```

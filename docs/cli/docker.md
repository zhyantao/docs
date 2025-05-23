# Docker

## 删除旧版本

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc
do
  sudo apt-get remove $pkg
done
```

:::
::::

## 安装 Docker

```bash
sudo apt-get install apt-transport-https \
  ca-certificates \
  curl \
  software-properties-common \
  docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 验证 Docker 是否安装成功

```bash
sudo docker run hello-world
```

## 卸载 Docker

```bash
sudo apt-get purge docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

## 列出本地所有镜像

```bash
docker images
```

## 删除镜像

```bash
# 删除指定镜像
docker image rm <镜像名称>:<标签名>

# 只删除 <none> 标签的镜像
docker image rm -f $(docker images | grep '<none>' | awk '{print $3}')

# 无提示地删除所有没有被至少一个容器使用的镜像（慎用）
docker image prune -a -f
```

## 删除容器

```bash
# 删除指定容器
docker rm -f <容器 ID>

# 删除状态为 Exited 的容器
docker rm $(docker ps -a | grep Exited | awk '{print $1}')

# 强制删除正在运行的容器（慎用）
docker rm -f $(docker ps -a | grep Exited | awk '{print $1}')
```

## 交互式启动容器

以交互模式启动一个容器并进入其 shell 环境：

```bash
docker run -it ubuntu:20.04 /bin/bash
```

对于没有安装 bash 的镜像（如 Alpine）：

```bash
docker run -it alpine sh
```

## 查看运行中的容器

```bash
docker ps
```

查看所有容器（包括停止的）：

```bash
docker ps -a
```

## 构建镜像

从当前目录下的 `Dockerfile` 构建镜像：

```bash
docker build -t <镜像名称>:<标签名> .
```

## 推送镜像到私有仓库

```bash
docker tag <镜像名称>:<标签名> <Registry-URL>/<镜像名称>:<标签名>
docker push <Registry-URL>/<镜像名称>:<标签名>
```

## 下载镜像

```bash
# 从制定 Docker Registry 拉取镜像
docker pull <Registry-URL>/<镜像名称>:<标签名>

# 示例
docker pull myregistry.com/ubuntu:20.04
```

## 离线安装 Git 到现有镜像

```bash
# 确保 apt 源与 Docker 容器中的 Ubuntu 版本保持一致
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo vim /etc/apt/sources.list <<EOF
deb https://mirrors.ustc.edu.cn/ubuntu/ focal main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ focal-security main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
EOF
sudo apt-get clean all
sudo apt-get update

# 下载 deb 文件
PKGNAME="build-essential git"
apt-get download $(apt-cache depends --recurse --no-recommends \
  --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances \
  $PKGNAME | grep "^\w" | sort -u)

# 将 Git 安装包目录（绝对路径）挂载到 /mnt 目录
docker run -v $PWD:/mnt -it ubuntu:20.04 /bin/bash

# 在容器内，进入挂载点并开始安装
cd /mnt
dpkg -i *.deb

# 强制重新配置未正确配置的软件包
dpkg --configure -a
dpkg -i *.deb

# 保存当前容器的状态（假设容器正在运行），并制作新的镜像
docker ps
docker commit <容器 ID> <新镜像名称>:<标签名>
```

离线安装时，一些常见的错误：

```bash
#
# dpkg: error: duplicate file trigger interest for filename
#
mv /var/lib/dpkg/triggers/File /var/lib/dpkg/triggers/File.bak
apt-get --fix-broken install
dpkg -i *.deb
```

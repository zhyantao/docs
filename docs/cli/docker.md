# Docker

## 删除旧版本

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc
do
  sudo apt-get remove $pkg
done
```

## 设置 Docker 源

::::{tab-set}
:::{tab-item} 中科大源
:sync: ustc

```bash
# 设置 GPG 公钥
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 设置 Docker 仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
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
sudo curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 设置 Docker 仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
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
sudo curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 设置 Docker 仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
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

## Docker Registry 加速服务

```{warning}
使用国内的 Docker Hub 镜像前，必须准备一个该镜像站对应的账号和密码，否则将无法通过该源加速。因此，使用无效源时，会被重定向到 [`https://registry-1.docker.io/v2/`](https://registry-1.docker.io/v2/)。
```

::::::{tab-set}
:::::{tab-item} 中科大源
:sync: ustc

```{error}
科大 Docker Hub 不对校外开放，因此无法使用科大源。
```

::::{tab-set}
:::{tab-item} Docker v2

```bash
sudo docker login docker.mirrors.ustc.edu.cn
```

:::
:::{tab-item} Docker v1

```bash
sudo mkdir -p ~/.docker
cat <<EOF | sudo tee ~/.docker/config.json
{
  "auths": {
    "https://docker.mirrors.ustc.edu.cn" : {
      "auth": "put-your-auth-code-here",
      "email": "put-your-email-here"
    }
  }
}
EOF
```

:::
::::

```bash
if [ -f "/etc/docker/daemon.json" ]
then
echo "/etc/docker/daemon.json already exists, please modify it manually."
else
sudo mkdir -p /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
}
EOF
fi

sudo systemctl restart docker
sudo docker info
```

:::::
:::::{tab-item} 阿里云源
:sync: aliyun

```{error}
阿里云 Docker Hub 下架了，因此无法使用阿里云源。
```

::::{tab-set}
:::{tab-item} Docker v2

```bash
username=
sudo docker login $username.mirror.aliyuncs.com
```

:::
:::{tab-item} Docker v1

```bash
sudo mkdir -p ~/.docker
username=
cat <<EOF | sudo tee ~/.docker/config.json
{
  "auths": {
    "https://$username.mirror.aliyuncs.com" : {
      "auth": "put-your-auth-code-here",
      "email": "put-your-email-here"
    }
  }
}
EOF
```

:::
::::

```bash
if [ -f "/etc/docker/daemon.json" ]
then
echo "/etc/docker/daemon.json already exists, please modify it manually."
else
sudo mkdir -p /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "registry-mirrors": ["https://$username.mirror.aliyuncs.com"]
}
EOF
fi

sudo systemctl restart docker
sudo docker info
```

:::::
:::::{tab-item} 清华源
:sync: tuna

```{error}
清华 Docker Hub 不对校外开放，因此无法使用清华源。
```

::::{tab-set}
:::{tab-item} Docker v2

```bash
sudo docker login docker.mirrors.tuna.tsinghua.edu.cn
```

:::
:::{tab-item} Docker v1

```bash
sudo mkdir -p ~/.docker
cat <<EOF | sudo tee ~/.docker/config.json
{
  "auths": {
    "https://docker.mirrors.tuna.tsinghua.edu.cn" : {
      "auth": "put-your-auth-code-here",
      "email": "put-your-email-here"
    }
  }
}
EOF
```

:::
::::

```bash
if [ -f "/etc/docker/daemon.json" ]
then
echo "/etc/docker/daemon.json already exists, please modify it manually."
else
sudo mkdir -p /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "registry-mirrors": ["https://docker.mirrors.tuna.tsinghua.edu.cn"]
}
EOF
fi

sudo systemctl restart docker
sudo docker info
```

:::::
::::::

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

## 删除无效的镜像

```bash
# 清理 <none> 标签的悬空镜像（推荐方式）
docker image prune -a -f

# 只删除 <none> 标签的镜像
docker rmi -f $(docker images | grep '<none>' | awk '{print $3}')

# 删除状态为 Exited 的容器
docker rm $(docker ps -a | grep Exited | awk '{print $1}')

# 强制删除正在运行的容器（慎用）
docker rm -f $(docker ps -a | grep Exited | awk '{print $1}')
```

## 列出所有镜像

```bash
# 列出本地已有的所有镜像
docker images

# 查看更详细的镜像信息（如创建时间、大小等）
docker images --no-trunc

# 格式化输出
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}"
```

## 删除指定镜像

```bash
# 删除一个或多个特定镜像
docker image rm 192.168.163.146:5000/python3action:1.0.0
docker image rm openwhisk/action-python-v3.7:1.17.0
```

如果该镜像已被某个容器使用，则需先删除相关容器才能成功删除镜像。你可以通过以下命令查找使用该镜像的容器：

```bash
docker ps -a --filter "ancestor=镜像名" --format "{{.ID}}"
```

然后删除这些容器：

```bash
docker rm -f <container_id>
```

## 交互式启动镜像

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
docker build -t my-image:latest .
```

## 推送镜像到私有仓库

```bash
docker tag my-image:latest registry.example.com/my-image:latest
docker push registry.example.com/my-image:latest
```

## 下载镜像

```bash
# 从制定 Docker Registry 拉取镜像
docker pull <Registry-URL>/<Repository>:<Tag>

# 示例
docker pull myregistry.com/ubuntu:20.04
```

## 将 git 离线添加到现有镜像

```bash
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

# 如果遇到未解决的依赖关系，可以尝试使用以下命令修复（假设有本地 deb 包可满足这些依赖）
apt-get install -f
```

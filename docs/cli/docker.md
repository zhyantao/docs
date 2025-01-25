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
# 清理 <none> 容器
docker image prune -f
docker rmi -f $(docker images | grep '<none>' | awk '{print $3}')

# 清理异常退出的容器
docker rm $(docker ps -a | grep Exited | awk '{print $1}')
```

## 列出所有镜像

```bash
docker images
```

## 删除指定镜像

```bash
docker image rm 192.168.163.146:5000/python3action:1.0.0
docker image rm openwhisk/action-python-v3.7:1.17.0
```

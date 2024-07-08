# Docker

## 删除旧版本

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

## 设置 Docker 源

```bash
# 设置 GPG 公钥
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 设置 Docker 仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# 替换 Docker Register 服务（加速镜像下载）
sudo mkdir -p /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "registry-mirrors": ["https://mirrors.ustc.edu.cn"]
}
EOF
#sudo systemctl restart docker
```

## 安装 Docker

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 验证 Docker 是否安装成功

```bash
sudo docker run hello-world
```

## 卸载 Docker

```bash
sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
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

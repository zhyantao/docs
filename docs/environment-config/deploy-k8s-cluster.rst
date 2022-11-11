=====================
部署 Kubernetes 集群
=====================

下载并安装 Ubuntu 22.04：https://www.releases.ubuntu.com/22.04/

.. warning::

    以 2 个节点为例，创建集群：（一个 master 节点，一个 node 节点）

    - ``uname -a``：集群内每个节点必须为 x86 架构（\ :ref:`不支持 ARM 架构 <training-with-gpu>`\ ）。
    - ``lscpu``：最少 2 核处理器。
    - ``free -mh``：最小 2GB 内存。
    - ``vim /etc/hostname`` 修改 hostname，使集群内每个节点的 hostname 不同。
    - ``vim /etc/hosts``：添加地址映射，使集群内网络互通。
    - ``ping <hostname>``：集群内各节点网络可以互联。
    - ``ip link``：集群内每个节点的网络接口的 MAC 地址不同。
    - ``sudo cat /sys/class/dmi/id/product_uuid``：集群内每个节点的 product_uuid 不同。
    
    确保网络通畅的——这听起来像是废话，但确实有相当一部分的云主机不对
    SELinux、iptables、安全组、防火墙进行设置的话，内网各个节点之间、与外网之间会存在默认的访问障碍，导致部署失败。


安装容器运行时：Docker Engine
-----------------------------

本节内容参考：https://docs.docker.com/engine/install/ubuntu/

删除 Docker 的旧版本
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    su
    apt-get remove docker docker-engine docker.io containerd runc


使用仓库安装 Docker
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    apt-get update
    apt-get install ca-certificates curl gnupg lsb-release software-properties-common
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null


安装最新版的 Docker 引擎
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    apt-get update
    apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin


测试 Docker 是否安装成功
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo docker run hello-world


使 Docker 命令自动补全
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    echo 'source /usr/share/bash-completion/completions/docker' >> ~/.bashrc


让 Docker 能够开机启动
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    systemctl enable docker
    systemctl start docker


安装 Docker-Compose
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    apt-get install docker-compose-plugin


安装 cri-dockerd 适配器
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    git clone https://github.com/Mirantis/cri-dockerd.git

    sudo apt-get install golang-go

    cd cri-dockerd
    mkdir bin
    go build -o bin/cri-dockerd
    mkdir -p /usr/local/bin
    sudo install -o root -g root -m 0755 bin/cri-dockerd /usr/local/bin/cri-dockerd
    sudo cp -a packaging/systemd/* /etc/systemd/system
    sudo sed -i -e 's,/usr/bin/cri-dockerd,/usr/local/bin/cri-dockerd,' /etc/systemd/system/cri-docker.service
    sudo systemctl daemon-reload
    sudo systemctl enable cri-docker.service
    sudo systemctl enable --now cri-docker.socket

    #cd cri-dockerd && mkdir bin
    #VERSION=$((git describe --abbrev=0 --tags | sed -e 's/v//') || echo $(cat VERSION)-$(git log -1 --pretty='%h')) PRERELEASE=$(grep -q dev <<< "${VERSION}" && echo "pre" || echo "") REVISION=$(git log -1 --pretty='%h')
    #go build -ldflags="-X github.com/Mirantis/cri-dockerd/version.Version='$VERSION}' -X github.com/Mirantis/cri-dockerd/version.PreRelease='$PRERELEASE' -X github.com/Mirantis/cri-dockerd/version.BuildTime='$BUILD_DATE' -X github.com/Mirantis/cri-dockerd/version.GitCommit='$REVISION'" -o cri-dockerd


使用 Minikube 创建单点集群
--------------------------

本节内容参考：https://minikube.sigs.k8s.io/docs/start/


关闭 master 节点的交换分区
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    yes | cp /etc/fstab /etc/fstab_bak
    cat /etc/fstab_bak | grep -v swap > /etc/fstab
    reboot
    systemctl daemon-reload
    systemctl restart docker


安装 kubeadm、kubelet 和 kubectl
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    # sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    apt-get update
    apt-get install -y apt-transport-https ca-certificates curl

    # 切换国内源：http://mirrors.ustc.edu.cn/kubernetes/
    #apt-get update && apt-get install -y apt-transport-https
    curl http://mirrors.ustc.edu.cn/kubernetes/apt/doc/apt-key.gpg | apt-key add -
    curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg http://mirrors.ustc.edu.cn/kubernetes/apt/doc/apt-key.gpg
    cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
    deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] http://mirrors.ustc.edu.cn/kubernetes/apt/ kubernetes-xenial main
    EOF
    apt-get update

    apt-get install -y kubelet kubeadm kubectl

    # echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
    
    apt-mark hold kubelet kubeadm kubectl


初始化集群控制平面
~~~~~~~~~~~~~~~~~~

.. code-block:: bash 

    #kubeadm init --pod-network-cidr=10.244.0.0/16
    rm -rf /etc/containerd/config.toml
    systemctl restart containerd
    swapoff -a
    kubeadm init --pod-network-cidr=10.244.0.0/16
    #systemctl enable kubelet
    #systemctl restart kubelet

配置 cgroup 驱动
~~~~~~~~~~~~~~~~~

查看 Dokcer 驱动：``docker info | grep Driver``


安装 Minikube
~~~~~~~~~~~~~~

.. code-block:: bash

    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube


创建单点集群
~~~~~~~~~~~~

.. code-block:: bash

    sudo usermod -aG docker $USER && newgrp docker
    minikube config set driver docker
    minikube start --driver=docker


使用 kubeadm 创建生产集群
-------------------------

允许 iptables 检查桥接流量
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
    br_netfilter
    EOF

    cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
    net.bridge.bridge-nf-call-ip6tables = 1
    net.bridge.bridge-nf-call-iptables = 1
    EOF

    sudo sysctl --system


安装 kubeadm、kubelet 和 kubectl
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
    [kubernetes]
    name=Kubernetes
    baseurl=http://mirrors.ustc.edu.cn/kubernetes/yum/repos/kubernetes-el7-x86_64/
    enabled=1
    gpgcheck=1
    repo_gpgcheck=1
    gpgkey=http://mirrors.ustc.edu.cn/kubernetes/yum/doc/yum-key.gpg http://mirrors.ustc.edu.cn/kubernetes/yum/doc/rpm-package-key.gpg
    exclude=kubelet kubeadm kubectl
    EOF

    sudo setenforce 0
    sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

    sudo yum install -y --nogpgcheck kubelet kubeadm kubectl --disableexcludes=kubernetes

    sudo systemctl enable --now kubelet


初始化集群前的准备工作：关闭 Swap 分区
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 临时关闭Swap分区

.. code-block:: bash

    sudo swapoff -a
    echo "KUBELET_EXTRA_ARGS=--fail-swap-on=false" >> /etc/sysconfig/kubelet

- 永久关闭Swap分区

.. code-block:: bash

    yes | sudo cp /etc/fstab /etc/fstab_bak
    sudo cat /etc/fstab_bak | grep -v swap > /etc/fstab


修改 Docker 的驱动，使其与 K8s 的 cgroups 保持一致
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    cat <<EOF | sudo tee /etc/docker/daemon.json
    {
        "exec-opts": ["native.cgroupdriver=systemd"]
    }
    EOF

    systemctl daemon-reload
    systemctl restart docker


使 kubelet 开机启动
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    systemctl start kubelet
    systemctl enable kubelet


后续操作仅 master 节点需要运行
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


初始化集群控制平面
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    kubeadm init \
        --pod-network-cidr=10.244.0.0/16 \
        --image-repository registry.aliyuncs.com/google_containers \
        --apiserver-advertise-address <NET_INTERFACE_IP>

.. note:: 注意保持版本号的一致性，修改 ``NET_INTERFACE_IP`` 为本机的 ``IP`` 地址。


切换至需要配置的用户后，为当前用户生成 kubeconfig
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config

安装 CNI 插件
^^^^^^^^^^^^^^

.. code-block:: bash

    curl --insecure -sfL https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml | kubectl apply -f -

移除 master 节点上的污点
^^^^^^^^^^^^^^^^^^^^^^^^

参考连接：https://icyfenix.cn/

.. code-block:: bash

    kubectl taint nodes --all node-role.kubernetes.io/master-

启用 kubectl 的自动补全功能
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    echo 'source <(kubectl completion bash)' >> ~/.bashrc
    echo 'source /usr/share/bash-completion/bash_completion' >> ~/.bashrc

生成 token
^^^^^^^^^^^^

.. note::

    把下面这条命令的输出，在需要加入当前集群的节点上运行一次，即可完成集群的横向扩展。

.. code-block:: bash

    kubeadm token create --print-join-command


查看当前集群中节点的信息
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    kubectl cluster-info
    kubectl get nodes

=====================
部署 Kubernetes 集群
=====================

下载并安装 CentOS 7：http://isoredirect.centos.org/centos/7/isos/x86_64/

.. warning::

    以 3 个节点为例，创建集群：（一个 master 节点，两个 node 节点）

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
------------------------------

删除 Docker 的旧版本
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo yum remove docker \
        docker-client \
        docker-client-latest \
        docker-common \
        docker-latest \
        docker-latest-logrotate \
        docker-logrotate \
        docker-engine


使用仓库安装 Docker（推荐）
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo yum install -y yum-utils

    sudo yum-config-manager \
        --add-repo https://download.docker.com/linux/centos/docker-ce.repo


更新系统软件仓库
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo yum update


安装最新版的 Docker 引擎
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo yum install docker-ce docker-ce-cli containerd.io


测试 Docker 是否安装成功
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo docker run hello-world


Docker 命令自动补全
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    echo 'source /usr/share/bash-completion/completions/docker' >> ~/.bashrc


让 Docker 能够开机启动
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo systemctl enable docker
    sudo systemctl start docker


安装 Docker-Compose
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo curl -L "https://get.daocloud.io/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose


使用 kubeadm 创建生产集群
--------------------------

初始化集群前的准备工作
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # 永久关闭Swap分区
    yes | sudo cp /etc/fstab /etc/fstab_bak
    sudo cat /etc/fstab_bak | grep -v swap > /etc/fstab

    # 永久关闭防火墙，确保网络通畅
    sudo systemctl stop firewalld
    sudo systemctl disable firewalld

    # 关闭 SELinux 防火墙
    sudo setenforce 0
    sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

    # 允许 iptables 检查桥接流量
    cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
    br_netfilter
    EOF
    cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
    net.bridge.bridge-nf-call-ip6tables = 1
    net.bridge.bridge-nf-call-iptables = 1
    EOF
    sudo sysctl --system


安装 kubeadm、kubelet 和 kubectl
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
    [kubernetes]
    name=Kubernetes
    baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
    enabled=1
    gpgcheck=1
    repo_gpgcheck=1
    gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
    exclude=kubelet kubeadm kubectl
    EOF

    sudo yum install -y --nogpgcheck kubelet kubeadm kubectl --disableexcludes=kubernetes
    sudo systemctl enable --now kubelet


使 Docker 与 K8s 的驱动保持一致
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
------------------------------

初始化集群控制平面
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    kubeadm init \
        --pod-network-cidr=10.244.0.0/16 \
        --image-repository registry.aliyuncs.com/google_containers \
        --apiserver-advertise-address <主机IP地址>


为当前用户生成 kubeconfig
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config

安装 CNI 插件
~~~~~~~~~~~~~~

.. code-block:: bash

    curl --insecure -sfL https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml | kubectl apply -f -

移除 master 节点上的污点
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    kubectl taint nodes --all node-role.kubernetes.io/master-

启用 kubectl 的自动补全功能
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    echo 'source <(kubectl completion bash)' >> ~/.bashrc
    echo 'source /usr/share/bash-completion/bash_completion' >> ~/.bashrc

重新生成 token
~~~~~~~~~~~~~~~

.. note::

    把下面这条命令的输出，在需要加入当前集群的节点上运行一次，即可完成集群的横向扩展。

.. code-block:: bash

    kubeadm token create --print-join-command


查看当前集群中节点的信息
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    kubectl cluster-info
    kubectl get nodes

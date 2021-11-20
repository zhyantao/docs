=====================
部署 Kubernetes 集群
=====================

.. warning:: 
    
    集群中每台机器的 Hostname 不要重复，否则 Kubernetes 从不同机器收集状态信息时会产生干扰，被认为是同一台机器。

    安装 Kubernetes 最小需要 2 核处理器、2 GB 内存，且为 x86 架构（暂不支持 ARM 架构）。对于物理机器来说，今时今日要找一台不满足以上条件的机器很困难，但对于云主机来说，尤其是囊中羞涩、只购买了云计算厂商中最低配置的同学，就要注意一下是否达到了最低要求，不清楚的话请在/proc/cpuinf、/proc/meminfo中确认一下。


删除 Docker 的旧版本
--------------------

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
------------------------------

.. code-block:: bash

    sudo yum install -y yum-utils

    sudo yum-config-manager \
                --add-repo \
                https://download.docker.com/linux/centos/docker-ce.repo


更新系统软件仓库
----------------

.. code-block:: bash

    sudo yum update


安装最新版的 Docker 引擎
------------------------

.. code-block:: bash

    sudo yum install docker-ce docker-ce-cli containerd.io


测试 Docker 是否安装成功
------------------------

.. code-block:: bash

    sudo docker run hello-world


给命令行添加 Docker 命令自动补全
--------------------------------

.. code-block:: bash

    echo 'source /usr/share/bash-completion/completions/docker' >> ~/.bashrc


让 Docker 能够开机启动
----------------------

.. code-block:: bash

    sudo systemctl enable docker
    sudo systemctl start docker


安装 Docker-Compose
--------------------

.. code-block:: bash

    sudo curl -L "https://get.daocloud.io/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose


允许 iptables 检查桥接流量
--------------------------

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
---------------------------------

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

    sudo setenforce 0
    sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

    sudo yum install -y --nogpgcheck kubelet kubeadm kubectl --disableexcludes=kubernetes

    sudo systemctl enable --now kubelet


初始化集群前的准备工作：关闭 Swap 分区
------------------------------------------

- 临时关闭Swap分区

.. code-block:: bash

    sudo swapoff -a
    echo "KUBELET_EXTRA_ARGS=--fail-swap-on=false" >> /etc/sysconfig/kubelet

- 永久关闭Swap分区

.. code-block:: bash

    yes | sudo cp /etc/fstab /etc/fstab_bak
    sudo cat /etc/fstab_bak | grep -v swap > /etc/fstab


修改 Docker 的驱动，使其与 K8s 的 cgroups 保持一致
--------------------------------------------------

.. code-block:: bash

    cat <<EOF | sudo tee /etc/docker/daemon.json
    {
        "exec-opts": ["native.cgroupdriver=systemd"]
    }
    EOF

    systemctl daemon-reload
    systemctl restart docker


使 kubelet 开机启动
-------------------

.. code-block:: bash

    systemctl start kubelet
    systemctl enable kubelet


后续操作仅 master 节点需要运行
------------------------------


预拉取镜像，首先检查需要的版本
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: bash

    kubelet --version
    kubeadm config images list --kubernetes-version v1.22.1


预拉取镜像，然后手工拉取第三方镜像（因为 Google 连不上）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo docker pull v5cn/kube-apiserver:v1.22.1
    sudo docker pull v5cn/kube-controller-manager:v1.22.1
    sudo docker pull v5cn/kube-scheduler:v1.22.1
    sudo docker pull v5cn/kube-proxy:v1.22.1
    sudo docker pull v5cn/pause:3.5
    sudo docker pull v5cn/etcd:3.5.0-0
    sudo docker pull v5cn/coredns:v1.8.4

    sudo docker tag v5cn/kube-apiserver:v1.22.1 k8s.gcr.io/kube-apiserver:v1.22.1
    sudo docker tag v5cn/kube-controller-manager:v1.22.1 k8s.gcr.io/kube-controller-manager:v1.22.1
    sudo docker tag v5cn/kube-scheduler:v1.22.1 k8s.gcr.io/kube-scheduler:v1.22.1
    sudo docker tag v5cn/kube-proxy:v1.22.1 k8s.gcr.io/kube-proxy:v1.22.1
    sudo docker tag v5cn/pause:3.5 k8s.gcr.io/pause:3.5
    sudo docker tag v5cn/etcd:3.5.0-0 k8s.gcr.io/etcd:3.5.0-0
    sudo docker tag v5cn/coredns:v1.8.4 k8s.gcr.io/coredns/coredns:v1.8.4

    sudo docker rmi v5cn/kube-apiserver:v1.22.1
    sudo docker rmi v5cn/kube-controller-manager:v1.22.1
    sudo docker rmi v5cn/kube-scheduler:v1.22.1
    sudo docker rmi v5cn/kube-proxy:v1.22.1
    sudo docker rmi v5cn/pause:3.5
    sudo docker rmi v5cn/etcd:3.5.0-0
    sudo docker rmi v5cn/coredns:v1.8.4


初始化集群控制平面
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    kubeadm init \
        --pod-network-cidr=10.244.0.0/16 \
        --kubernetes-version v1.22.1 \
        --apiserver-advertise-address <NET_INTERFACE_IP>

.. note:: 注意保持版本号的一致性，修改NET_INTERFACE_IP为本机的IP地址


切换至需要配置的用户后，为当前用户生成 kubeconfig
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

生成 token
~~~~~~~~~~~

.. note:: 
    
    确保网络通畅的——这听起来像是废话，但确实有相当一部分的云主机不对 SELinux、iptables、安全组、防火墙进行设置的话，内网各个节点之间、与外网之间会存在默认的访问障碍，导致部署失败。

    把下面这条命令的输出，在需要加入当前集群的节点上运行一次，即可完成集群的横向扩展。

.. code-block:: bash

    kubeadm token create --print-join-command


查看当前集群中节点的信息
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    kubectl cluster-info
    kubectl get nodes


参考文献
---------

1. `凤凰架构 <https://icyfenix.cn/>`_
2. `Installing kubeadm <https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/>`_
3. `Creating a cluster with kubeadm <https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/>`_

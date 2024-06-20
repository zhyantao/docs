=====================
部署 Kubernetes 集群
=====================

下载并安装 CentOS 7：http://isoredirect.centos.org/centos/7/isos/x86_64/

.. warning::

    以 3 个节点为例，创建集群：（一个 master 节点，两个 node 节点）

    - ``uname -m``：集群内每个节点必须为 x86 架构（\ :ref:`不支持 ARM 架构 <training-with-gpu>`\ ）。
    - ``lscpu``：最少 2 核处理器。
    - ``free -mh``：最小 2GB 内存。
    - ``vim /etc/hostname`` 修改 hostname，使集群内每个节点的 hostname 不同。
    - ``vim /etc/sysconfig/network-scripts/ifcfg-ens33``：修改为静态 IP 地址。
    - ``vim /etc/hosts``：配置主机名和 IP 地址映射，确保各节点 ``ping <hostname>`` 互通。
    - ``ip link``：集群内每个节点的网络接口的 MAC 地址不同。
    - ``sudo cat /sys/class/dmi/id/product_uuid``：集群内每个节点的 product_uuid 不同。
    - ``firewall-cmd --state``：确保防火墙关闭。
    - ``sestatus``：确保 SELinux 被禁止。
    - ``date``：确保集群内各节点的时间保持一致。
    
    确保网络通畅的——这听起来像是废话，但确实有相当一部分的云主机不对
    SELinux、iptables、安全组、防火墙进行设置的话，内网各个节点之间、与外网之间会存在默认的访问障碍，导致部署失败。


初始化集群前的准备工作
----------------------

.. code-block:: bash

    # 每台主机的名字不同
    hostnamectl set-hostname master # 在主机 1 上操作
    hostnamectl set-hostname node01 # 在主机 2 上操作
    hostnamectl set-hostname node02 # 在主机 3 上操作

    # 升级 Linux 内核到 5.4
    rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
    yum -y install https://www.elrepo.org/elrepo-release-7.0-4.el7.elrepo.noarch.rpm
    yum --enablerepo="elrepo-kernel" -y install kernel-lt.x86_64
    grub2-set-default 0
    grub2-mkconfig -o /boot/grub2/grub.cfg
    reboot
    uname -r

    # 同步时间
    sudo systemctl stop chronyd
    sudo systemctl disable chronyd
    sudo yum install ntp ntpdate
    sudo ntpdate ntp.aliyun.com
    sudo rm -rf /etc/localtime
    sudo ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

    # 永久关闭Swap分区
    yes | sudo cp /etc/fstab /etc/fstab_bak
    sudo cat /etc/fstab_bak | grep -v swap > /etc/fstab

    # 永久关闭防火墙，确保网络通畅
    sudo systemctl stop firewalld
    sudo systemctl disable firewalld
    firewall-cmd --state

    # 关闭 SELinux 防火墙
    sudo sed -i 's/^SELINUX=enforcing$/SELINUX=disabled/' /etc/selinux/config

    # 允许 iptables 检查桥接流量
    cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
    overlay
    br_netfilter
    EOF

    sudo modprobe overlay
    sudo modprobe br_netfilter

    # 配置端口转发和网桥过滤
    cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
    net.bridge.bridge-nf-call-iptables  = 1
    net.bridge.bridge-nf-call-ip6tables = 1
    net.ipv4.ip_forward                 = 1
    vm.swappiness                       = 0
    EOF

    # 应用 sysctl 参数而不重新启动
    sudo sysctl --system

    # 配置 IPVS
    yum -y install ipset ipvsadm
    
    cat > /etc/sysconfig/modules/ipvs.modules <<EOF
    #!/bin/bash
    modprobe -- ip_vs
    modprobe -- ip_vs_rr
    modprobe -- ip_vs_wrr
    modprobe -- ip_vs_sh
    modprobe -- nf_conntrack
    EOF

    chmod 755 /etc/sysconfig/modules/ipvs.modules
    bash /etc/sysconfig/modules/ipvs.modules


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


使用仓库安装 Docker
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo yum install -y yum-utils device-mapper-persistent-data lvm2

    sudo yum-config-manager \
        --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo


更新系统软件仓库
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo yum update


安装最新版的 Docker 引擎
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo yum makecache fast
    sudo yum install docker-ce docker-ce-cli containerd.io
    sudo service docker start


测试 Docker 是否安装成功
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo docker run hello-world


安装 cri-dockerd
~~~~~~~~~~~~~~~~~~

因为 K8s 1.24 及以上的版本移除了 dockershim，需要 cri-dockerd 才能初始化 K8s 集群。

.. code-block:: bash

    # 安装 Go
    wget https://go.dev/dl/go1.19.3.linux-amd64.tar.gz
    sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.19.3.linux-amd64.tar.gz
    echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/profile
    source /etc/profile

    # 安装 cri-dockerd
    git clone https://github.com/Mirantis/cri-dockerd.git
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


让 Docker 能够开机启动
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo systemctl enable docker
    sudo systemctl start docker


安装 Docker-Compose
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo curl -L "https://get.daocloud.io/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose


使用 kubeadm 创建生产集群
--------------------------

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


使 kubelet 与容器的运行时驱动保持一致
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # 修改 docker 的驱动
    cat <<EOF | sudo tee /etc/docker/daemon.json
    {
        "exec-opts": ["native.cgroupdriver=systemd"]
    }
    EOF

    systemctl daemon-reload
    systemctl restart docker

    # 修改 kubelet 的驱动
    echo 'KUBELET_EXTRA_ARGS="--cgroup-driver=systemd"' > /etc/sysconfig/kubelet
    
    systemctl enable --now kubelet


使 kubelet 开机启动
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    systemctl start kubelet
    systemctl enable kubelet


后续操作仅 master 节点需要运行
------------------------------

初始化集群控制平面
~~~~~~~~~~~~~~~~~~

首先使用 ``kubeadm config print init-defaults > kubeadm-config.yaml`` 创建配置文件，并进行如下修改

.. code-block:: yaml

    apiVersion: kubeadm.k8s.io/v1beta3
    bootstrapTokens:
    - groups:
    - system:bootstrappers:kubeadm:default-node-token
    token: abcdef.0123456789abcdef
    ttl: 24h0m0s
    usages:
    - signing
    - authentication
    kind: InitConfiguration
    localAPIEndpoint:
    advertiseAddress: 192.168.163.139
    bindPort: 6443
    nodeRegistration:
    criSocket: unix:///var/run/cri-dockerd.sock
    imagePullPolicy: IfNotPresent
    name: master
    taints: null
    ---
    apiServer:
    timeoutForControlPlane: 4m0s
    apiVersion: kubeadm.k8s.io/v1beta3
    certificatesDir: /etc/kubernetes/pki
    clusterName: master
    controllerManager: {}
    dns: {}
    etcd:
    local:
        dataDir: /var/lib/etcd
    imageRepository: registry.aliyuncs.com/google_containers
    kind: ClusterConfiguration
    kubernetesVersion: 1.25.4
    networking:
    dnsDomain: cluster.local
    serviceSubnet: 10.96.0.0/12
    scheduler: {}
    ---
    kind: KubeletConfiguration
    apiVersion: kubelet.config.k8s.io/v1beta1
    cgroupDriver: systemd


之后进行初始化集群：

.. code-block:: bash

    kubeadm init --config kubeadm-config.yaml

.. warning::
    
    如果出现下面的报错：

    .. code-block:: bash
        
        [ERROR CRI]: container runtime is not running

    请尝试 ``rm /etc/containerd/config.toml`` 和 ``systemctl restart containerd``，然后重新运行 ``kubeadm init`` 命令。


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

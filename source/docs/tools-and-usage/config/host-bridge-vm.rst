=====================
VM 和 HOST 之间的通信
=====================

基本的网络知识，如果两台设备要互相通信，有一个渠道就是通过交换机。

安装完 VMware 后，我们电脑上就会出现 **三台虚拟交换机** ：VMnet0、VMnet1、VMnet8。
如果想让双方通信，我们只需要选择其中的一种，最常用的还是 VMnet8（NAT 模式）。

在 Windows 上我们可以检查 VMnet8 的网关信息，默认应该是动态分配的。
但是大多时候，我们不希望我们的虚拟机 IP 地址随便改动，所以这里对宿主机一般也是静态分配。

确保宿主机和虚拟机的 **网关（GATEWAY）地址保持一致** ，随便给宿主机和虚拟机分配一个 **不重复的 IP 地址** 就可以了。
网关地址一般都是 ``192.168.?.1`` 这里的 ? 可以随便设，子网掩码都设置为 ``255.255.255.0`` 。
DNS 地址关系到 **能不能上网** 的问题，常用的 DNS 服务器有 ``114.114.114.114`` （中国电信）、 ``8.8.8.8`` （谷歌）。

然后说完了设置的值是什么，那么从哪里找到这些配置文件呢？

- Windows： ``控制面板`` > ``网络和 Internet`` > ``网络连接`` > ``VMnet8 属性`` > ``IPv4 属性``
- 虚拟机： 
  
  - VMware： ``Edit`` > ``Virtual Network Editor`` > ``选中 VMnet8`` > ``Change Settings`` > ``Subnet IP: 192.168.?.0`` > ``NAT Settings`` > ``GATEWAY IP: 192.168.?.1``
  - Linux： ``/etc/sysconfig/network-scripts/ifcfg-*`` > ``BOOTPROTO=static`` & ``ONBOOT=yes`` & ``IPADDR=192.168.?.xxx`` & ``GATEWAY=192.168.?.1``

注意：我设置完之后，在 Windows 中双击 VMnet8 查看状态的时候显示 “无网络访问权限”，但是实际上能上网，不知道为什么。

最后测试，宿主机和虚拟机互相 ``ping`` 一下，然后再都 ``ping www.baidu.com`` 。如果 ``ping`` 不通，检查一下防火墙。

.. admonition:: 防火墙设置
    :class: dropdown

    Windows

    .. code-block:: bash

        1. 控制面板
        2. 系统和安全
        3. Windows Defender 防火墙
        4. 允许应用或功能通过 Windows Defender 防火墙
        5. 文件和打印机共享（专用打上对勾）

    CentOS、Fedora
    
    .. code-block:: bash

        systemctl stop firewalld.service
        yum install openssh-server
        service sshd start

    Debian
    
    .. code-block:: bash

        iptables -F
        apt install openssh-server
        service sshd start

    Ubuntu

    .. code-block:: bash

        ufw disable
        apt install openssh-server
        service sshd start


--------

如果使用 VMware 的虚拟机克隆方法，两台主机需要通信，则需要修改克隆机的：

- ``IP Address`` `Ref <https://linuxconfig.org/how-to-configure-static-ip-address-on-ubuntu-18-10-cosmic-cuttlefish-linux>`__
- ``MAC Address`` 直接删除（重启后会自动生成），或参考 `Ref <https://www.howtogeek.com/192173/how-and-why-to-change-your-mac-address-on-windows-linux-and-mac/>`__ 手工分配硬件地址。
- ``UUID`` 直接删除（重启后会自动生成），或参考 `Ref <https://www.howtogeek.com/192173/how-and-why-to-change-your-mac-address-on-windows-linux-and-mac/>`__ 手工指定 ``UUID`` 。
- ``hostname``  （在网络中可以看见的主机名字） `Ref <https://phoenixnap.com/kb/ubuntu-20-04-change-hostname>`__
- 虚拟机的网卡信息 `Ref <https://phoenixnap.com/kb/ubuntu-20-04-change-hostname>`__
- 在需要相互访问的物理机和虚拟机的 ``/etc/hosts`` 中分别添加 IP 其他主机的地址映射，格式为 ``IPAddress hostname`` ，作用是 ``ping hostname`` 是能成功

--------

我们如果用 ``ipconfig`` 查看宿主机的网络信息，可能会出现很多看不懂的名词，这里来统一解释一下：

- **Realtek PCIe GbE Family Controller**\ ：网线/有线入网使用的协议。 `Ref <https://answers.microsoft.com/en-us/windows/forum/windows_7-networking/what-is-realtek-pcie-gbe-family-controller-why-it/5a6cdd17-155b-e011-8dfc-68b599b31bf5>`__
- **Hyper-V**\ ：微软原生的虚拟机管理程序，它允许你在一台物理机上创建多个虚拟机，多个虚拟机之间相互独立，但是资源共享。
- **Hyper-V Virtual Ethernet Adapter（Default Switch）**\ ：虚拟网络适配器，也叫 Virtual NIC 。可以看作是物理网络适配器的一个虚拟版本。它通过 LAN 连接一个物理服务器和多个 VM 或其他网络设备。简言之，它管理着所有的网络通信。每个 VM 都有一个或多个 vNIC ，它提供向子网的连接。你可以通过给 NIC 分配 IP 地址，让更多子网中的机器可以相互通信。 `Ref <https://www.nakivo.com/blog/hyper-v-network-adapters-what-why-and-how/>`__
- **Intel(R) Wi-Fi 6 AX200 160MHz**：\ WLAN/无线入网使用的协议
- **Microsoft Wi-Fi Direct Virtual Adapter**：主要用于创建无线热点。这项虚拟化技术把一个物理无线适配器转换为两个虚拟无线适配器。然后，你通过连接一个虚拟无线适配器到常规无线网络，并使用另一个虚拟适配器连接到另一个网络（例如 WiFi 热点），并让其他人像连接到普通 AP 一样无线连接到你的 Windows 机器。 `Ref <https://superuser.com/questions/1580417/what-is-microsoft-wi-fi-direct-virtual-adapter-used-for>`__
- **VMware Virtual Ethernet Adapter for VMnet1**\ ：这是 Host-Only 网络模式，用于建立一个与世隔绝的网络环境。其中 VMnet1 是一个虚拟的交换机，交换机的一个端口连接到你的 Host 上，另外一个端口连接到虚拟的 DHCP 服务器上（实际上是 VMware 的一个组件），剩下的端口连到虚拟机上。虚拟网卡 VMnet1 作为虚拟机的网关接口，为虚拟机提供服务。在虚拟机启动之后，如果你用 ipconfig 命令，你会看到默认网关指向了 VMnet1 网卡的地址。（实际上它并不能提供路由，这是 VMware 设计使然，它是干除了提供路由之外的一些事情——实际上是我也不知道它干了什么事情），这里没有提供路由主要表现在没有提供 NAT 服务，使得虚拟机不可以访问 Host-Only 模式所指定的网段之外的地址。 `Ref <https://blog.csdn.net/u012110719/article/details/42318717>`__
- **VMware Virtual Ethernet Adapter for VMnet8**\ ：这是 NAT 方式，是最简单的组网方式。VMnet8 是一张虚拟网卡。物理机使用 VMnet8 和虚拟机通信时，网卡和虚拟机的网关需要保持一致。虚拟网卡一个接口连接到虚拟的 NAT 服务器上（这也是一个VMware组件），一个接口连接到虚拟 DHCP 服务器，其他的接口连虚拟机。NAT 组网方式比 Host-Only 方式多了一个 NAT 服务。 `Ref <http://www.unixlinux.online/unixlinux/linuxgl/linuxjq/201703/77641.html>`__
- **VMware Virtual Ethernet Adapter for VMnet0**\ ：实际上就是一个虚拟的网桥。这个网桥有很若干个端口，一个端口用于连接你的Host，一个端口用于连接你的虚拟机，他们的位置是对等的，谁也不是谁的网关。 `Ref <https://wxler.github.io/2021/02/02/221724>`__
- **Bluetooth Device (Personal Area Network)**\ ：蓝牙网络连接


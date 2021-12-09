==========================
可以 ping 通，ssh 无法连接
==========================

CentOS、Fedora
---------------
 
.. code-block:: bash

    systemctl stop firewalld.service
    yum install openssh-server
    service sshd start

Debian
-------
 
.. code-block:: bash

    iptables -F
    apt install openssh-server
    service sshd start

Ubuntu
--------

.. code-block:: bash

    ufw disable
    apt install openssh-server
    service sshd start

======
Linux
======

.. tip:: 

    当我们对一个命令印象模糊的时候，首先应该想到的不应该是谷歌百度，而应该是 MAN 手册。
    
    关于如何读懂 MAN 手册，我想大概能明白下面几条就足够了：

    - 由中括号括起来的部分 ``[OPTION1 | OPTION2 | ...]`` 为可选项。 

      - 中括号内部多个选项之间由 ``|`` 分割，表示从多个 OPTIONS 中选择一个。

    - 由大括号括起来的部分 ``{OPTION1 | OPTION2 | ...}`` 为必选项。

      - 大括号内部多个选项之间由 ``|`` 分割，表示从多个 OPTIONS 中选择一个。

    - 既没有中括号，也没有大括号括起来的部分 ``FILE`` 也是必选项。


Linux 目录结构
---------------

.. code-block:: bash

    bin         # Linux 操作系统下可执行的系统级的二进制命令（binary 的缩写）

    boot        # 系统开机时需要加载的一些文件和配置

    dev         # 设备文件所在目录（device 的缩写）

    etc         # 包含了当前操作系统用户所有配置的相关信息

    home        # 当前操作系统所安装的用户的主目录

    lib         # 操作系统使用的库文件以及相关的配置

    media       # 系统自动挂载目录

    mnt         # 手动挂载目录

    opt         # 给第三方协力软体方放置的目录

    root        # root 用户的宿主目录

    sbin        # 超级用户需要用到的一些二进制命令存储在该目录（super binary 的缩写）

    usr         # Unix 软件资源包管理目录，存放的是当前用户下的一些东西

    srv         # 一些网络启动后，这些服务所需要取用的资料目录

    lost+found  # 存放系统错误产生的文件碎片，方便用户查找和恢复

    proc        # 内核提供的一个接口，主要用来存储系统统计信息

    sys         # 与 proc 相似，记录与核心相关的资讯

    run         # 存放系统运行时需要的一些文件


文件和目录操作
--------------

.. code-block:: bash

    ls          # 查看执行目录下所有文件和目录信息
        -a      # 列出当前目录下所有文件内容
        -R      # 同时列出所有子目录层
        -l      # 除了文件名外，还将文件的权限、所有者、文件大小等信息详细列出来

    tree        # 以树状形式显示当前文件和目录
    
    cd          # 进入指定目录
        -       # 返回到最近访问的目录

    pwd         # 查看当前所在目录的缩写

    touch       # 新建文件

    mkdir       # 新建目录
        -p      # 创建多级目录
    
    rm          # 删除文件
        -r      # 删除目录
        -i      # 提示用户是否删除目录或文件
        -f      # 强制删除（默认）

    cp          # 复制文件（有同名文件会覆盖）
        -r      # 复制目录（目录不存在会新建）

    scp         # 不同机器之间复制文件
        user@remotehost:directory/SourceFile LocalTargetFile
        -r user@remotehost:directory/SourceFolder LocalTargetFolder
        LocalTargetFile user@remotehost:directory/SourceFile
        -r LocalTargetFolder user@remotehost:directory/SourceFolder
    
    cat         # 查看文件内容
        <<EOF | tee save/to/tagetFile
        Will override original contents...
        EOF
    
    more        # 将文件内容分页输出到屏幕，不可以上下滑动
        Enter   # 显示下一行
        Space   # 显示下一页
        q       # 退出

    less        # 将文件内容分页输出到屏幕，可以上下滑动
        Enter   # 显示下一行
        Space   # 显示下一页
        q       # 退出
        ↑       # 滚动到上一行
        ↓       # 滚动到下一行

    head        # 查看文件前 10 行的内容（默认）
        -5      # 查看文件前 5 行内容

    tail        # 查看文件后 10 行的内容（默认）
        -5      # 查看文件后 5 行内容

    wc          # 显示文件的行数、字数、字节数
        -l      # 只显示行数
        -w      # 只显示字数
        -c      # 只显示字节数

    stat        # 查看文件或文件系统信息
    od          # 查看二进制文件信息
    file        # 查看文件类型
    lsattr      # 显示文件扩展属性

    ln                                  # 新建快捷方式，默认为硬链接，不允许对目录创建硬链接
        SourceFile TargetFile           # SourceFile 和 TargetFile 的内容将保持一致
        -s SourceFile TargetFile        # 占用空间小，复制快捷方式将复制源文件）
        -s SourceFolder TargetFolder    # 对目录创建软连接）


查找
-----

.. code-block:: bash

    find expr1                      # 查找文件或目录，从磁盘遍历
        -name 'PATTERN'             # 根据正则表达式搜索文件或目录
        -and expr2                  # 仅当字符串同时满足 expr1 和 expr2 的 PATTERN 时有结果输出
        -or expr2                   # 将满足 expr1 或 expr2 的 PATTERN 都输出到屏幕
        ! expr2                     # 根据 expr2 的 PATTERN 筛除查找结果
        -type [d|f]                 # 指定搜索的文件类型为目录或文件
        -exec                       # 对找到的文件执行相应的命令
            rm -i {} \;             # 删除找到的文件
            grep 'PATTERN' {} \;    # 找到文件中有PATTERN对应文本所在的行
        -empty                      # 找空文件夹
        -perm 664                   # 查找具有664权限的文件
        -size [+|-][k|M]            # 按文件大小查找，[+|-]为大于，小于，默认等于，[k|M]为单位

    grep                            # 查找文件内容
        [OPTIONS] PATTERN [FILE...]
        [OPTIONS] [-e PATTERN | -f FILE] [FILE...]
        FILE...                     # 需要查找的文件
        -e PATTERN                  # 可以多次使用 -e 可以指定多个 PATTREN
        -f FILE                     # 此文件中的每一行都是 PATTERN
        -i                          # 忽略大小写

    which                           # 查找二进制命令，按 PATH 查找

    whereis                         # 查找二进制命令及其源代码、帮助文件，按 PATH 查找


进程管理
---------

.. code-block:: bash

    ps          # 查看整个系统内部正在运行的进程
        -a      # 当前系统所有用户的进程
        -u      # 查看进程所有者的一些其他信息
        -x      # 查看不能与用户交互的进程
        -e      # 显示所有进程
        -f      # 显示 UID，PPID，C，STIME 等栏位

    kill        # 杀死进程

    env         # 查看当前进程环境变量

    top         # 相当于 Windows 下的环境变量


网络管理
---------

.. code-block:: bash

    ip addr         # 获取网络接口配置信息（ifconfig）
    
    ping            # 测试与目标主机的连通性
        -C          # 发送指定包数目后停止
        -i          # 设定间隔秒数，每个几秒发送一个包，默认 1 秒
    
    nslookup        # 查看服务器域名对应的 IP 地址

    vi /etc/sysconfig/network-scripts/ifcfg-<网口名>    # 设置网卡信息
        BOOTPROTO="static"                              # 路由方式
        IPADDR="192.168.3.31"                           # 设置 IP 地址（须和网关位于同一网段）
        PREFIX="24"                                     # 网络前缀
        NETMASK="255.255.255.0"                         # 子网掩码
        GATEWAY="192.168.3.1"                           # 网关地址（统一路由下保持一致可上网）
        DNS1="114.114.114.114"                          # 中国电信 DNS 服务器（static 方式下不设置无法上网）
        DNS2="8.8.8.8"                                  # 谷歌 DNS 服务器
    
    netstat             # 查看网络连接，路由表，接口统计信息，虚拟连接，组播成员
        -t              # 仅显示 TCP 相关选项
        -u              # 仅显示 UDP 相关选项
        -n              # 拒绝显示别名，能显示数字的全部转化为数字
        -l              # 仅列出在 Listen(监听) 状态的服务
        -p              # 显示建立相关链接的程序名
    
    lsof -i:<端口号>    # 查看端口占用情况（netstat也可以，利用管道和 grep 就可以了）

    systemctl restart network   # 重启网络服务


用户和权限管理
--------------

.. code-block:: bash

    groupadd            # 创建用户组

    useradd             # 创建用户
        -g              # 指定用户组

    passwd              # 添加用户密码

    vi /etc/sudoers     # 提升用户权限

    su                  # 切换用户

    exit                # 退出登录用户

    userdel             # 删除用户
        -r              # 顺便把用户的主目录一起删除
 
    whoami              # 查看当前登录用户，相当于 id -un
        who             # 查看当前登录用户信息
        w               # 查看活动用户
    
    chmod               # 修改文件访问权限
        [u|g|o|a]       # 修改用户/同组用户/其他用户/所有用户的权限
        [+|-|=]         # 添加/取消/赋予给定权限并取消其他权限
        [r|w|x]         # 只读/可写/权限（r=4, w=2, x=1）

    chown               # （将文件拷贝到另一用户目录下，需要修改）文件的拥有者和所属组
        name_of_new_owner file_name
        newuser:newgroup file_name
        -R              # 处理指定目录以及其子目录下的所有文件

    chgrp               # 改变文件或目录的所属群组
        [OPTIONS] new_group files


压缩包管理
-----------

.. code-block:: bash

    tar                     # 解压或压缩命令
       [OPTION...] [FILE]...
       -C                   # 指定解压或压缩路径 
       -c                   # 创建压缩包，默认创建 .tar 包（创建压缩包时一定要带的参数）
       -x                   # 解压文件，默认解压 .tar 包（解压压缩包时一定要带的参数）
       -v                   # 显示处理的中间过程
       -j                   # 处理 .tar.bz2 或 .tar.bz 类型的文件
       -z                   # 处理 .tar.gz 或 .tgz 类型的文件
       -f                   # 选择文件
       --overwrite          # 解压时覆盖重名文件
       --skip-old-files     # 解压时不覆盖重名文件
    
    upzip                   # 解压 .zip 类型的文件
    zip                     # 压缩 .zip 类型的文件

    gunzip                  # 解压 .gz 类型的文件
    gzip                    # 压缩 .gz 类型的文件

    bunzip                  # 解压 .bz 或 .bz2 类型的文件
    bzip                    # 压缩 .bz 或 .bz2 类型的文件

    rar                     # 处理 .rar 类型的文件
        -x                  # 解压文件
        -a                  # 压缩文件


安装包管理
-----------

.. code-block:: bash

    yum             # 在线安装、更新、卸载、搜索安装包的工具
        [options] command [package ...]
        install     # 安装
        update      # 更新
        remove      # 卸载
        search      # 搜索
        list        # 列出可以获取到的安装包
        clean       # 清除缓存

    rpm             # 离线安装、更新、卸载、搜索安装包的工具
        rpm {-q|--query} [select-options] [query-options]       # 搜索安装包
        rpm {-V|--verify} [select-options] [verify-options]     # 确认安装包
        rpm {-i|--install} [install-options] PACKAGE_FILE ...   # 安装
        rpm {--reinstall} [install-options] PACKAGE_FILE ...    # 重新安装
        rpm {-U|--upgrade} [install-options] PACKAGE_FILE ...   # 更新
        rpm {-F|--freshen} [install-options] PACKAGE_FILE ...   # 只更新已安装的早期版本
        rpm {-e|--erase} [--allmatches] [--justdb] [--nodeps] \ # 卸载
           [--noscripts] [--notriggers] [--test] PACKAGE_NAME ...


系统管理
---------

.. code-block:: bash

    hostname        # 显示主机名称（网络可见）

    uname -a        # 显示系统信息
    cat /proc/version
    cat /etc/redhat-release

    lscpu           # 显示 CPU 简略信息（通常使用）
    /proc/cpuinfo   # 显示 CPU 详细信息

    du              # 查看某个目录的大小（disk used 的缩写）

    df              # 查看磁盘的使用情况（disk free 的缩写）

    which           # 查看指定命令所在的路径

    fdisk -l        # 查看所有分区 
    swapon -s       # 查看所有交换分区


Bash 快捷键
------------

.. code-block:: bash

    Ctrl + s        # 冻结窗口，用 Ctrl + q，Ctrl + C 退出

    Ctrl + l        # 清屏

    Ctrl + c        # 终止程序运行

    echo            # 输出到屏幕
        $PATH       # 环境环境变量
        $?          # 上次命令是否运行成功，成功为0，其他失败
    
    feee            # 查看内存和交换分区的使用情况
        [-m|-g|-k]  # 显示的单位可以是M、G、K
    
    shutdown        # 关机
    reboot          # 重启
    halt            # 关机后关闭电源


VIM 快捷键
-----------

.. code-block:: bash

    Ctrl + S    # 冻结窗口
    Ctrl + q    # 解冻窗口

    h j k l     # 左 下 右 上

    gg          # 光标移动到文件开头
    G           # 光标移动到文件末尾
    0           # 光标移动到行首
    $           # 光标移动到行尾
    23G         # 光标跳转到第23行

    x           # 删除光标后一个字符
    X           # 删除光标前一个字符
    dw          # 删除光标开始位置的单词
    d0          # 删除光标前本行文本的所有内容，不包含光标所在的字符
    D           # 删除光标后本行所有的内容，包含光标所在的字符
    dd          # 删除光标所在的行
    n dd        # 删除光标后面所有的行，包含光标所在的行

    u           # 一步撤销，可多次使用
    Ctrl + r    # 反撤销

    yy          # 复制当前行
    10yy        # 复制 10 行

    p           # 在光标所在位置向下开辟一行，粘贴
    P           # 在光标所在位置向上开辟一行，粘贴

    /PATTERN    # 从光标所在位置向下查找
    ?PATTERN    # 从光标所在位置向上查找
        Enter   # 输入完毕
        n       # 向下查找下一个
        N       # 向上查找下一个

    >>          # 文本右移一个 Tab 大小
    <<          # 文本左移一个 Tab 大小

    i           # 在光标前插入一个字符
    I           # 在行首插入一个字符
    a           # 在光标后插入一个字符
    A           # 在行尾插入一个字符
    o           # 向下新开辟一行，插入行首
    O           # 向上新开辟一行，插入行首
    s           # 删除光标所在的字符，并进入插入状态
    S           # 删除光标所在的行，并进入插入状态

    :23         # 跳转到第 23 行

    r                           # 替换当前字符
    :s/PATTERN/toString         # 将当前行第一次出现的 PATTERN 替换为 toString
    :s/PATTERN/toString/g       # 将当前行出现的 PATTERN 全部替换为 toString
    :%s/PATTERN/toString        # 将所有行第一次出现的 PATTERN 替换为 toString
    :%s/PATTERN/toString/g      # 将当前行出现的 PATTERN 全部替换为 toString
    :2,3s/PATTERN/toString      # 将[2,3]行第一次出现的 PATTERN 替换为 toString
    :2,3s/PATTERN/toString/g    # 将[2,3]行第一次出现的 PATTERN 替换为 toString

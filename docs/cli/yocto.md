# Yocto

```{note}
学习 Yocto 请参考 <https://gitee.com/zhyantao/pdf/raw/master/yocto/yocto-slides.pdf>。
```

## bitbake 常用命令

| 命令                                                              | 作用                                            |
| ----------------------------------------------------------------- | ----------------------------------------------- |
| `source oe-init-build-env`                                        | 将  `bitbake`  添加到环境变量中                 |
| `cd $BUILD_DIR && rm -Rf tmp sstate-cache`                        | 清除所有 `recipe` 的构建缓存                    |
| `bitbake <recipe>`                                                | 构建指定 `recipe`                               |
| `bitbake -c clean <recipe>` <br>`bitbake -c cleansstate <recipe>` | 清理指定 `recipe` 的构建产物                    |
| `bitbake -e <recipe> \| grep ^S=`                                 | 定位 `recipe` 源代码所在目录                    |
| `bitbake -e <recipe> \| grep ^WORKDIR=`                           | 查看  `${WORKDIR}` 变量的值                     |
| `bitbake-layers show-recipes "gdb*"`                              | 搜索指定的  `recipe`                            |
| `bitbake -c devshell <recipe>`                                    | 进入命令行交互界面进行编译                      |
| `bitbake -c devpyshell <recipe>`                                  | 进入 Python 交互界面进行编译                    |
| `bitbake -c listtasks <recipe>`                                   | 列出构建   `recipe`   所需执行的任务            |
| `bitbake -f <recipe>`                                             | 强制重新构建                                    |
| `bitbake -v <recipe>`                                             | 详细输出构建过程                                |
| `bitbake -DDD <recipe>`                                           | 显示详细的 Debug 信息                           |
| `yocto-layer create <layer_name>`                                 | 新建一个 `layer`                                |
| `bitbake-layers add-layer /path/to/your_meta-layer`               | 新建一个自定义的 `layer`                        |
| `bitbake-layers remove-layer /path/to/your_meta-layer`            | 删除自定义的 `layer`                            |
| `bitbake-layers show-recipes`                                     | 列出所有的   `recipe`                           |
| `bitbake-layers show-overlayed`                                   | 列出所有冲突的   `recipe`                       |
| `bitbake-layers show-appends`                                     | 列出所有的  `.bbappend`  文件                   |
| `bitbake-layers flatten <output_dir>`                             | 将所有的  `.bb`  文件抽离出来放到  `output_dir` |
| `bitbake-layers show-cross-depends`                               | 列出所有 `layer` 的交叉依赖关系                 |
| `bitbake-layers layerindex-show-depends <layer_name>`             | 根据 OE index 列出指定 `layer` 的依赖           |
| `bitbake-layers layerindex-fetch <layer name>`                    | 使用 OE index 拉取和添加 `layer`                |

## BitBake 文件简介

运行 `bitbake <recipe>` 时，会自动匹配 `<recipe>.bb`，默认情况下 [Task](https://docs.yoctoproject.org/ref-manual/tasks.html) 按照如下工作流进行：

```{note}
The [TOPDIR](https://docs.yoctoproject.org/ref-manual/variables.html#term-TOPDIR) variable points to the [Build Directory](https://docs.yoctoproject.org/ref-manual/terms.html#term-Build-Directory).
```

```{uml}
@startuml
start
:read <color:blue>${TOPDIR}</color>/conf/bblayers.conf;
:read <color:blue>${TOPDIR}</color>/conf/local.conf;
:read [[https://layers.openembedded.org/layerindex/branch/master/layers layer]]/meta/conf/layer.conf;
:read [[https://layers.openembedded.org/layerindex/branch/master/layers layer]]/meta/conf/bitbake.conf;
:<color:green>select a target recipe</color>;
:generate cache directory;
:execute <color:red>do_fetch</color>, download from [[https://docs.yoctoproject.org/bitbake/bitbake-user-manual/bitbake-user-manual-ref-variables.html#term-SRC_URI SRC_URI]], save to [[https://github.com/openembedded/openembedded-core/blob/yocto-5.1.1/meta/conf/bitbake.conf#L842 DL_DIR]];
:execute <color:red>do_unpack</color>, unpack the source code to [[https://github.com/openembedded/openembedded-core/blob/yocto-5.1.1/meta/conf/bitbake.conf#L404 ${WORKDIR}]];
:execute <color:red>do_patch</color>;
:execute <color:red>do_configure</color>;
:execute <color:red>do_compile</color>, firstly cd to [[https://github.com/openembedded/openembedded-core/blob/yocto-5.1.1/meta/conf/bitbake.conf#L409 ${B}]], then run [[https://github.com/openembedded/openembedded-core/blob/yocto-5.1.1/meta/classes-global/base.bbclass#L41 oe_runmake]];
:execute <color:red>do_install</color>, install the compiled files to [[https://github.com/openembedded/openembedded-core/blob/yocto-5.1.1/meta/conf/bitbake.conf#L407 ${D}]];
:execute <color:red>do_package</color>, package data to [[https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-PKGDATA_DIR PKGDATA_DIR]];
:execute <color:red>do_rootfs</color>, see [[https://docs.yoctoproject.org/dev/ref-manual/tasks.html#do-rootfs docs.yoctoproject.org]];
stop
@enduml
```

例：假设你有三个脚本需要加入发行版：`startup-script`、`run-script` 和 `support-script`，以下是如何通过 `.bb` 文件实现这一过程的简要指南 [^ref-cite-1]。

```bash
DESCRIPTON = "Startup scripts"
LICENSE = "MIT"

# 菜谱的版本：更新菜谱后，不要忘记修改这里的版本号
PR = "r0"

# 运行时依赖
#
# 添加类似于以下内容的行，以确保运行脚本所需的所有包都安装在映像中
#
# RDEPENDS_${PN} = "parted"

# SRC_URI 指定制作菜谱所需的源文件（或脚本文件）
#
# src_uri 常用的有效格式有 files、https、git 等
# 本例假设所有的源文件都存储在 files 目录下
#
SRC_URI = "              \
   file://startup-script \
   file://run-script     \
   file://support-script \
   "

# do_compile 的功能如下：
#  1) 切换到 build 目录
#  2) 运行 oe_runmake 编译源代码
#
do_compile() {
    #
    # 查找 Makefile、makefile 或 GNUmakefile
    # 若不存在上述文件，则什么都不做
    #
    make
}

# do_install 的功能如下：
#  1) 确保映像中存在所需的目录；
#  2) 将脚本安装到映像中；
#  3) 为脚本创建符合其运行级别的软连接。
#
do_install() {
    #
    # 创建目录：
    #   ${D}${sysconfdir}/init.d - 用于保存脚本
    #   ${D}${sysconfdir}/rcS.d  - 用于保存系统启动时运行的脚本的软链接
    #   ${D}${sysconfdir}/rc5.d  - 用于保存 runlevel=5 的脚本的软链接
    #   ${D}${sbindir}           - 用于保存被上面两个脚本调用的脚本
    #
    # ${D} 实际上是目标系统的根目录
    # ${D}${sysconfdir} 是存储系统配置文件的位置（例如 /etc）
    # ${D}${sbindir} 是存储可执行文件的位置（例如 /sbin）
    #
    install -d ${D}${sysconfdir}/init.d
    install -d ${D}${sysconfdir}/rcS.d
    install -d ${D}${sysconfdir}/rc1.d
    install -d ${D}${sysconfdir}/rc2.d
    install -d ${D}${sysconfdir}/rc3.d
    install -d ${D}${sysconfdir}/rc4.d
    install -d ${D}${sysconfdir}/rc5.d
    install -d ${D}${sbindir}

    #
    # 将脚本安装到 Linux 发行版中
    #
    # 通过 SRC_URI 获取的文件会存在于 ${WORKDIR} 目录下
    # ${WORKDIR}=file://
    #
    install -m 0755 ${WORKDIR}/startup-script  ${D}${sysconfdir}/init.d/
    install -m 0755 ${WORKDIR}/run-script      ${D}${sysconfdir}/init.d/
    install -m 0755 ${WORKDIR}/support-script  ${D}${sbindir}/

    #
    # 软链接同样可以被安装到 Linux 发行版中，比如：
    #
    # ln -s support-script-link ${D}${sbindir}/support-script

    #
    # 在 runlevel 目录下创建指向脚本的软链接
    # 以 S... 和 K... 开头的文件分别表示在 entering 和 exiting 相应 runlevel 时会被调用的脚本
    # 比如：
    #   rc5.d/S90run-script 会在进入 runlevel 5 时调用 (with %1='start')
    #   rc5.d/K90run-script 会在退出 runlevel 5 时调用 (with %1='stop')
    #
    ln -sf ../init.d/startup-script  ${D}${sysconfdir}/rcS.d/S90startup-script
    ln -sf ../init.d/run-script      ${D}${sysconfdir}/rc1.d/K90run-script
    ln -sf ../init.d/run-script      ${D}${sysconfdir}/rc2.d/K90run-script
    ln -sf ../init.d/run-script      ${D}${sysconfdir}/rc3.d/K90run-script
    ln -sf ../init.d/run-script      ${D}${sysconfdir}/rc4.d/K90run-script
    ln -sf ../init.d/run-script      ${D}${sysconfdir}/rc5.d/S90run-script
}
```

## 添加新的 `layer`/`recipe`

The Yocto Project 维护了一个官方的在线资源库，可用于浏览和检索可直接集成至 Linux 发行版中的层 (`layer`) 和配方 (`recipe`)。相关信息可通过以下链接获取：

- `layer` 索引：<https://layers.openembedded.org/layerindex/branch/master/layers/>
- `recipe` 索引：<https://layers.openembedded.org/layerindex/branch/master/recipes/>

这些资源提供了详细的列表和信息，帮助开发者选择合适的组件来丰富其基于 Yocto 的构建系统。

以上所有的源代码都可以在 Github 仓库找到：<https://github.com/openembedded/meta-openembedded>

## 离线构建 `meta-clang`

```bash
# 添加底包合 meta-clang 层
git clone git://github.com/openembedded/openembedded-core.git
cd openembedded-core
git clone git://github.com/openembedded/bitbake.git
git clone git://github.com/kraj/meta-clang.git

# 激活 bitbake 环境变量
source ./oe-init-build-env

# Add meta-clang overlay
bitbake-layers add-layer ../meta-clang

# 允许 bitbake 检查本地缓存
export BB_NO_NETWORK=1

# 将提前下载好的 git2_github.com.llvm.llvm-project.tar.gz 放到 DL_DIR 目录下
cp git2_github.com.llvm.llvm-project.tar.gz <build-dir>/downloads
```

````{note}
因为离线包 `*.llvm-project.tar.gz` 是以 `git2_` 开头的，需要手动创建 `.done` 文件：

```bash
cd <build-dir>/downloads
touch git2_github.com.llvm.llvm-project.tar.gz.done
```

如果离线包 `*.tar.gz` 不以 `git2_` 开头，不需要创建 `.done` 文件，但需要先注释掉以下几个变量：

- `LICENSE`
- `LIC_FILES_CHKSUM`
- `SRC_URI[md5sum]`
- `SRC_URI[sha256sum]`

然后使用 `bitbake recipe_name`，根据错误提示按步骤操作就可以了。你可能会遇到下面的问题：

- 错误提示先解开 `LICENSE` 的注释，照做即可。
- 重新运行 `bitbake` 生成 `SRC_URI[sha256sum]`，赋值给对应变量，并解开注释
- 重新运行 `bitbake` 错误提示解开 `LIC_FILES_CHKSUM` 的注释，照做即可
- 重新运行 `bitbake` 生成 `LIC_FILES_CHKSUM` 的 `md5`，赋值给对应变量，并解开注释
````

## Q & A

**ERROR: No space left on device or exceeds fs.inotify.max_user_watches?**

- <https://unix.stackexchange.com/questions/13751/kernel-inotify-watch-limit-reached>
- <https://ruanyifeng.com/blog/2011/12/inode.html>

[^ref-cite-1]: [Cookbook:Appliance:Startup Scripts - Yocto Project](https://wiki.yoctoproject.org/wiki/Cookbook:Appliance:Startup_Scripts)

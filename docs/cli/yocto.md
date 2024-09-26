# Yocto

**Yocto 用于构建**针对嵌入式设备**定制 Linux 发行版的**一套综合的**工具套件、模板和资源**。

探索 Yocto Project，建议从以下几个核心领域开始：

1. **Poky 工作流程**：作为 Yocto 的基础参考发行版，Poky 提供了定制发行版的实践范例。
2. **OpenEmbedded 构建系统**：利用 BitBake 构建引擎来驱动整个构建过程。
3. **定制操作系统组件**：学习如何根据需求选择和调整软件包。
4. **板级支持包(BSP)**：为特定硬件平台提供必要的驱动和配置。
5. **应用开发工具**：了解如何使用 Extensible SDK 或 Legacy SDK 进行应用开发。

本文聚焦于 BitBake 基础语法和操作命令，更深入的请学习 [yocto-slides.pdf](https://bootlin.com/doc/training/yocto/yocto-slides.pdf)。

## BitBake 文件简介

Bitbake 的构建流程可以分为四个步骤：

1. **解析层配置**：读取 `build` 目录下的 `conf/bblayers.conf` 以确定使用的层。
2. **配置解析**：遍历各层中的 `layer.conf` 和 `bitbake.conf`。
3. **依赖解析**：建立依赖图，并生成缓存信息（生成 `cache` 目录）。
4. **任务执行**：依据 `.bb` 和 `.bbappend` 文件执行构建任务。

其中，第四步是工作中最常遇到的，因此展开来讲：

当我们运行 `bitbake <recipe>` 时，它会自动地去找 `<recipe>.bb` 这个文件，`.bb` 文件包含了一系列的任务（[Tasks](https://docs.yoctoproject.org/ref-manual/tasks.html)）：`do_fetch`、`do_patch`、`do_compile`、`do_install` 及 `do_package` 等等。

Bitbake 的执行流程：

1. `do_fetch`：此阶段默认负责从网络源（根据 [`SRC_URI`](https://docs.yoctoproject.org/bitbake/bitbake-user-manual/bitbake-user-manual-ref-variables.html#term-SRC_URI) 变量指定）下载源代码，并将其保存至默认的下载目录 `${DL_DIR}`，该目录通常位于 `${TOPDIR}/downloads`，但实际位置可由用户在 `build/conf/local.conf` 文件中配置。下载完成后，还会验证源码完整性，生成一个 `.done` 文件。
2. `源代码解压与准备`：下载后的源代码会被解压缩并准备到一个工作目录下，通常是 `${WORKDIR}`，路径类似 `build/tmp/work/<archname>/<recipe>-<version>/`，其中 `<archname>` 是目标体系结构，`<recipe>-<version>` 对应于具体的配方及其版本。这个步骤确保了源代码在一个干净、独立的环境中准备就绪，以便后续构建过程使用。
3. `do_compile`：接着，Bitbake 调用 `do_compile` 任务来编译源代码。此阶段通常在 `${B}`（即编译目录）下设置当前工作目录，并默认尝试运行 `oe_runmake` 函数来执行 Makefile 中定义的编译指令。这一步骤利用了由 `oe-init-build-env` 脚本初始化的环境，支持交叉编译，确保生成的目标代码适用于目标架构。
4. `do_install`：编译完成后，`do_install` 任务将指定的编译输出（如库文件、可执行文件等）安装到一个临时的安装目录 `${D}`。这个目录作为打包前的暂存区，用于收集所有将被包含进最终包或根文件系统（`ROOTFS`）的文件。此过程在 `${B}` 目录下执行，并通常在 `fakeroot` 环境下操作，以模拟包的安装者权限。
5. `do_package`：最后，`do_package` 任务负责将 `${D}` 目录下的文件打包成合适的软件包格式（如 `.ipk`, `.deb`, `.rpm` 等），具体格式由配方和构建配置确定。这一阶段涉及文件归档、元数据生成以及可能的包管理数据库更新，为软件分发和部署做准备。

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

注意：`.bb` 文件中好多全局变量都是在 [`poky/meta/conf/bitbake.conf`](https://git.openembedded.org/bitbake/tree/conf/bitbake.conf) 中声明的，关于这些全局变量的解释可以参考 [Variables Glossary](https://docs.yoctoproject.org/bitbake/2.6/bitbake-user-manual/bitbake-user-manual-ref-variables.html)，比如 [`SRC_URI`](https://docs.yoctoproject.org/bitbake/2.6/bitbake-user-manual/bitbake-user-manual-ref-variables.html#term-SRC_URI)。重点理解 [`Build Directory`](https://docs.yoctoproject.org/ref-manual/terms.html#term-Build-Directory) 它和 `${TOPDIR}` 以及 `${TMPDIR}` 都有关系。

## BitBake 常用命令

| 命令                                                                 | 作用                               |
| ------------------------------------------------------------------ | -------------------------------- |
| `source oe-init-build-env`                                         | 将 `bitbake` 添加到环境变量中             |
| `cd $BUILD_DIR && rm -Rf tmp sstate-cache`                         | 清除所有 `recipe` 的构建缓存              |
| `bitbake <recipe>`                                                 | 构建指定 `recipe`                    |
| `bitbake -c clean <recipe>`  <br>`bitbake -c cleansstate <recipe>` | 清理指定 `recipe` 的构建产物              |
| `bitbake -e <recipe> \| grep ^S=`                                  | 定位 `recipe` 源代码所在目录              |
| `bitbake -e <recipe> \| grep ^WORKDIR=`                            | 查看 `${WORKDIR}` 变量的值             |
| `bitbake-layers show-recipes "gdb*"`                               | 搜索指定的 `recipe`                   |
| `bitbake -c devshell <recipe>`                                     | 进入命令行交互界面进行编译                    |
| `bitbake -c devpyshell <recipe>`                                   | 进入 Python 交互界面进行编译               |
| `bitbake -c listtasks <recipe>`                                    | 列出构建  `recipe`  所需执行的任务          |
| `bitbake -f <recipe>`                                              | 强制重新构建                           |
| `bitbake -v <recipe>`                                              | 详细输出构建过程                         |
| `bitbake -DDD <recipe>`                                            | 显示详细的 Debug 信息                   |
| `yocto-layer create <layer_name>`                                  | 新建一个 `layer`                     |
| `bitbake-layers add-layer /path/to/your_meta-layer`                | 新建一个自定义的 `layer`                 |
| `bitbake-layers remove-layer /path/to/your_meta-layer`             | 删除自定义的 `layer`                   |
| `bitbake-layers show-recipes`                                      | 列出所有的  `recipe`                  |
| `bitbake-layers show-overlayed`                                    | 列出所有冲突的  `recipe`                |
| `bitbake-layers show-appends`                                      | 列出所有的 `.bbappend` 文件             |
| `bitbake-layers flatten <output_dir>`                              | 将所有的 `.bb` 文件抽离出来放到 `output_dir` |
| `bitbake-layers show-cross-depends`                                | 列出所有 `layer` 的交叉依赖关系             |
| `bitbake-layers layerindex-show-depends <layer_name>`              | 根据 OE index 列出指定 `layer` 的依赖     |
| `bitbake-layers layerindex-fetch <layer name>`                     | 使用 OE index 拉取和添加 `layer`        |

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
echo BB_NO_NETWORK=1

# 将提前下载好的 git2_github.com.llvm.llvm-project.tar.gz 放到 DL_DIR 目录下
cp git2_github.com.llvm.llvm-project.tar.gz <build-dir>/downloads

# (可选) 如果离线包是以 git2_ 开头的，需要手动创建 .done 文件
cd <build-dir>/downloads
touch git2_github.com.llvm.llvm-project.tar.gz.done
```

## Q & A

**ERROR: No space left on device or exceeds fs.inotify.max_user_watches?**

- <https://unix.stackexchange.com/questions/13751/kernel-inotify-watch-limit-reached>
- <https://ruanyifeng.com/blog/2011/12/inode.html>

[^ref-cite-1]: [Cookbook:Appliance:Startup Scripts - Yocto Project](https://wiki.yoctoproject.org/wiki/Cookbook:Appliance:Startup_Scripts)

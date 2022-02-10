# 备份 Windows 系统

在系统发生崩溃后，我们通常不希望总是从零开始，一个一个地重新安装应用程序。
如果能够将电脑当前的状态（包括操作系统，用户配置信息等）保存起来就好了，下一次直接从这个状态直接恢复。

借助 WinPE 工具，我们可以轻松地实现上述目标。

Windows PE 或 WinPE，全称 Windows 预先安装环境，是 Microsoft Windows 的轻量版本。
主要为个人电脑开发商、工作站、服务器打造定制的操作系统环境，或系统离线时进行故障排除。
它取代了格式较旧的 MS-DOS 启动磁片/启动光盘 [^cite_ref-1]。

注意，如果我们使用 Windows 自带的升级工具来重装系统，Windows 可能会自动将我们之前的系统保存到
`C:\Windows.old` 。如果直接在文件夹上右击删除，往往没有足够的权限，比较推荐的做法是使用磁盘清理工具。

## 如何备份

1. 下载并安装 WinPE <https://www.wepe.com.cn>；
2. 选择 FAT32 制作 U 盘启动盘，注意，不建议选择 NTFS 或 exFat；
3. （备份）用 U 盘启动，进入可视化界面，使用 Ghost 封装系统；
4. （恢复）用 U 盘启动，进入可视化界面，使用 Ghost 恢复系统。

## 文件系统

Windows 操作系统支持 NTFS、FAT32、exFAT 三种不同文件系统。
文件系统是系统对文件的存放排列方式，不同格式的文件系统关系到数据如何在磁盘进行存储。

- NTFS 是目前 Windows 系统中一种**现代文件系统**，目前使用最广泛，内置的硬盘大多数都是 NTFS 格式；
- FAT32 是**老旧但通用**的文件系统，可以适配 Linux、Mac 或 Android（建议使用该格式制作启动盘）；
- exFAT 是 FAT32 文件格式的替代品，很多设备和操作系统都支持该文件系统，但是**目前用的不多** [^cite_ref-2]。

FAT（File Allocation Table，文件分配表）是一种由微软发明并拥有部分专利的**文件系统**。
供 MS-DOS 使用，也是所有非 NT（Windows New Technology，新技术视窗操作系统）核心的 Windows
系统使用的文件系统 [^cite_ref-3]。FAT32 表示文件分配表采用 32 位二进制数记录磁盘文件，单个文件最大寻址范围是
$2^{32} = 4 GB$。

## 参考文献

[^cite_ref-1]: Windows 预先安装环境 <https://en.wikipedia.org/wiki/Windows_Preinstallation_Environment>
[^cite_ref-2]: File Allocation Table <https://en.wikipedia.org/wiki/File_Allocation_Table>
[^cite_ref-3]: NTFS，FAT32 和 exFAT 文件系统有什么区别？ <https://zhuanlan.zhihu.com/p/32364955>

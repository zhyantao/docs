# 使用 Zotero 管理参考文献

## 配合 WPS 实现文献云同步

由于 Zotero 提供的默认工作空间大小只有 300M，空间很小，通常不能满足科研需求。本文介绍使用 WPS 的同步功能来实现文献备份。

【编辑】-【首选项】-【高级】-【文件和文件夹】

```{figure} ../_static/images/zotero_1.png

```

## 格式化 PDF 文件名

【工具】-【添加组件】-【设置】-【Install Add-on From File】

安装插件 <https://github.com/jlegewie/zotfile>，重启 Zotero。

【工具】-【Zotfile Preferences】

```{figure} ../_static/images/zotero_2.png

```

右击参考文献 - 【Management Attachments】 - 【Rename and Move】

## 解决文献链接失效的问题

参考文章 <https://darencard.net/blog/2019-09-19-zotero-file-relink/>

安装插件 <https://github.com/wshanks/Zutilo>，打开下面这两个选项：

```{figure} ../_static/images/zotero_4.png

```

选中一篇文献 - 右击 - 【Zutilo】 - 【显示附件路径】

选中全部文献 - 右击 - 【Zutilo】 - 【修改附件路径】 - 旧字符串填写【`attachments:`】 - 勾选【替换所有部分路径字符串实例】 - 新字符串填写附件所在目录的实际路径，比如【`D:/`】

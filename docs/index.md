# Read-the-Docs with Github

[![Documentation Status](https://readthedocs.org/projects/getstarted/badge)](https://readthedocs.org/projects/getstarted/builds)
[![GitHub Release](https://img.shields.io/github/v/release/zhyantao/getstarted)](https://github.com/zhyantao/getstarted/releases)
[![Curriculum Vitae](https://img.shields.io/badge/cv-ongoing-blue)](https://getstarted.readthedocs.io/_static/resume/cv.pdf)

## 环境部署

1、在 Github 上创建仓库（仓库名以 `notebook` 为例），创建完成后，克隆 `notebook` 到本地。

```bash
git clone https://github.com/<your_github_username>/notebook.git
```

2、将 [源代码压缩包](https://github.com/zhyantao/getstarted/archive/refs/heads/master.zip) 解压后，把压缩包中的内容全部复制到 `notebook` 文件夹中。

3、安装 Cairo 依赖（Windows 用户需提前下载 [MSYS2](./script/msys2.md)）。

```bash
# For Windows
pacman -S mingw-w64-x86_64-gtk2

# For Linux
sudo apt install libcairo2 libcairo2-dev
```

4、安装项目所需依赖，预览效果。

```bash
cd notebook
pip install -r requirements.txt
# export PATH=~/.local/bin:$PATH
make html
```

5、提交 `notebook` 仓库的修改到 Github。

```bash
git add . && git commit -m "v1.0.0" && git pull && git push
```

6、登录 [Readthedocs](https://readthedocs.org/) 导入刚刚新建的 Github 项目 `notebook`，构建完成后方可阅读文档。

## 撰写文档

1、把需要发表的文档放在 `notebook/docs` 文件夹中（写作格式可以是 `Markdown` 或者 `reStructuredText` ）

2、打开命令行，并切换到 `notebook` 目录下，输入 `make html`

3、打开 `notebook/build/html/index.html` 预览效果，确认无误后提交代码到 Github 仓库

4、重新打开 [Readthedocs](https://readthedocs.org/) 文档的网址，查看新发表的博客（有延迟，可能需要等待）。

## 注意事项

在 `notebook/docs` 下的添加新文章后需要在 `notebook/docs/index.md` 中添加一条记录。

```{toctree}
:caption: 专业基础
:maxdepth: 2
:glob:
:hidden:

theory/index
cc/index
assembly/index
java/index
python/index
js/index
script/index
config/index
appendix/index
```

```{toctree}
:caption: 外部链接
:maxdepth: 1
:glob:
:hidden:

Competitive Programming <https://getstarted.readthedocs.io/_static/cheatsheet/CompetitiveProgramming-Steven&Felix-NUS.pdf>
Programmer's Handbook <https://getstarted.readthedocs.io/_static/cheatsheet/CompetitiveProgrammer’sHandbook.pdf>
Algorithm Design Manual <https://getstarted.readthedocs.io/_static/cheatsheet/SkienaTheAlgorithmDesignManual.pdf>
ACM 常用算法模板 <https://getstarted.readthedocs.io/_static/cheatsheet/ACMTemplate-kuangbin.pdf>
PlantUML Online Editor <https://pansinm.github.io/plantuml-editor/>
C++ 小抄表 <https://getstarted.readthedocs.io/_static/cheatsheet/cpp.pdf>
C 语言小抄表 <https://getstarted.readthedocs.io/_static/cheatsheet/c.pdf>
Java 小抄表 <https://getstarted.readthedocs.io/_static/cheatsheet/java.pdf>
```

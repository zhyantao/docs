Git 常用命令
=============

.. note::

    推荐一个比较好的学习 Git 命令的网站 `Learn Git Branching <https://oschina.gitee.io/learn-git-branching/>`_。

仓库
~~~~~

.. code-block:: bash

    # 在当前目录新建一个Git代码库
    $ git init

    # 新建一个目录，将其初始化为Git代码库
    $ git init [project-name]

    # 下载一个项目和它的整个代码历史
    $ git clone [url]

配置
~~~~~

.. code-block:: bash

    # 显示当前的Git配置
    $ git config --list

    # 编辑Git配置文件
    $ git config -e [--global]

    # 设置提交代码时的用户信息
    $ git config [--global] user.name "[name]"
    $ git config [--global] user.email "[email address]"

增加/删除文件
~~~~~~~~~~~~~~

.. code-block:: bash

    # 添加指定文件到暂存区
    $ git add [file1] [file2] ...

    # 添加指定目录到暂存区，包括子目录
    $ git add [dir]

    # 添加当前目录的所有文件到暂存区
    $ git add .

    # 添加每个变化前，都会要求确认
    # 对于同一个文件的多处变化，可以实现分次提交
    $ git add -p

    # 删除工作区文件，并且将这次删除放入暂存区
    $ git rm [file1] [file2] ...

    # 停止追踪指定文件，但该文件会保留在工作区
    $ git rm --cached [file]

    # 改名文件，并且将这个改名放入暂存区
    $ git mv [file-original] [file-renamed]

代码提交
~~~~~~~~~

.. code-block:: bash

    # 提交暂存区到仓库区
    $ git commit -m [message]

    # 提交暂存区的指定文件到仓库区
    $ git commit [file1] [file2] ... -m [message]

    # 提交工作区自上次commit之后的变化，直接到仓库区
    $ git commit -a

    # 提交时显示所有diff信息
    $ git commit -v

    # 使用一次新的commit，替代上一次提交
    # 如果代码没有任何新变化，则用来改写上一次commit的提交信息
    $ git commit --amend -m [message]

    # 重做上一次commit，并包括指定文件的新变化
    $ git commit --amend [file1] [file2] ...

标准格式：（任何一行都不得超过72个字符（或100个字符）。这是为了避免自动换行影响美观。）

.. code-block:: text

    <type>(<scope>): <subject>
    // 空一行
    <body>
    // 空一行
    <footer>

**type（必须）** 如果type为feat和fix，则该 commit 将出现在 Change log 中。其他情况建议不要放入 Change log。

- feat：新功能（feature）
- fix：修补bug
- docs：文档（documentation）
- style： 格式（不影响代码运行的变动）
- refactor：重构（即不是新增功能，也不是修改bug的代码变动）
- test：增加测试
- chore：构建过程或辅助工具的变动

**scope（可选）** 用于说明 commit 影响的范围，比如数据层、控制层、视图层等等，视项目不同而不同。

**subject（必须）** 是 commit 目的的简短描述，不超过50个字符。

- 以动词开头，使用第一人称现在时，比如change，而不是changed或changes
- 第一个字母小写
- 结尾不加句号（.）

**body（可选）** 是对本次 commit 的详细描述，可以分成多行。下面是一个范例。

.. code-block:: text

    More detailed explanatory text, if necessary.  Wrap it to 
    about 72 characters or so. 

    Further paragraphs come after blank lines.

    - Bullet points are okay, too
    - Use a hanging indent

有两个注意点。（1）使用第一人称现在时，比如使用 change 而不是 changed 或 changes。（2）应该说明代码变动的动机，以及与以前行为的对比。

**footer（可选）**

footer 部分只用于两种情况。（1）不兼容变动：如果当前代码与上一个版本不兼容，则 footer 部分以 ``BREAKING CHANGE`` 开头，后面是对变动的描述、以及变动理由和迁移方法。

.. code-block:: text

    BREAKING CHANGE: isolate scope bindings definition has changed.

        To migrate the code follow the example below:

        Before:

        scope: {
        myAttr: 'attribute',
        }

        After:

        scope: {
        myAttr: '@',
        }

        The removed `inject` wasn't generaly useful for directives so there should be no code using it.

（2）关闭 Issue：如果当前 commit 针对某个 issue，那么可以在 footer 部分关闭这个 issue 。

.. code-block:: text

    Closes #234, #245, #992

分支
~~~~~

.. code-block:: bash

    # 列出所有本地分支
    $ git branch

    # 列出所有远程分支
    $ git branch -r

    # 列出所有本地分支和远程分支
    $ git branch -a

    # 新建一个分支，但依然停留在当前分支
    $ git branch [branch-name]

    # 新建一个分支，并切换到该分支
    $ git checkout -b [branch]

    # 新建一个分支，指向指定commit
    $ git branch [branch] [commit]

    # 新建一个分支，与指定的远程分支建立追踪关系
    $ git branch --track [branch] [remote-branch]

    # 切换到指定分支，并更新工作区
    $ git checkout [branch-name]

    # 切换到上一个分支
    $ git checkout -

    # 建立追踪关系，在现有分支与指定的远程分支之间
    $ git branch --set-upstream [branch] [remote-branch]

    # 合并指定分支到当前分支
    $ git merge [branch]

    # 选择一个commit，合并进当前分支
    $ git cherry-pick [commit]

    # 删除分支
    $ git branch -d [branch-name]

    # 删除远程分支
    $ git push origin --delete [branch-name]
    $ git branch -dr [remote/branch]

.. csv-table:: Git 分支命名规范
    :header: "分支", "命名", "说明"
    :widths: 12, 12, 40

    "主分支", "master", "主分支，所有提供给用户使用的正式版本，都在这个主分支上发布"
    "开发主分支", "dev", "开发分支，永远是功能最新最全的分支"
    "功能分支", "feature-*", "新功能分支，某个功能点正在开发阶段"
    "发布版本", "release-*", "发布定期要上线的功能"
    "修复发布版本分支",	"bugfix-release-*", "修复测试bug"
    "紧急修复分支", "bugfix-master-*", "紧急修复线上代码的 bug"

标签
~~~~~

.. code-block:: bash

    # 列出所有tag
    $ git tag

    # 新建一个tag在当前commit
    $ git tag [tag]

    # 新建一个tag在指定commit
    $ git tag [tag] [commit]

    # 删除本地tag
    $ git tag -d [tag]

    # 删除远程tag
    $ git push origin :refs/tags/[tagName]

    # 查看tag信息
    $ git show [tag]

    # 提交指定tag
    $ git push [remote] [tag]

    # 提交所有tag
    $ git push [remote] --tags

    # 新建一个分支，指向某个tag
    $ git checkout -b [branch] [tag]

查看信息
~~~~~~~~~

.. code-block:: bash

    # 显示有变更的文件
    $ git status

    # 显示当前分支的版本历史
    $ git log

    # 显示commit历史，以及每次commit发生变更的文件
    $ git log --stat

    # 搜索提交历史，根据关键词
    $ git log -S [keyword]

    # 显示某个commit之后的所有变动，每个commit占据一行
    $ git log [tag] HEAD --pretty=format:%s

    # 显示某个commit之后的所有变动，其"提交说明"必须符合搜索条件
    $ git log [tag] HEAD --grep feature

    # 显示某个文件的版本历史，包括文件改名
    $ git log --follow [file]
    $ git whatchanged [file]

    # 显示指定文件相关的每一次diff
    $ git log -p [file]

    # 显示过去5次提交
    $ git log -5 --pretty --oneline

    # 显示所有提交过的用户，按提交次数排序
    $ git shortlog -sn

    # 显示指定文件是什么人在什么时间修改过
    $ git blame [file]

    # 显示暂存区和工作区的差异
    $ git diff

    # 显示暂存区和上一个commit的差异
    $ git diff --cached [file]

    # 显示工作区与当前分支最新commit之间的差异
    $ git diff HEAD

    # 显示两次提交之间的差异
    $ git diff [first-branch]...[second-branch]

    # 显示今天你写了多少行代码
    $ git diff --shortstat "@{0 day ago}"

    # 显示某次提交的元数据和内容变化
    $ git show [commit]

    # 显示某次提交发生变化的文件
    $ git show --name-only [commit]

    # 显示某次提交时，某个文件的内容
    $ git show [commit]:[filename]

    # 显示当前分支的最近几次提交
    $ git reflog

远程同步
~~~~~~~~~

.. code-block:: bash

    # 下载远程仓库的所有变动
    $ git fetch [remote]

    # 显示所有远程仓库
    $ git remote -v

    # 显示某个远程仓库的信息
    $ git remote show [remote]

    # 增加一个新的远程仓库，并命名
    $ git remote add [shortname] [url]

    # 取回远程仓库的变化，并与本地分支合并
    $ git pull [remote] [branch]

    # 上传本地指定分支到远程仓库
    $ git push [remote] [branch]

    # 强行推送当前分支到远程仓库，即使有冲突
    $ git push [remote] --force

    # 推送所有分支到远程仓库
    $ git push [remote] --all

撤销
~~~~~

.. code-block:: bash

    # 恢复暂存区的指定文件到工作区
    $ git checkout [file]

    # 恢复某个commit的指定文件到暂存区和工作区
    $ git checkout [commit] [file]

    # 恢复暂存区的所有文件到工作区
    $ git checkout .

    # 重置暂存区的指定文件，与上一次commit保持一致，但工作区不变
    $ git reset [file]

    # 重置暂存区与工作区，与上一次commit保持一致
    $ git reset --hard

    # 重置当前分支的指针为指定commit，同时重置暂存区，但工作区不变
    $ git reset [commit]

    # 重置当前分支的HEAD为指定commit，同时重置暂存区和工作区，与指定commit一致
    $ git reset --hard [commit]

    # 重置当前HEAD为指定commit，但保持暂存区和工作区不变
    $ git reset --keep [commit]

    # 新建一个commit，用来撤销指定commit
    # 后者的所有变化都将被前者抵消，并且应用到当前分支
    $ git revert [commit]

    暂时将未提交的变化移除，稍后再移入
    $ git stash
    $ git stash pop

其他
~~~~~

.. code-block:: bash

    # 生成一个可供发布的压缩包
    $ git archive

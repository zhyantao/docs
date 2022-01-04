Git
===

初始化仓库
~~~~~~~~~~

.. code-block:: bash

    # 在当前目录新建一个 Git 代码库
    $ git init

    # 新建一个目录，将其初始化为 Git 代码库
    $ git init [project-name]

    # 下载一个项目和它的整个代码历史
    $ git clone [url]


配置信息
~~~~~~~~

.. code-block:: bash

    # 显示当前的 Git 配置
    $ git config --list

    # 编辑 Git 配置文件
    $ git config -e [--global]

    # 设置提交代码时的用户信息
    $ git config [--global] user.name "[name]"
    $ git config [--global] user.email "[email address]"


工作区管理
~~~~~~~~~~

.. code-block:: bash

    # 恢复暂存区的指定文件到工作区
    $ git checkout [file]

    # 恢复暂存区的所有文件到工作区
    $ git checkout .

    # 删除工作区文件，并且将这次删除放入暂存区
    $ git rm [file1] [file2] ...

    # 停止同步指定文件，但该文件会保留在工作区
    $ git rm --cached [file]

    # 重命名文件，并且将这个改名放入暂存区
    $ git mv [file-original] [file-renamed]

    # 合并分支时，暂时将工作区未提交的冲突删除，稍后再恢复
    $ git stash
    $ git stash pop


暂存区管理
~~~~~~~~~~

.. code-block:: bash

    # 添加当前目录的所有文件到暂存区
    $ git add .

    # 添加指定文件到暂存区
    $ git add [file1] [file2] ...

    # 添加指定目录到暂存区，包括子目录
    $ git add [dir]

    # 重置暂存区的指定文件，与上一次 commit 保持一致，但工作区不变
    $ git reset [file]

    # 重置暂存区与工作区，与上一次 commit 保持一致
    $ git reset --hard

    # 重置当前分支的指针为指定 commit，同时重置暂存区，但工作区不变
    $ git reset [commit]

    # 重置当前分支的 HEAD 为指定 commit，同时重置暂存区和工作区，与指定 commit 一致
    $ git reset --hard [commit]

    # 重置当前 HEAD 为指定 commit，但保持暂存区和工作区不变
    $ git reset --keep [commit]


本地分支管理
~~~~~~~~~~~~

.. code-block:: bash

    # 列出所有本地分支
    $ git branch

    # 新建一个本地分支，但依然停留在当前分支
    $ git branch [branch-name]

    # 新建一个分支，并切换到该分支
    $ git checkout -b [branch]

    # 切换本地分支，并更新工作区
    $ git checkout [branch-name]

    # 建立同步关系，在现有分支与指定的远程分支之间
    $ git branch --set-upstream [branch] [remote-branch]

    # 提交时显示所有diff信息
    $ git commit -v

    # 提交暂存区到本地分支，并做简要说明
    $ git commit -m "message"

    # 提交暂存区到本地分支，并做详细说明
    $ git commit

    # 合并指定分支到当前分支（适用场景：主分支 <- 子分支）
    $ git merge [feature-branch]

    # 合并指定分支到当前分支（适用场景：子分支 <-- 主分支）
    $ git rebase [master-branch]

    # 删除本地分支
    $ git branch -d [branch-name]


.. admonition:: Git 分支命名规范
    :class: dropdown

    .. csv-table::
        :header: "分支", "命名", "说明"
        :widths: 15, 15, 40

        "主分支", "master", "主分支是提供给用户使用的正式版本"
        "开发分支", "dev", "开发分支永远是功能\ **最新最全**\ 的分支"
        "功能分支", "feature-*", "新功能分支开发完成后\ **需删除**"
        "发布版本", "release-*", "发布定期要上线的功能"
        "发布版本修复分支",	"bugfix-release-*", "修复测试 Bug"
        "紧急修复分支", "bugfix-master-*", "紧急修复线上代码的 Bug"


远程分支管理
~~~~~~~~~~~~

.. code-block:: bash

    # 列出所有远程分支
    $ git branch -r

    # 下载远程分支的所有变动
    $ git fetch [remote]

    # 显示所有远程分支（一般是 origin）
    $ git remote -v

    # 取回远程分支的变化，并与本地分支合并
    $ git pull [remote] [branch]

    # 上传本地指定分支到远程分支
    $ git push [remote] [branch]

    # 强行推送当前分支到远程分支，即使有冲突
    $ git push [remote] --force

    # 推送所有分支到远程分支
    $ git push [remote] --all

    # 删除远程分支
    $ git push origin --delete [branch-name]


查看变更
~~~~~~~~

.. code-block:: bash

    # 显示有变更的文件
    $ git status

    # 显示暂存区和工作区的差异
    $ git diff

    # 显示暂存区和上一个 commit 的差异
    $ git diff --cached [file]

    # 显示工作区与当前分支最新 commit 之间的差异
    $ git diff HEAD

    # 显示当前分支的版本历史
    $ git log


记录关键节点
~~~~~~~~~~~~

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


.. note::

    更直观的方式体验 Git 命令：\ `Learn Git Branching <https://oschina.gitee.io/learn-git-branching/>`_。


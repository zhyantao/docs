.. _git-syntax:

Git
===

工作流程
~~~~~~~~

.. figure:: ../../_static/images/bg2015120901.png

    图源阮一峰的博客 [1]_

- Workspace：工作区
- Index / Stage：暂存区
- Repository：仓库区（或本地仓库）
- Remote：远程仓库

在 Learn Git Branching 上，可以更轻松直观地体验 Git 完整流程 [2]_。


常用命令
~~~~~~~~

.. admonition:: 解释本文中出现的名词

    - ``<commit>`` 表示历史提交记录，可通过 ``git log`` 查询，推荐使用相对引用 ``HEAD`` 查询；
    - ``<remote>`` 表示指向远程仓库的指针，可通过 ``git remote`` 查询，一般是 ``origin``；
    - ``<branch>`` 表示分支名称，可通过 ``git branch`` 查询。

Git 全局设置
-------------

.. code-block:: bash

    git config --global user.name "zhyantao"
    git config --global user.email "zh6tao@gmail.com"

.. admonition:: GitHub 不显示头像

    如果你在 Github 上修改了提交邮箱，而没有修改本地提交邮箱的话，会发现你的头像在提交记录上无法显示。
    因此，本地的提交邮箱应当与远程仓库保持一致。
    通过 **再次运行** 上面的命令可以更新本地提交邮箱，也可以修改 ``~/.gitconfig`` 文件。

创建 git 仓库
--------------

.. code-block:: bash

    mkdir repository
    cd repository
    git init
    git add .
    git commit -m "Initial commit"
    git remote add origin git@gitee.com:username/repository.git
    git push -u origin "master"

已有仓库
--------

.. code-block:: bash

    cd existing_git_repo
    git remote add origin git@gitee.com:username/repository.git
    git push -u origin "master"


仓库
~~~~~

.. code-block:: bash

    # 在当前目录新建一个 Git 代码库
    $ git init

    # 新建一个目录，将其初始化为 Git 代码库
    $ git init [project-name]

    # 下载一个项目和它的整个代码历史
    $ git clone <url>


配置
~~~~

.. code-block:: bash

    # 显示当前的 Git 配置
    $ git config --list

    # 编辑 Git 配置文件
    $ git config -e [--global]

    # 设置提交代码时的用户信息
    $ git config [--global] user.name "<name>"
    $ git config [--global] user.email "<email address>"

    # 只关注文件内容变更，忽略文件权限变化
    $ git config --global core.filemode false


增加/删除文件
~~~~~~~~~~~~~

.. code-block:: bash

    # 添加指定文件到暂存区
    $ git add <file1> <file2> ...

    # 添加指定目录到暂存区，包括子目录
    $ git add <dir>

    # 添加当前目录的所有文件到暂存区
    $ git add .

    # 添加每个变化前，都会要求确认
    # 对于同一个文件的多处变化，可以实现分次提交
    $ git add -p

    # 删除工作区文件，并且将这次删除放入暂存区
    $ git rm <file1> <file2> ...

    # 停止追踪指定文件，但该文件会保留在工作区
    $ git rm --cached <filename>

    # 改名文件，并且将这个改名放入暂存区
    $ git mv <file-original> <file-renamed>


代码提交
~~~~~~~~

.. code-block:: bash

    # 提交暂存区到仓库区
    $ git commit -m "<message>"

    # 提交暂存区的指定文件到仓库区
    $ git commit <file1> <file2> ... -m "<message>"

    # 提交工作区自上次 commit 之后的变化，直接到仓库区
    $ git commit -a

    # 提交时显示所有 diff 信息
    $ git commit -v

    # 使用一次新的 commit，替代上一次提交
    # 如果代码没有任何新变化，则用来改写上一次 commit 的提交信息
    $ git commit --amend -m "<message>"

    # 重做上一次 commit，并包括指定文件的新变化
    $ git commit --amend <file1> <file2> ...


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
    $ git branch <branch>

    # 新建一个分支，并切换到该分支
    $ git checkout -b <branch>

    # 新建一个分支，指向指定 commit
    $ git branch <branch> <commit>

    # 新建一个分支，与指定的远程分支建立追踪关系
    $ git branch --track <local-branch> <remote-branch>

    # 切换到指定分支，并更新工作区
    $ git checkout <branch>

    # 切换到上一个分支
    $ git checkout -

    # 建立追踪关系，在现有分支与指定的远程分支之间
    $ git branch --set-upstream <local-branch> <remote-branch>

    # 重命名分支
    $ git branch -m <old-name> <new-name>

    # 合并指定分支到当前分支（适用场景：主分支 <- 子分支）
    $ git merge <branch>

    # 合并指定分支到当前分支（适用场景：子分支 <-- 主分支）
    $ git rebase <branch>

    # 选择一个 commit，合并进当前分支
    $ git cherry-pick <commit>

    # 删除分支
    $ git branch -d <branch>

    # 删除远程分支
    $ git push origin --delete <branch>
    $ git branch -dr <remote/branch>

.. admonition:: 分支命名规范

    .. csv-table::
        :header: "分支", "命名", "说明"
        :widths: 15, 15, 40
    
        "主分支", "master", "主分支是提供给用户使用的正式版本"
        "开发分支", "dev", "开发分支永远是功能\ **最新最全**\ 的分支"
        "功能分支", "feature-*", "新功能分支开发完成后\ **需删除**"
        "发布版本", "release-*", "发布定期要上线的功能"
        "发布版本修复分支",	"bugfix-release-*", "修复测试 Bug"
        "紧急修复分支", "bugfix-master-*", "紧急修复线上代码的 Bug"

.. admonition:: 冲突处理

    有时想把 ``<other-branch>`` 的内容合并到当前所在分支，使用命令
    ``git fetch <remote> <other-branch>`` 和 ``git merge FETCH_HEAD``
    后，发现 **有冲突**。冲突的文件会有类似如下所示的结果：

    .. code-block:: python

        <<<<<<< HEAD (冲突开始的位置)
        最新的修改
        =======
        上一次提交的修改
        >>>>>>> 上一个分支的名称 (冲突结束的位置)

    因此，我们的目标就是对冲突开始和结束之间的部分进行删减。
    解决完冲突后，继续使用命令 ``git add`` 和 ``git commit`` 命令即可完成后续开发工作。


标签
~~~~

.. code-block:: bash

    # 列出所有 tag
    $ git tag

    # 新建一个 tag 在当前 commit
    $ git tag <tag>

    # 新建一个 tag 在指定 commit
    $ git tag <tag> <commit>

    # 删除本地 tag
    $ git tag -d <tag>

    # 删除远程 tag
    $ git push origin :refs/tags/<tag-name>

    # 查看 tag 信息
    $ git show <tag>

    # 提交指定 tag
    $ git push <remote> <tag>

    # 提交所有 tag
    $ git push <remote> --tags

    # 新建一个分支，指向某个 tag
    $ git checkout -b <branch> <tag>

    # 生成一个可供发布的压缩包
    $ git archive


查看信息
~~~~~~~~

.. code-block:: bash

    # 显示有变更的文件
    $ git status

    # 显示当前分支的版本历史
    $ git log

    # 显示 commit 历史，以及每次 commit 发生变更的文件
    $ git log --stat

    # 搜索提交历史，根据关键词
    $ git log -S <keyword>

    # 显示某个 commit 之后的所有变动，每个 commit 占据一行
    $ git log <tag> HEAD --pretty=format:%s

    # 显示某个 commit 之后的所有变动，其"提交说明"必须符合搜索条件
    $ git log <tag> HEAD --grep feature

    # 显示某个文件的版本历史，包括文件改名
    $ git log --follow <filename>
    $ git whatchanged <filename>

    # 显示指定文件相关的每一次 diff
    $ git log -p <filename>

    # 显示过去 5 次提交
    $ git log -5 --pretty --oneline

    # 显示所有提交过的用户，按提交次数排序
    $ git shortlog -sn

    # 显示指定文件是什么人在什么时间修改过
    $ git blame <filename>

    # 显示暂存区和工作区的差异
    $ git diff

    # 显示暂存区和上一个 commit 的差异
    $ git diff --cached <filename>

    # 显示工作区与当前分支最新 commit 之间的差异
    $ git diff HEAD

    # 显示两次提交之间的差异
    $ git diff <first-branch> <second-branch>

    # 显示今天你写了多少行代码
    $ git diff --shortstat "@{0 day ago}"

    # 显示某次提交的元数据和内容变化
    $ git show <commit>

    # 显示某次提交发生变化的文件
    $ git show --name-only <commit>

    # 显示某次提交时，某个文件的内容
    $ git show <commit>:<filename>

    # 显示当前分支的最近几次提交
    $ git reflog


远程同步
~~~~~~~~

.. code-block:: bash

    # 下载远程仓库的所有变动
    $ git fetch <remote>

    # 显示所有远程仓库
    $ git remote -v

    # 更新远程仓库链接
    $ git remote set-url <remote> <url>

    # 显示某个远程仓库的信息
    $ git remote show <remote>

    # 增加一个新的远程仓库，并命名
    $ git remote add <shortname> <url>

    # 取回远程仓库的变化，并与本地分支合并
    $ git pull <remote> <branch>

    # 上传本地指定分支到远程仓库
    $ git push <remote> <branch>

    # 强行推送当前分支到远程仓库，即使有冲突
    $ git push <remote> --force

    # 推送所有分支到远程仓库
    $ git push <remote> --all

撤销
~~~~

.. code-block:: bash

    # 恢复暂存区的指定文件到工作区
    $ git checkout <filename>

    # 恢复某个 commit 的指定文件到暂存区和工作区
    $ git checkout <commit> <filename>

    # 恢复暂存区的所有文件到工作区
    $ git checkout .

    # 重置暂存区的指定文件，与上一次 commit 保持一致，但工作区不变
    $ git reset <filename>

    # 重置暂存区与工作区，与上一次 commit 保持一致
    $ git reset --hard

    # 重置当前分支的指针为指定 commit，同时重置暂存区，但工作区不变
    $ git reset <commit>

    # 重置当前分支的 HEAD 为指定 commit，同时重置暂存区和工作区，与指定 commit 一致
    $ git reset --hard <commit>

    # 重置当前 HEAD 为指定 commit，但保持暂存区和工作区不变
    $ git reset --keep <commit>

    # 新建一个 commit，用来撤销某个旧的 commit，但保留旧 commit 之后的 commit
    $ git revert <commit>

    # 暂时将未提交的变化移除，稍后再移入
    $ git stash
    $ git stash pop

第三方库
~~~~~~~~

.. code-block:: bash

    # 添加 submodule 到现有项目
    git submodule add <remote> <submodule-dir>

    # 从当前项目移除 submodule
    git submodule deinit -f <submodule-dir> # 删除 .git/config 中的相关条目
    rm -rf .git/modules/<submodule-dir>     # 删除 .git/modules 中的 submodule 文件夹
    git rm -f <submodule-dir>               # 删除 submodule 文件夹和 .gitmodules 中的相关条目

    # 更新 submodule 的 URL
    # 首先修改 .gitmodules 文件中的 url 属性
    # 如果已经初始化了，先删除 submodule 在本地相应的文件夹
    git submodule sync
    git submodule update --init --recursive

    # 把依赖的 submodule 全部拉取到本地并更新为最新版本
    git submodule update --init --recursive

    # 更新 submodule 为远程项目的最新版本
    git submodule update --remote

    # 更新指定的 submodule 为远程的最新版本
    git submodule update --remote <submodule-dir>

    # 检查 submodule 是否有提交未推送，如果有，则使本次提交失败
    git push --recurse-submodules=check

    # 先推送 submodule 的更新，然后推送主项目的更新
    # 如果 submodule 推送失败，那么推送任务直接终止
    git push --recurse-submodules=on-demand

    # 所有的 submodule 会被依次推送到远端，但是 superproject 将不会被推送
    git push --recurse-submodules=while

    # 与 while 相反，只推送 superproject，不推送其他 submodule
    git push --recurse-submodules=no

    # 拉取所有子仓库（fetch）并 merge 到所跟踪的分支上
    git pull --recurse-submodules

    # 查看 submodule 所有改变
    git diff --submodule

    # 对所有 submodule 执行命令，非常有用。如 git submodule foreach 'git checkout main'
    git submodule foreach <arbitrary-command-to-run>

gitignore 匹配规则
~~~~~~~~~~~~~~~~~~~

.. admonition:: 匹配规则
    
    - ``gitignore`` 只匹配其所在目录及子目录的文件。
    - 已经被 ``git track`` 的文件不受 ``gitignore`` 影响。
    - 子目录的 ``gitignore`` 文件规则会覆盖父目录的规则。

.. code-block:: bash

    # 忽略特定文件
    ModelIndex.xml
    ExportedFiles.xml

    # [] 匹配包含在 [] 范围内的任意字符
    [Mm]odel/[Dd]eployment

    # 使用 \ 加空格匹配包含空格的文件或文件夹
    Program\ Files

    # 忽略名为 hello 的目录和该目录下的所有文件，但是不会匹配名为 hello 的文件
    hello/

    # 忽略名为 hello 的文件
    hello

    # 忽略名为 b 的文件，该文件在文件夹 a 下，且该文件的路径为 a/b 或 a/任意路径/b
    a/**/b

    # 强制包含指定文件夹，* 匹配除了 / 之外任意数量的任意字符串
    !Model/Portal/*/SupportFiles/[Bb]in/

    # 强制包含指定文件，? 匹配除了 / 之外的任意一个字符
    !Model/Portal/PortalTemplates/?/SupportFiles/[Bb]in


显示 git 分支
~~~~~~~~~~~~~~

打开 ``~/.bashrc`` 做如下修改：

.. code-block:: bash

    # display git branch on bash
    git_branch() {
    branch="`git branch 2>/dev/null | grep "^\*" | sed -e "s/^\*\ //"`"
    if [ "${branch}" != "" ];then
        if [ "${branch}" = "(no branch)" ];then
            branch="(`git rev-parse --short HEAD`...)"
        fi
        echo " ($branch)"
    fi
    }

    PS1 = '\[\033[01;32m\]$(git_branch)\[\033[00m\]' # 补充到 PS1 变量上


自动补全
~~~~~~~~~

.. code-block:: bash

    # 下载 git-completition.bash
    wget https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash
    
    # 将 git-completition.bash 放在服务器上    
    cp ~/git-completion.bash /etc/bash_completion.d/
    
    # 使 git-completition.bash 生效
    . /etc/bash_completion.d/git-completion.bash
    
    # 编辑 /etc/profile 添加如下内容
    if [ -f /etc/bash_completion.d/git-completion.bash ]; then
        . /etc/bash_completion.d/git-completion.bash
    fi

    # 使 /etc/profile 生效
    source /etc/profile


.. [1] 阮一峰的网络日志 - 常用 Git 命令清单 [`webpage <https://www.ruanyifeng.com/blog/2015/12/git-cheat-sheet.html>`__]
.. [2] Learn Git Branching [`webpage <https://oschina.gitee.io/learn-git-branching/>`__]

(git-syntax)=

# Git-2

## 工作流程

```{figure} ../_static/images/basic-usage.*

```

上面的四条命令在工作目录、暂存目录（也叫做索引）和仓库之间复制文件。

- `git add files` 把当前文件放入暂存区域。
- `git commit` 给暂存区域生成快照并提交。
- `git reset -- files` 用来撤销最后一次 `git add files`，你也可以用 `git reset` 撤销所有暂存区域文件。
- `git checkout -- files` 把文件从暂存区域复制到工作目录，用来丢弃本地修改。

你可以用 `git reset -p`, `git checkout -p`, `git add -p` 进入交互模式。

也可以跳过暂存区域直接从仓库取出文件或者直接提交代码。

```{figure} ../_static/images/basic-usage-2.*

```

- `git commit -a` 相当于先运行 `git add` 把所有当前目录下的文件加入暂存区域，再运行 `git commit`。
- `git commit files` 将工作目录中文件的快照同时提交到暂存区域和仓库中。
- `git checkout HEAD -- files` 回滚到最后一次提交。

注：

1. 本文图片均摘自 [图解 Git](https://marklodato.github.io/visual-git-guide/index-zh-cn.html)。
2. 在 [Learn Git Branching](https://learngitbranching.js.org/?locale=zh_CN) 可以直观地体验 Git 流程。

## 快速上手

本节介绍典型的 Git 工作流程：`创建仓库` > `编辑源代码` > `提交源代码`。

```bash
# 本地创建空仓库
mkdir repository
cd repository
git init

# (可选) 添加子仓库
git submodule add https://github.com/username/subrepo.git path/to/subrepo
git submodule update --init --recursive
# To update submodule, `cd` to the folder of your repository, run:
git submodule update --remote --merge

# (可选) 更新子仓库
cd path/to/subrepo
git checkout -b master
git pull origin master

# 设置远程仓库地址（如果 git remote -v 已经有结果，无需设置这一步）
git remote add origin git@gitee.com:username/repository.git

# 查看 <remote> 及其 URL
git remote -v

# 查看远程分支 <branch>
git fetch
git branch -r

# 切换到分支
git checkout <branch>

# 编辑源代码
code <directory>

# 查看文件变更
git status

# 查看文件内容变更
git diff path/to/file

# 将代码添加到暂存区
git add .

# 将代码添加到本地仓库
git commit -m "commit message"

# 将代码添加到远程仓库
# -u (set upstream)：设置本地仓库与远程仓库的关联关系（仅在创建仓库后的首次 push 时需要）
# HEAD 表示本地分支，refs/for 表示提交后的代码需要 Code Review
git push [-u] $(git remote) HEAD:refs/for/$(git branch --show-current)

# 查看 <commit>
git log --graph
```

## 配置仓库 config

```bash
# 配置用户名和邮箱
git config --global user.name "zhyantao"
git config --global user.email "yantao.z@outlook.com"

# 解决 VSCode 未修改代码，但显示变更的问题
# 1) 修改全局配置
git config --global --replace-all core.filemode false
git config --global --replace-all core.autocrlf false
# 2) 修改当前仓库的本地配置
git config --replace-all core.filemode false
git config --replace-all core.autocrlf false
# 3) 清除 Git 的索引（或称为缓存）
git rm --cached -r .
git reset HEAD .
```

:::{dropdown} GitHub 不显示头像
如果你在 Github 上修改了提交邮箱，而没有修改本地提交邮箱的话，会发现你的头像在提交记录上无法显示。因此，本地的提交邮箱应当与远程仓库保持一致。修改 `~/.gitconfig` 可解决问题。
:::

## 更新本地仓库 pull/fetch

```bash
# 下载远程仓库的所有变动
git fetch <remote>

# 显示所有远程仓库
git remote -v

# 更新远程仓库链接
git remote set-url <remote> <url>

# 显示某个远程仓库的信息
git remote show <remote>

# 增加一个新的远程仓库，并命名
git remote add <shortname> <url>

# 取回远程仓库的变化，并与本地分支合并
git pull <remote> <branch>

# 上传本地指定分支到远程仓库
git push <remote> <branch>

# 强行推送当前分支到远程仓库，即使有冲突
git push <remote> --force

# 推送所有分支到远程仓库
git push <remote> --all
```

## 比较文件差异 status/diff

```bash
# 显示有变更的文件
git status

# 显示有变更的文件，包括被删除的文件
git status -u

# 显示暂存区和工作区的差异
git diff

# 显示暂存区和上一个 commit 的差异
git diff --cached <filename>

# 显示工作区与当前分支最新 commit 之间的差异
git diff HEAD

# 显示两次提交之间的差异
git diff <first-branch> <second-branch>

# 显示今天你写了多少行代码
git diff --shortstat "@{0 day ago}"
```

```{figure} ../_static/images/diff.*

```

## 管理文件变更 add/rm

```bash
# 添加指定文件到暂存区
git add <file1> <file2> ...

# 添加指定目录到暂存区，包括子目录
git add <dir>

# 添加当前目录的所有文件到暂存区
git add .

# 添加每个变化前，都会要求确认
# 对于同一个文件的多处变化，可以实现分次提交
git add -p

# 删除工作区文件，并且将这次删除放入暂存区
git rm <file1> <file2> ...

# 停止追踪指定文件，但该文件会保留在工作区
git rm --cached <filename>

# 改名文件，并且将这个改名放入暂存区
git mv <file-original> <file-renamed>
```

## 创建快照并撰写日志 commit

```bash
# 提交暂存区到仓库区
git commit -m "<message>"

# 提交暂存区的指定文件到仓库区
git commit <file1> <file2> ... -m "<message>"

# 提交工作区自上次 commit 之后的变化，直接到仓库区
git commit -a

# 提交时显示所有 diff 信息
git commit -v

# 使用一次新的 commit，替代上一次提交
# 如果代码没有任何新变化，则用来改写上一次 commit 的提交信息
git commit --amend -m "<message>"

# 重做上一次 commit，并包括指定文件的新变化
git commit --amend <file1> <file2> ...
```

:::{dropdown} 代码提交规范

| 类型       | 说明                         |
| ---------- | ---------------------------- |
| `feat`     | 新功能                       |
| `fix`/`to` | 修复漏洞                     |
| `docs`     | 文档                         |
| `style`    | 格式（不影响代码运行的变动） |
| `refactor` | 重构（不改变功能的代码变动） |
| `perf`     | 优化相关，比如提升性能、体验 |
| `test`     | 增加测试                     |
| `chore`    | 构建过程或辅助工具的变动     |
| `revert`   | 回滚到上一个版本             |
| `merge`    | 代码合并                     |
| `sync`     | 同步主线或分支的变动         |
| `typo`     | 更改一些拼写错误             |

:::

:::::{dropdown} 修改 Git Commit 历史

参考 [git-filter-repo(1) (htmlpreview.github.io)](https://htmlpreview.github.io/?https://github.com/newren/git-filter-repo/blob/docs/html/git-filter-repo.html)

**(1) 环境部署**

1. 下载仓库：<https://github.com/newren/git-filter-repo.git>
2. 将仓库根目录添加到系统环境变量。

**(2) 修改历史提交记录**

::::{tab-set}

:::{tab-item} 修改用户名和邮箱

如果你修改了邮箱，你在 Windows 上设置的提交邮箱与 GitHub 上设置的邮箱不一致，历史提交信息中的头像可能会空白。这种情况下下，可以使用下面的方法解决。

创建 `mailmap.txt`，格式如下所示（注：`username` 允许存在空格，尖括号不用去掉）：

```bash
cat <<EOF | tee ../mailmap.txt
User Name <email@addre.ss>                                   # 本次提交的用户名和邮箱
<new@email.com> <old1@email.com>                             # 只修改邮箱
New User Name <new@email.com> <old2@email.com>               # 同时修改用户名和邮箱
New User Name <new@email.com> Old User Name <old3@email.com> # 同时修改用户名和邮箱
EOF
```

一个简单的示例如下所示：

```bash
cat <<EOF | tee ../mailmap.txt
<yantao.z@outlook.com> <zh6tao@gmail.com>
zhyantao <yantao.z@outlook.com> 非鱼 <zh6tao@gmail.com>
EOF
```

`cd` 到仓库的根目录，运行下面的命令：

```bash
git filter-repo --mailmap ../mailmap.txt
```

:::

:::{tab-item} 删除敏感信息

在开发过程中，发现将密码或私钥上传到 GitHub 上，思考如何在不删除仓库的情况下，仅修改敏感信息来将密码隐藏掉。首先，创建 `replacements.txt`，添加如下变更内容：

```bash
cat <<EOF | sudo tee ../replacements.txt
PASSWORD1                       # 将所有提交记录中的 'PASSWORD1' 替换为 '***REMOVED***' (默认)
PASSWORD2==>examplePass         # 将所有提交记录中的 'PASSWORD2' 替换为 'examplePass'
PASSWORD3==>                    # 将所有提交记录中的 'PASSWORD3' 替换为空字符串
regex:password=\w+==>password=  # 使用正则表达式将 'password=\w+' 替换为 'password='
regex:\r(\n)==>$1               # 将所有提交记录中的 Windows 中的换行符替换为 Unix 的换行符
EOF
```

`cd` 到仓库的根目录，运行下面的命令：

```bash
git filter-repo --replace-text ../replacement.txt
```

:::

::::

**(3) 提交到远程仓库**

`git filter-repo` 工具将自动删除你配置的远程库。使用 `git remote set-url` 命令还原远程库：

```bash
git remote add origin git@github.com:username/repository.git
```

需要强制推送才能将修改提交到远程仓库：

```bash
git push origin --force --all
```

:::{dropdown} ! [remote rejected] main -> main (protected branch hook declined)

```bash
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote: error: Cannot force-push to this branch
To github.com:zhyantao/cc-frontend-preview.git
! [remote rejected] main -> main (protected branch hook declined)
```

解决方法：`Settings` > `General` > `Danger Zone` > `Disable branch protection rules`

:::

要从标记版本删除敏感文件，还需要针对 Git 标记强制推送：

```bash
git push origin --force --tags
```

:::::

```{figure} ../_static/images/commit-main.*

```

```{figure} ../_static/images/commit-stable.*

```

```{figure} ../_static/images/commit-amend.*

```

```{figure} ../_static/images/commit-detached.*

```

## 检查与切换分支 branch

```bash
# 列出所有本地分支
git branch

# 列出所有远程分支
git branch -r

# 列出所有本地分支和远程分支
git branch -a

# 新建一个分支，但依然停留在当前分支
git branch <branch>

# 新建一个分支，并切换到该分支
git checkout -b <branch>

# 新建一个分支，指向指定 commit
git branch <branch> <commit>

# 新建一个分支，与指定的远程分支建立追踪关系
git branch --track <local-branch> <remote-branch>

# 建立追踪关系，在现有分支与指定的远程分支之间
git branch --set-upstream <local-branch> <remote-branch>

# 重命名分支
git branch -m <old-name> <new-name>

# 删除分支
git branch -d <branch>

# 删除远程分支
git push origin --delete <branch>
git branch -dr <remote/branch>
```

:::{dropdown} 分支命名规范

| 分支             | 命名               | 说明                             |
| ---------------- | ------------------ | -------------------------------- |
| 主分支           | `master`           | 主分支是提供给用户使用的正式版本 |
| 开发分支         | `dev`              | 开发分支永远是功能最新最全的分支 |
| 功能分支         | `feature-*`        | 新功能分支开发完成后需删除       |
| 发布版本         | `release-*`        | 发布定期要上线的功能             |
| 发布版本修复分支 | `bugfix-release-*` | 修复测试 BUG                     |
| 紧急修复分支     | `bugfix-master-*`  | 紧急修复线上代码的 BUG           |

:::

:::{dropdown} 冲突处理

有时想把 `<other-branch>` 的内容合并到当前所在分支，使用命令
`git fetch <remote> <other-branch>` 和 `git merge FETCH_HEAD`
后，发现 **有冲突**。冲突的文件会有类似如下所示的结果：

```python
<<<<<<< HEAD (冲突开始的位置)
最新的修改
=======
上一次提交的修改
>>>>>>> 上一个分支的名称 (冲突结束的位置)
```

因此，我们的目标就是对冲突开始和结束之间的部分进行删减。
解决完冲突后，继续使用命令 `git add` 和 `git commit` 命令即可完成后续开发工作。

**error: The following untracked working tree files would be overwritten by checkout**

```bash
git clean -fd
```

:::

## 标记重要提交 tag

```bash
# 列出所有 tag
git tag

# 新建一个 tag 在当前 commit
git tag <tag>

# 新建一个 tag 在指定 commit
git tag <tag> <commit>

# 删除本地 tag
git tag -d <tag>

# 删除远程 tag
git push origin :refs/tags/<tag-name>

# 查看 tag 信息
git show <tag>

# 提交指定 tag
git push <remote> <tag>

# 提交所有 tag
git push <remote> --tags

# 新建一个分支，指向某个 tag
git checkout -b <branch> <tag>

# 生成一个可供发布的压缩包
git archive
```

:::{dropdown} 标签命名规范
标签命名遵循 `主版本号.次版本号.修订号` 的规则，例如 `v1.2.3` 是版本 1.2 的第 4 次修订。以下是版本号的升级规则：

- 优化已经存在的功能，或者修复 BUG：修订号 + 1；
- 新增功能：次版本号 + 1；
- 架构变化，接口变更：主版本号 + 1。

:::

## 审查提交历史 log

```bash
# 显示当前分支的版本历史
git log

# 显示 commit 历史，以及每次 commit 发生变更的文件
git log --stat

# 搜索提交历史，根据关键词
git log -S <keyword>

# 显示某个 commit 之后的所有变动，每个 commit 占据一行
git log <tag> HEAD --pretty=format:%s

# 显示某个 commit 之后的所有变动，其"提交说明"必须符合搜索条件
git log <tag> HEAD --grep feature

# 显示某个文件的版本历史，包括文件改名
git log --follow <filename>
git whatchanged <filename>

# 显示指定文件相关的每一次 diff
git log -p <filename>

# 显示过去 5 次提交
git log -5 --pretty --oneline

# 显示所有提交过的用户，按提交次数排序
git shortlog -sn

# 显示指定文件是什么人在什么时间修改过
git blame <filename>

# 显示某次提交的元数据和内容变化
git show <commit>

# 显示某次提交发生变化的文件
git show --name-only <commit>

# 显示某次提交时，某个文件的内容
git show <commit>:<filename>

# 显示当前分支的最近几次提交
git reflog
```

## 恢复文件与撤销更改 checkout

```bash
# 切换到指定分支，并更新工作区
git checkout <branch>

# 切换到上一个分支
git checkout -

# 恢复暂存区的指定文件到工作区
git checkout <filename>

# 恢复某个 commit 的指定文件到暂存区和工作区
git checkout <commit> <filename>

# 恢复暂存区的所有文件到工作区
git checkout .

# 暂时将未提交的变化移除，稍后再移入
git stash
git stash pop
```

```{figure} ../_static/images/checkout-files.*

```

```{figure} ../_static/images/checkout-branch.*

```

```{figure} ../_static/images/checkout-detached.*

```

```{figure} ../_static/images/checkout-after-detached.*

```

```{figure} ../_static/images/checkout-b-detached.*

```

## 撤销提交和未提交的更改 reset

```bash
# 重置暂存区的指定文件，与上一次 commit 保持一致，但工作区不变
git reset -- <filename>

# 重置暂存区与工作区，与上一次 commit 保持一致
git reset --hard

# 重置当前分支的指针为指定 commit，同时重置暂存区，但工作区不变
git reset <commit>

# 重置当前分支的 HEAD 为指定 commit，同时重置暂存区和工作区，与指定 commit 一致
git reset --hard <commit>

# 重置当前 HEAD 为指定 commit，但保持暂存区和工作区不变
git reset --keep <commit>
```

```{figure} ../_static/images/reset-commit.*

```

```{figure} ../_static/images/reset.*

```

```{figure} ../_static/images/reset-files.*

```

## 撤销特定的历史更改 revert

```bash
# 撤销对指定文件在最近一次提交中的修改，但保留文件的修改内容
git revert filename

# 新建一个提交，用来撤销对当前分支指定提交的修改，但保留该提交的内容
git revert <commit>

# 新建一个提交，用来撤销对当前分支指定合并提交的修改，并改写提交信息
git revert -m <n> <merge-commit>
```

## 应用提交到当前分支 cherry-pick

```bash
# 将其他分支上的某个提交应用到当前分支
git cherry-pick <commit>

# 将一系列连续的提交应用到当前分支
git cherry-pick <first-commit>^..<last-commit>

# 解决冲突时选择性的应用父提交：<n> 是指在三路合并中使用的父提交编号（1 或 2）
git cherry-pick -m <n> <commit>
```

```{figure} ../_static/images/cherry-pick.*

```

## 合并分支 merge

```bash
# 合并指定 commit 到当前分支
git merge <commit>

# 合并指定分支到当前分支
git merge <branch>

# 合并指定分支到当前分支，并提交合并记录
git merge --no-ff <branch>

# 合并指定分支到当前分支，并提交合并记录，同时改写提交信息
git merge--no-ff <branch> -m <message>
```

```{figure} ../_static/images/merge-ff.*

```

```{figure} ../_static/images/merge.*

```

## 更新分支历史 rebase

```bash
# 将当前分支的提交历史，重新应用到另一个分支
git rebase <branch>

# 将当前分支的提交历史，重新应用到另一个分支，但保留提交信息
git rebase -i <branch>

# 将当前分支的提交历史，重新应用到另一个分支，但保留提交信息
git rebase -i HEAD~<n>
```

```{figure} ../_static/images/rebase.*

```

```{figure} ../_static/images/rebase-onto.*

```

## 管理子库 submodule

```bash
# 添加 submodule 到现有项目
git submodule add <remote> <submodule-path>

# 从当前项目移除 submodule
git submodule deinit -f <submodule-path>
rm -rf .git/modules/<submodule-path>
git rm -f <submodule-path>

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
git submodule update --remote <submodule-path>

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
```

## 忽略规则 gitignore

:::{dropdown} 匹配规则

- `gitignore` 只匹配其所在目录及子目录的文件。
- 已经被 `git track` 的文件不受 `gitignore` 影响。
- 子目录的 `gitignore` 文件规则会覆盖父目录的规则。

:::

```bash
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
```

## 在 shell 中显示 git 分支

::::{tab-set}

:::{tab-item} Linux
:sync: Linux

方法一：使用 <https://github.com/romkatv/gitstatus> 提供的服务：

```bash
git clone --depth=1 https://github.com/romkatv/gitstatus.git ~/gitstatus
echo 'source ~/gitstatus/gitstatus.prompt.sh' >> ~/.bashrc
```

方法二：打开 `~/.bashrc` 做如下修改：

```bash
# display git branch on bash
git_branch() {
branch="`git branch 2>/dev/null | grep "^\*" | sed -e "s/^\*\ //"`"
if [ "${branch}" != "" ];then
    if [ "${branch}" = "(no branch)" ];then
        branch="(`git rev-parse --short HEAD`...)"
    fi
    echo -e ":\033[01;32m$branch\033[00m"
fi
}

PS1 = '$(git_branch)' # 补充到 PS1 变量上
```

:::

:::{tab-item} Windows
:sync: Windows

Post Git 提供了显示 Git 分支的功能，安装 Posh Git，请执行以下步骤：

1. 以管理员身份启动 PowerShell。
2. 修改执行策略以允许脚本运行：

   ```bash
   Set-ExecutionPolicy RemoteSigned
   ```

3. 安装 Posh Git 模块，指定范围为当前用户并强制安装：

   ```bash
   Install-Module posh-git -Scope CurrentUser -Force
   ```

4. 导入 Posh Git 模块以便使用：

   ```bash
   Import-Module posh-git
   ```

5. 将 Posh Git 添加到 PowerShell 配置文件中，以便对所有会话有效：

   ```bash
   Add-PoshGitToProfile -AllHosts
   ```

卸载 Posh Git，请执行以下步骤：

1.  以管理员身份运行 PowerShell。
2.  删除 Posh Git 模块：

    ```bash
    Uninstall-Module posh-git
    ```

3.  编辑 PowerShell 配置文件以移除 Posh Git 模块的导入命令。打开配置文件：

    ```bash
    notepad $PROFILE
    ```

    然后，删除文件中包含 `Import-Module posh-git` 的行。

:::

::::

## 自动补全

::::{tab-set}

:::{tab-item} Linux
:sync: Linux

```bash
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
```

:::

:::{tab-item} Windows
:sync: Windows

Post Git 提供了自动补全的功能，安装 Posh Git，请执行以下步骤：

1. 以管理员身份启动 PowerShell。
2. 修改执行策略以允许脚本运行：

   ```bash
   Set-ExecutionPolicy RemoteSigned
   ```

3. 安装 Posh Git 模块，指定范围为当前用户并强制安装：

   ```bash
   Install-Module posh-git -Scope CurrentUser -Force
   ```

4. 导入 Posh Git 模块以便使用：

   ```bash
   Import-Module posh-git
   ```

5. 将 Posh Git 添加到 PowerShell 配置文件中，以便对所有会话有效：

   ```bash
   Add-PoshGitToProfile -AllHosts
   ```

卸载 Posh Git，请执行以下步骤：

1.  以管理员身份运行 PowerShell。
2.  删除 Posh Git 模块：

    ```bash
    Uninstall-Module posh-git
    ```

3.  编辑 PowerShell 配置文件以移除 Posh Git 模块的导入命令。打开配置文件：

    ```bash
    notepad $PROFILE
    ```

    然后，删除文件中包含 `Import-Module posh-git` 的行。

:::

::::

(git-syntax)=

# Git

## 配置仓库

:::{dropdown} 配置用户名和邮箱

```bash
git config --global user.name "zhyantao"
git config --global user.email "yantao.z@outlook.com"
```

:::

:::{dropdown} VSCode 未修改代码，但显示变更

```bash
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

:::

:::{dropdown} GitHub 不显示头像
如果你在 Github 上修改了提交邮箱，而没有修改本地提交邮箱的话，会发现你的头像在提交记录上无法显示。因此，本地的提交邮箱应当与远程仓库保持一致。修改 `~/.gitconfig` 可解决问题。
:::

## 典型工作流程

- 工作目录 (Working Directory)：你正在编辑的文件。
- 暂存区 (Staging Area / Index)：通过 `git add` 添加的文件，准备下次提交。
- 版本库 (Repository / HEAD)：通过 `git commit` 提交后的历史记录。

```{uml}
@startuml
start

:git pull;
note right:同步远程更改

repeat
  :编辑文件;
  repeat
  repeat
    :git add <file>...;
    note right:添加到暂存区
    backward:git restore --staged <file>...;
  repeat while (撤销暂存?) is (Yes) not (No)

  repeat
    :git commit;
    note right:创建新提交
    backward:git reset --soft HEAD~1;
  repeat while (撤销提交(保留暂存)?) is (Yes) not (No)

  backward:git reset --mixed HEAD~1;
  repeat while (撤销提交和暂存?) is (Yes) not (No)

  backward:git reset --hard HEAD~1;
repeat while (彻底丢弃更改?) is (Yes) not (No)

repeat
  :git push [--force] <remote> <branch>;
  note right:推送到远程
  backward:git revert HEAD;
repeat while (安全撤销提交?) is (Yes) not (No)

stop
@enduml
```

```bash
# 列出所有已配置的远程仓库及其对应的 URL
git remote -v

# 显示所有远程跟踪分支
git branch -r

# 更新指定远程仓库的 URL 地址
git remote set-url <remote> <url>

# 显示工作目录和暂存区的状态 (变更文件列表)
git status

# 显示工作目录与暂存区之间的差异
git diff

# 显示两次特定提交之间的差异对比
git diff HEAD~1 HEAD~2

# 修改最近一次提交的提交信息 (不会创建新的提交)
git commit --amend -m "<message>"

# 基于当前提交创建新分支
git branch <branch>

# 重命名本地分支
git branch -m <old-name> <new-name>

# 安全删除已合并的本地分支
git branch -d <branch>

# 删除远程分支
git push origin --delete <branch>

# 显示当前分支的提交历史 (按时间倒序)
git log

# 逐行显示文件的修改历史 (作者、时间、提交信息)
git blame <filename>

# 将指定提交的更改应用到当前分支
git cherry-pick <commit>

# 将连续多个提交应用到当前分支 (包含首尾提交)
git cherry-pick <first-commit>^..<last-commit>

# 将指定提交合并到当前分支
git merge <commit>

# 将指定分支的所有更改合并到当前分支
git merge <branch>

# 将当前分支的提交在目标分支上重新应用 (变基操作)
git rebase <branch>

# 在当前提交上创建一个新标签
git tag <tag>

# 删除本地标签
git tag -d <tag>

# 将标签推送到远程仓库
git push <remote> <tag>
```

## submodule

:::{dropdown} 管理子库

```bash
# 添加 submodule 到现有项目
git submodule add https://github.com/username/subrepo.git path/to/subrepo

# 从当前项目移除 submodule
cat .gitmodules | grep path
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

:::

## 代码提交规范

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

## 分支命名规范

| 分支             | 命名               | 说明                             |
| ---------------- | ------------------ | -------------------------------- |
| 主分支           | `master`           | 主分支是提供给用户使用的正式版本 |
| 开发分支         | `dev`              | 开发分支永远是功能最新最全的分支 |
| 功能分支         | `feature-*`        | 新功能分支开发完成后需删除       |
| 发布版本         | `release-*`        | 发布定期要上线的功能             |
| 发布版本修复分支 | `bugfix-release-*` | 修复测试 BUG                     |
| 紧急修复分支     | `bugfix-master-*`  | 紧急修复线上代码的 BUG           |

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

## 标签命名规范

标签命名遵循 `主版本号.次版本号.修订号` 的规则，例如 `v1.2.3` 是版本 1.2 的第 4 次修订。以下是版本号的升级规则：

- 优化已经存在的功能，或者修复 BUG：修订号 +1；
- 新增功能：次版本号 +1；
- 架构变化，接口变更：主版本号 +1。

## gitignore

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

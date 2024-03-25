# 修改 Git Commit 历史

参考文档：[git-filter-repo(1) (htmlpreview.github.io)](https://htmlpreview.github.io/?https://github.com/newren/git-filter-repo/blob/docs/html/git-filter-repo.html)

## 前提：环境部署

1. 下载仓库：<https://github.com/newren/git-filter-repo.git>
2. 将仓库根目录添加到系统环境变量。

## 修改历史提交记录

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
zhyantao <zh6tao@gmail.com>
<zh6tao@gmail.com> <zhyantao@126.com>
<zh6tao@gmail.com> <yanntao@yeah.net>
<zh6tao@gmail.com> <yann.tao@qq.com>
<zh6tao@gmail.com> <yantao.z@qq.com>
zhyantao <zh6tao@gmail.com> toooney <toooney@126.com>
zhyantao <zh6tao@gmail.com> Zh YT <zhyantao@126.com>
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

## 提交到远程仓库

`git filter-repo` 工具将自动删除你配置的远程库。使用 `git remote set-url` 命令还原远程库：

```bash
git remote add origin git@github.com:username/repository.git
```

需要强制推送才能将修改提交到远程仓库：

```bash
git push origin --force --all
```

````{dropdown} ! [remote rejected] main -> main (protected branch hook declined)
```bash
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote: error: Cannot force-push to this branch
To github.com:zhyantao/cc-frontend-preview.git
 ! [remote rejected] main -> main (protected branch hook declined)
```

解决方法：`Settings` > `General` > `Danger Zone` > `Disable branch protection rules`
````

要从标记版本删除敏感文件，还需要针对 Git 标记强制推送：

```bash
git push origin --force --tags
```

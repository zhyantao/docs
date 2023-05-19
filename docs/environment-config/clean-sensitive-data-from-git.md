# 删除 GitHub 中的敏感信息

在开发过程中，发现将密码或私钥上传到 GitHub 上，思考如何在不删除仓库的情况下，仅修改敏感信息来将密码隐藏掉。

第 1 步：下载仓库，假设下载后的仓库路径为 `D:/Workshop/real-time-faas`。

第 2 步：编辑敏感信息（修改或删除），然后提交到 GitHub：

```{code-block} bash
git add .
git commit -m "clean sensitive data from git commit"
git push origin master
```

第 3 步：下载 [bfg-1.14.0.jar](https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar)。

第 4 步：新建 `replacements.txt`，根据下面的格式添加内容：

```{code-block} bash
PASSWORD1                       # 将所有提交记录中的字符串 'PASSWORD1' 替换为 '***REMOVED***' (默认)
PASSWORD2==>examplePass         # 将所有提交记录中的字符串 'PASSWORD2' 替换为 'examplePass'
PASSWORD3==>                    # 将所有提交记录中的字符串 'PASSWORD3' 替换为空字符串
regex:password=\w+==>password=  # 使用正则表达式将 'password=\w+' 替换为 'password='
regex:\r(\n)==>$1               # 将所有提交记录中的 Windows 中的换行符替换为 Unix 的换行符
```

第 4 步：利用 `jar` 文件，修改（或抹去）所有的提交记录：

```{code-block} bash
java -jar bfg-1.14.0.jar --replace-text replacements.txt D:/Workshop/real-time-faas
```

第 5 步：将修改后的结果提交到远程仓库 `git push --force`。

# macOS 环境设置

## 批量修改文件默认打开方式（duti）

在 macOS 上，`duti` 是一款通过命令行批量、精准设置文件默认打开方式的工具，配合 Homebrew 即可快速安装，非常适合开发环境统一配置。

### 安装 duti

```bash
# 安装 duti（依赖 Homebrew）
brew install duti
```

### 常用基础命令

```bash
# 查看某类文件当前的默认打开程序（以 .md 为例）
duti -x .md

# 设置文件默认打开方式
# 格式：duti -s 软件BundleID 后缀名 all
duti -s com.microsoft.VSCode .md all
```

下面是**前端、后端、运维、脚本、配置、文档**等最常用源码/配置文件后缀，统一设置为 VS Code 打开：

```bash
# 文本与标记语言
duti -s com.microsoft.VSCode .md all
duti -s com.microsoft.VSCode .txt all
duti -s com.microsoft.VSCode .rtf all

# Web 前端
duti -s com.microsoft.VSCode .css all
duti -s com.microsoft.VSCode .scss all
duti -s com.microsoft.VSCode .sass all
duti -s com.microsoft.VSCode .less all
duti -s com.microsoft.VSCode .js all
duti -s com.microsoft.VSCode .jsx all
duti -s com.microsoft.VSCode .ts all
duti -s com.microsoft.VSCode .tsx all
duti -s com.microsoft.VSCode .vue all
duti -s com.microsoft.VSCode .json all
duti -s com.microsoft.VSCode .xml all

# 后端语言
duti -s com.microsoft.VSCode .py all
duti -s com.microsoft.VSCode .java all
duti -s com.microsoft.VSCode .c all
duti -s com.microsoft.VSCode .cpp all
duti -s com.microsoft.VSCode .h all
duti -s com.microsoft.VSCode .go all
duti -s com.microsoft.VSCode .rs all
duti -s com.microsoft.VSCode .php all
duti -s com.microsoft.VSCode .rb all
duti -s com.microsoft.VSCode .swift all
duti -s com.microsoft.VSCode .kt all
duti -s com.microsoft.VSCode .dart all

# Shell 与运维
duti -s com.microsoft.VSCode .sh all
duti -s com.microsoft.VSCode .zsh all
duti -s com.microsoft.VSCode .bash all
duti -s com.microsoft.VSCode .fish all
duti -s com.microsoft.VSCode .env all
duti -s com.microsoft.VSCode .yml all
duti -s com.microsoft.VSCode .yaml all
duti -s com.microsoft.VSCode .ini all
duti -s com.microsoft.VSCode .conf all
duti -s com.microsoft.VSCode .gitignore all
duti -s com.microsoft.VSCode .dockerignore all
duti -s com.microsoft.VSCode .Makefile all

# 数据与配置
duti -s com.microsoft.VSCode .csv all
duti -s com.microsoft.VSCode .log all
duti -s com.microsoft.VSCode .sql all
```

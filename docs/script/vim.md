# Vim

## 移动

| 键位    | 功能        |
| ----- | --------- |
| `h`   | 左         |
| `j`   | 下         |
| `k`   | 上         |
| `l`   | 右         |
| `gg`  | 光标移动到文件开头 |
| `G`   | 光标移动到文件末尾 |
| `0`   | 光标移动到行首   |
| `$`   | 光标移动到行尾   |
| `23G` | 光标跳转到第 23 行 |
| `:23` | 跳转到第 23 行 |

## 插入

| 键位  | 功能                |
| --- | ----------------- |
| `i` | 在光标前插入一个字符        |
| `I` | 在行首插入一个字符         |
| `a` | 在光标后插入一个字符        |
| `A` | 在行尾插入一个字符         |
| `o` | 向下新开辟一行，插入行首      |
| `O` | 向上新开辟一行，插入行首      |
| `s` | 删除光标所在的字符，并进入插入状态 |
| `S` | 删除光标所在的行，并进入插入状态  |

## 复制、粘贴

| 键位           | 功能           |
| ------------ | ------------ |
| `yy`         | 复制当前行        |
| `10yy`       | 复制 10 行      |
| `p`          | 在光标所在位置下一行粘贴 |
| `P`          | 在光标所在位置上一行粘贴 |
| `:set paste` | 防止粘贴时格式错乱    |

## 剪切、删除

| 键位     | 功能                        |
| ------ | ------------------------- |
| `x`    | 删除光标后一个字符                 |
| `X`    | 删除光标前一个字符                 |
| `dw`   | 删除光标开始位置的单词               |
| `d0`   | 删除光标前本行文本的所有内容，不包含光标所在的字符 |
| `D`    | 删除光标后本行所有的内容，包含光标所在的字符    |
| `dd`   | 删除光标所在的行                  |
| `n dd` | 删除光标后面所有的行，包含光标所在的行       |

## 撤销

| 键位         | 功能         |
| ---------- | ---------- |
| `u`        | 一步撤销，可多次使用 |
| `Ctrl + r` | 反撤销        |

## 查找

| 键位         | 功能           |
| ---------- | ------------ |
| `/PATTERN` | 从光标所在位置向下查找  |
| `?PATTERN` | 从光标所在位置向上查找  |
| `Enter`    | 完成输入模式       |
| `n`        | 向下查找下一个      |
| `N`        | 向上查找下一个      |
| `#`        | 查找光标当前指向的字符串 |

## 替换

| 命令                         | 功能                                |
| -------------------------- | --------------------------------- |
| `r`                        | 替换当前字符                            |
| `:s/PATTERN/toString`      | 将当前行第一次出现的 `PATTERN` 替换为 `toString`   |
| `:s/PATTERN/toString/g`    | 将当前行所有 `PATTERN` 替换为 `toString`       |
| `:%s/PATTERN/toString`     | 将所有行第一次出现的 `PATTERN` 替换为 `toString`   |
| `:%s/PATTERN/toString/g`   | 将所有行所有 `PATTERN` 替换为 `toString`       |
| `:2,3s/PATTERN/toString`   | 将第 2 至 3 行第一次出现的 `PATTERN` 替换为 `toString` |
| `:2,3s/PATTERN/toString/g` | 将第 2 至 3 行所有 `PATTERN` 替换为 `toString`     |

## 格式化文本

| 键位     | 功能            |
| ------ | ------------- |
| `>>`   | 文本右移一个 Tab 大小   |
| `<<`   | 文本左移一个 Tab 大小   |
| `gg=G` | 整理代码，使其符合标准格式 |

## 全选

| 键位     | 功能   |
| ------ | ---- |
| `ggVG` | 全部选择 |

## 窗口

| 键位         | 功能   |
| ---------- | ---- |
| `Ctrl + S` | 冻结窗口 |
| `Ctrl + q` | 解冻窗口 |

## 记住上次打开的位置

```vim
" 若要在重新打开文件时跳转到最后位置，请取消以下注释
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif
```

## 配置 Vim 插件

对于 Linux，默认安装的 Vim 版本如果是 7.x，而要使用 YouCompleteMe，则需要升级到 8.x。

### 使用 Vundle 管理插件

**安装 Vundle**

```bash
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
```

**配置 Vundle**

在 `~/.vimrc` 文件中添加配置：

```vim
" General settings
set nu                  " 显示行号
set tabstop=4           " 设置 Tab 字符宽度
set softtabstop=4       " 设置缩进宽度
set shiftwidth=4        " 设置自动缩进宽度
"set expandtab          " 使用空格代替 Tab

set nocompatible        " 开启 Vim 增强模式
filetype off            " 关闭文件类型检测

" 设置运行路径以包含Vundle并初始化
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" Vundle管理自身
Plugin 'VundleVim/Vundle.vim'

" 添加其他插件示例
Plugin 'vim-scripts/Auto-Pairs'             " 自动完成括号/引号/方括号

call vundle#end()            " 结束 Vundle 配置
filetype plugin indent on    " 开启文件类型检测、插件和缩进

" 插件管理快捷方式
" :PluginList       - 列出已配置插件
" :PluginInstall    - 安装插件；加 ! 更新，或直接 :PluginUpdate
" :PluginSearch foo - 搜索 foo 插件；加 ! 刷新本地缓存
" :PluginClean      - 确认删除未使用的插件；加 ! 自动批准删除
" 更多详情见 :h vundle 或访问 wiki 查询 FAQ
```

打开 Vim，执行 `:PluginInstall` 安装插件。

**删除插件**

- 从 `.vimrc` 中移除不需要的插件条目。
- 运行 `:PluginUpdate!` 更新插件列表。
- 最后，运行 `:PluginClean!` 清理不再配置的插件。

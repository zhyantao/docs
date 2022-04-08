# 常用的 VIM 插件及配置

Linux 默认安装的 VIM 版本是 7.x，如果要使用 YouCompelteMe，需要先升级到 8.x。

为了更方便地管理我们的 VIM 插件，推荐使用 Vundle。具体步骤如下：

```{code-block} bash
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
```

新建或打开 `~/.vimrc`，然后再文件中添加如下内容：

```{code-block} text
" General settings
set nu                  " show line numbers
set tabstop     =4      " Width of tab character
set softtabstop =4      " Fine tunes the amount of white space to be added
set shiftwidth  =4      " Determines the amount of whitespace to add in normal mode
"set expandtab          " When this option is enabled, vi will use spaces instead of tabs

set nocompatible        " be iMproved, required
filetype off            " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
Plugin 'vim-scripts/Auto-Pairs'             " Autocomplete parens/quotes/brackets

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line
```

如果要删除某些不需要的插件，可以参考上面配置文件中的 Brief help 部分。首先编辑 `.vimrc`
将不需要的 Plugin 删掉，先运行 `:PluginUpdate!` 然后再运行 `:PluginClean!` 即可。

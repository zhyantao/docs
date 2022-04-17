# Bash

## 快捷键

```{code-block} bash
Ctrl + s        # 冻结窗口，用 Ctrl + q，Ctrl + C 退出

Ctrl + l        # 清屏

Ctrl + c        # 终止程序运行

echo            # 输出到屏幕
    $PATH       # 环境环境变量
    $?          # 上次命令是否运行成功，成功为 0，其他失败

df              # 查看内存和交换分区的使用情况
    [-m|-g|-k]  # 显示的单位可以是 M、G、K

shutdown        # 关机
reboot          # 重启
halt            # 关机后关闭电源
```

## 显示 git 分支

```{code-block} bash
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

PS1 = '\[\033[01;32m\]$(git_branch)\[\033[00m\]'
```

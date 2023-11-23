# Shell

- Bash 4.0 参考文档（[PDF](https://kdocs.cn/l/cf0I6g1Luc87)） | Bash Reference Manual（[LINK](https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html)）
- 遇到了不会用的命令？可以在 tldr 上搜索：<https://tldr.inbrowser.app/pages/common/tar>
- 更多实用的技巧，可以参考：<https://missing-semester-cn.github.io/2020/shell-tools/>

## 1. Hello World

### 1.1. 基本结构

创建 `helloWorld.sh` 文件，写入如下内容：

```bash
#!/bin/bash

echo "hello world"
```

其中 `#!` 告诉系统其后路径所指定的程序是解释此脚本文件的 Shell 程序，常见的 Shell 程序有以下几类（可通过命令 `cat /etc/shells` 查看）：

- Bourne Shell（/usr/bin/sh或/bin/sh）
- Bourne Again Shell（/bin/bash）
- C Shell（/usr/bin/csh）
- K Shell（/usr/bin/ksh）
- Shell for Root（/sbin/sh）
- ……

其中 **Bash** 在日常工作中被广泛使用，同时也是大多数 Linux 系统默认的 Shell。

执行该 sh 脚本

```bash
# 增加可执行权限
➜  chmod u+x helloWorld.sh

# 运行脚本
➜  ./helloWorld.sh
或
➜  sh hellowWorld.sh
```

### 1.2. 注释

单行注释

- 以 `#` 开头的行是注释

多行注释

- 方式一：用一对 `{}` 括起来，定义成一个函数，没有地方调用即达到注释的效果。

- 方式二：

  ```bash
  :<<EOF
  注释内容...
  注释内容...
  注释内容...
  EOF
  ```

## 2. 基本语法

### 2.1. 变量

- 变量定义

  - 变量名建议大写；
  - 有效字符仅能包含字母、数字、下划线，首个字符不能以数字开头；
  - `=` 两边不能有空格；
  - 不能使用标点符号；
  - 不能使用 bash 里的关键字（可用 `help` 命令查看保留关键字）。

  ```bash
  # 示例
  VAR1="whoru"
  VAR2=100
  var3=/data/www
  var4_name="root"
  ```

- 访问变量 `$VAR1` 或 `$(var1)`，其中，加花括号是为了帮助解释器识别变量的边界。

- 设置变量只读 `readonly VAR1`

- 删除变量（**不适用于只读变量！**） `unset VAR1`

- 局部、全局变量

  - 不做特殊声明，Shell 中所有变量都是**全局变量**。
  - 可以使用关键字 `local` 定义局部变量。
  - *如果函数内部和外部存在同名变量，则内部会覆盖外部*。

### 2.2. 字符串

- 值用双引号 `""` 或单引号 `''` 表示

  - 单引号单限制：
    - 单引号里的任何字符都会原样输出；
    - 单引号字符串中的变量是无效的；
  - 双引号的优点：
    - 双引号里可以有变量；
    - 双引号里可以出现转义字符；

- 其它

  ```bash
  # 字符串拼接
  name="xiaoming"
  var2="hello, "$name # 输出 hello, xiaoming
  
  # 获取字符串长度
  string="abcd"
  echo ${#string} # 输出 4
  echo `expr length "$string"` # 输出 4
  
  # 提取子字符串
  msg="zhangsan is a good man"
  echo ${msg:1:4} # 输出 hang
  echo ${msg: -3} # 输出 man
  ```

### 2.3. 数组

- bash 支持一维数组（**不支持多维数组**），并且没有限定数组的大小。

- 数组元素的下标由 0 开始，获取数组元素要用到下标。

- 定义：

  ```bash
  array1=(value0 value1 value2 value3)
  
  # 或
  
  array2[0]=value0
  array2[1]=value1
  array2[2]=value2
  ```

- 读取

  ```bash
  # 获取第 1 个元素
  ➜  echo ${array2};  // 输出 value0
  ➜  echo ${array2-};
  ➜  echo ${array2?}
  
  # 获取指定下标的元素
  ➜  echo ${array2[2]}; // 输出 value2
  
  # 获取数组所有元素
  ➜  echo ${array2[*]}; // 输出 value0 value1 value2
  ➜  echo ${array2[@]}
  ```

- 获取数组元素个数

  ```bash
  ➜  echo ${#array2[@]}; // 输出 3
  ➜  echo ${#array2[*]};
  ```

- 取得数组中指定下标元素的字符长度

  ```bash
  ➜  echo ${#array2[2]};
  ```

### 2.4. 传递参数

在执行 Shell 脚本时，可以向脚本传递参数，脚本内获取参数的格式为 `$n`。其中，`n` 指传递给脚本的第 `n` 个参数。

如下脚本文件 `demo.sh`：

```bash
#!/bin/bash

echo "执行的文件名：$0";
echo "第一个参数为：$1";
echo "第二个参数为：$2";
echo "第三个参数为：$3";
```

执行该文件，并传递参数，如下：

```bash
➜  ./demo3.sh param1 param2 param3
执行的文件名：./demo3.sh
第一个参数为：param1
第二个参数为：param2
第三个参数为：param3
```

其中，`$0` 是一个特殊变量，代表当前脚本文件名，还有几个类似的变量如下：

| 变量 | 说明                                                                       |
| ---- | -------------------------------------------------------------------------- |
| `$#` | 传递给脚本的参数个数                                                       |
| `$*` | 以字符串的形式，显示所有向脚本传递的参数，如 `"$1 $2 ... $n"`                  |
| `$@` | 与 `$*` 类似，但是使用引号把每个参数包裹起来，用于遍历，如 `"$1" "$2" ... "$n"` |
| `$?` | 最后一个执行的命令的退出状态：0 表示正常；1 或其它任何值表示有错误               |
| `$$` | 脚本运行的当前进程 `ID` 号                                                   |
| `$!` | 最后一个后台命令的进程号                                                     |

## 3. 运算符

### 3.1. 算数运算符

> 原生 bash 不支持数学运算，但是可以通过其他命令来实现，例如 `awk` 和 `expr`，其中 `expr` 最常用。

假定有两个变量：`a=10` `b=20`

| 运算符 | 说明                       | 举例                           |
| ------ | -------------------------- | ------------------------------ |
| `+`    | 加法                       | ``expr $a + $b`` 结果为 30   |
| `-`    | 减法                       | ``expr $a - $b`` 结果为 -10  |
| `*`    | 乘法                       | ``expr $a \* $b`` 结果为 200 |
| `/`    | 除法                       | ``expr $b / $a`` 结果为 2    |
| `%`    | 取余                       | ``expr $b % $a`` 结果为 0    |
| `=`    | 赋值                       | `a=$b` 将把变量 b 的值赋给 a |
| `==`   | 用于比较两个数字是否相同   | `[ $a == $b ]` 返回 false    |
| `!=`   | 用于比较两个数字是否不相同 | `[ $a != $b ]` 返回 true     |

**注意**：

- 表达式和运算符之间要有空格，如 `2+2` 是错误的，必须写成 `2 + 2`;
- 完整的表达式要被反引号 ` `` `包裹起来；

### 3.2. 关系运算符

> 关系运算符只支持数字，不支持字符串，除非字符串的值是数字。

假定有两个变量：`a=10` `b=20`

| 运算符 | 说明                           | 举例                         |
| ------ | ------------------------------ | ---------------------------- |
| `-eq`  | 检测两个数是否相等             | `[ $a -eq $b ]` 返回 false |
| `-ne`  | 检测两个数是否不相等           | `[ $a -ne $b ]` 返回 true   |
| `-gt`  | 检测左边的数是否大于右边的     | `[ $a -gt $b ]` 返回 false |
| `-lt`  | 检测左边的数是否小于右边的     | `[ $a -lt $b ]` 返回 true  |
| `-ge`  | 检测左边的数是否大于等于右边的 | `[ $a -ge $b ]` 返回 false |
| `-le`  | 检测左边的数是否小于等于右边的 | `[ $a -le $b ]` 返回 true  |

### 3.3. 布尔操作符

假定有两个变量：`a=10` `b=20`

| 运算符 | 说明                                                | 举例                                       |
| ------ | --------------------------------------------------- | ------------------------------------------ |
| `!`    | 非运算，表达式为 true 则返回 false，否则返回 true  | `[ ! false ]` 返回 true                  |
| `-o`   | 或运算，有一个表达式为 true 则返回 true           | `[ $a -lt 20 -o $b -gt 100 ]` 返回 true  |
| `-a`   | 与运算，两个表达式都为 true 才返回 true           | `[ $a -lt 20 -a $b -gt 100 ]` 返回 false |

### 3.4. 逻辑运算符

假定有两个变量：`a=10` `b=20`

| 运算符 | 说明       | 举例                                         |
| ------ | ---------- | -------------------------------------------- |
| `&&`   | 逻辑的 AND | `[[ $a -lt 100 && $b -gt 100 ]]` 返回 false  |
| `\|\|`   | 逻辑的 OR  | `[[ $a -lt 100 \|\| $b -gt 100 ]]` 返回 true |

### 3.5. 字符串运算符

假定有两个变量：`a="abc"` `b="efg"`

| 运算符 | 说明                            | 举例                       |
| ------ | ------------------------------- | -------------------------- |
| `=`    | 检测两个字符串是否相等          | `[ $a = $b ]` 返回 false |
| `!=`   | 检测两个字符串是否不相等        | `[ $a != $b ]` 返回 true |
| `-z`   | 检测字符串长度是否为 0（空）    | `[ -z $a ]` 返回 false   |
| `-n`   | 检测字符串长度是否不为 0（非空） | `[ -n "$a" ]` 返回 true  |
| str    | 检测字符串是否为不为空          | `[ $a ]` 返回 true       |

### 3.6. 文件测试运算符

| 运算符 | 说明（如果是，则返回 true）                          | 举例           |
| ------ | ---------------------------------------------------- | -------------- |
| `-b`   | 检测文件是否是块设备文件                             | `[ -b $file ]` |
| `-c`   | 检测文件是否是字符设备文件                           | `[ -c $file ]` |
| `-d`   | 检测文件是否是目录                                   | `[ -d $file ]` |
| `-f`   | 检测文件是否是普通文件（既不是目录，也不是设备文件） | `[ -f $file ]` |
| `-g`   | 检测文件是否设置了 SGID 位                           | `[ -g $file ]` |
| `-k`   | 检测文件是否设置了粘着位（Sticky Bit）                 | `[ -k $file ]` |
| `-p`   | 检测文件是否是有名管道                               | `[ -p $file ]` |
| `-u`   | 检测文件是否设置了 SUID 位                           | `[ -u $file ]` |
| `-r`   | 检测文件是否可读                                     | `[ -r $file ]` |
| `-w`   | 检测文件是否可写                                     | `[ -w $file ]` |
| `-x`   | 检测文件是否可执行                                   | `[ -x $file ]` |
| `-s`   | 检测文件是否为非空（文件大小是否大于 0）文件          | `[ -s $file ]` |
| `-e`   | 检测文件（包括目录）是否存在                         | `[ -e $file ]` |

## 4. 流程控制

### 4.1. if 语句

大多使用**关系运算符**检查关系

```bash
# 语法格式
if condition1
then
    command1
    ...
elif condition2
then
    command2
else
    commandN
fi
```

### 4.2. case 语句

```bash
# 语法格式
case 值 in
    模式1)
        command1
        command2
        ...
        commandN
        ;;
    模式2）
        command1
        command2
        ...
        commandN
        ;;
    *)
        commandDefault
        ;;
esac
```

### 4.3. while 语句

用于不断执行一系列命令，也用于从输入文件中读取数据；命令通常为测试条件。其格式为：

```bash
# 语法格式
while condition
do
    command
done
```

### 4.4. until 循环

执行一系列命令直至条件为 `true` 时停止，它与 `while 循环` 在处理方式上刚好相反。

```bash
# 语法格式
until condition
do
    command
done
```

### 4.5. for 循环

```bash
# 语法格式
for var in item1 item2 ... itemN
do
    command1
    command2
    ...
    commandN
done
```

### 4.6. 无限循环

```bash
# 语法1
while :
do
    command
done

# 语法2
while true
do
    command
done

# 语法3
for (( ; ; ))
```

### 4.7. 退出循环

- `break` 跳出整个循环，执行循环体后面的代码，支持 `break n` 退出多层嵌套循环
- `continue` 结束当前循环，同样支持 `continue n` 退出多层

## 5. 输入、输出重定向

### 5.1. 命令列表

| 命令              | 说明                                               |
| ----------------- | -------------------------------------------------- |
| `command > file`  | 将输出结果重定向到 file                          |
| `command < file`  | 将输入重定向到 file                              |
| `command >> file` | 将输出以追加的方式重定向到 file                  |
| `n > file`        | 将文件描述符为 n 的文件重定向到 file             |
| `n >> file`       | 将文件描述符为 n 的文件以追加的方式重定向到 file |
| `n >& m`          | 将输出文件 m 和 n 合并                           |
| `n <& m`          | 将输入文件 m 和 n 合并                           |
| `<< tag`          | 将开始标记 tag 和结束标记 tag 之间的内容作为输入 |

关于文件描述符：

- `0` 通常是标准输入（STDIN），Unix 程序默认从 `stdin` 读取数据。
- `1` 标准输出（STDOUT），Unix 程序默认向 `stdout` 输出数据。
- `2` 标准错误输出（STDERR），Unix 程序会向 `stderr` 流中写入错误信息。

示例：

```bash
# 将 stdout 和 stderr 合并后重定向到 file
➜  command > file 2>&1
```

```bash
# 将 .config 中的内容传给 while，一行一行地打印出来
while read line
do
    echo $line
done < .config
```

### 5.2. /dev/null 文件

这是一个特殊的文件，写入到它的内容都会被丢弃；如果尝试从该文件读取内容，也什么也读不到。我们通常将命令的输出重定向到它，起到“禁止输出”的效果。

如：

```bash
# 屏蔽 stdout 和 stderr
➜  command > /dev/null 2>&1
```

### 5.3. Here 文档

```bash
# 将两个 delimiter 之间的内容(document) 作为输入传递给 command。
command << delimiter
document
delimiter
```

说明：

- 结尾的 `delimiter` 一定要顶格写，前面不能有任何字符，后面也不能有任何字符，包括空格和 tab 缩进。
- 开始的 `delimiter` 前后的空格会被忽略掉。

## 6. 函数

### 6.1. 基本语法

```bash
[ function ] funcName [()] {

    command;

    [return int;]

}
```

说明：

- `function` 关键字非必须；
- 如果该函数不传入变量，这函数名的后面的括号可以不加；
- `return` 函数返回值
  - 非必须，默认返回最后一条命令的执行结果；
  - 它只能返回 1 ～ 255 之间的整数，通常只是用来供其它地方获取状态，比如 0 成功，1 或 非 0 失败；
  - 也可以使用 `echo` 输出一个字符串作为函数的返回值。
- 调用函数仅使用其函数名，如 `funcName`；
- **所有函数在使用前必须定义**，即函数调用必须要在函数声明之后。

### 6.2. 函数参数

```bash
func() {
    echo "第一个参数为 $1 !"
    echo "第二个参数为 $2 !"
    ...
    echo "第十个参数为 ${10} !"
    ...
}

# 调用并传参
func param1 param2 param3
```

**说明**：

- 在函数体内部，通过 `$n` 的形式来获取参数的值，例如：`$1` 表示第一个参数，`$2` 表示第二个参数；
- 当 `n >= 10` 时，需要使用 `${n}` 来获取参数。

## 7. 包含文件（封装函数库）

通常我们将公用的函数抽离到单独文件，以便重复调用，减少冗余代码。

对于一个函数库文件：

- 后缀名任意，通常使用 `.lib` 进行标识；
- 一般不授予可执行权限；
- 不需要跟脚本放在同一级目录，只需在脚本引用时指定；
- 通常第一行一般使用 `#!/bin/echo` 输出警告信息，避免用户执行。

示例：

```bash
#!/bin/echo
# /home/user1/lib/comm_function.lib

function add {
    echo "`expr $1 + $2`"
}
#!/bin/bash
# /home/user1/test.sh

# 引入函数库文件
# 使用绝对 或 相对路径
. ./lib/comm_function.lib

# 使用文件中的函数
add 1 3
➜  sh -x test_functions.sh
+ . ./lib/comm_function.lib
+ add 1 3
++ expr 1 + 3
+ echo 4
4
```

## 8. 常用命令

### 8.1. find 命令

语法：`find [路径] [选项] [操作]`

#### 选项

| 选项            | 说明                    | 选项                     | 说明                                        |
| --------------- | ----------------------- | ------------------------ | ------------------------------------------- |
| `-name`         | 文件名                  | `-iname`                 | 文件名（忽略大小写）                        |
| `-perm 777`     | 文件权限                | `-type f｜d｜l｜c｜b｜p` | 文件类型                                    |
| `-user`         | 文件属主                | `-nouser`                | 无有效属主                                  |
| `-group`        | 文件属组                | `-nogroup`               | 无有效属组                                  |
| `-size -n｜+n`  | 文件大小                | `-prune`                 | 排除某些查找目录<br/>通常与 `-path` 一同使用 |
| `-mindepth n`   | 从 n 级子目录开始查找   | `-maxdepth n`            | 最多搜索到 n 级子目录                       |
| `-mtime -n｜+n` | 文件修改时间（天）      | `-mmin -n｜+n`           | 文件修改时间（分钟）                        |
| `-newer file1`  | 文件修改时间比 file1 早 |                          |                                             |

示例：

```bash
# 文件名
➜  find /etc/ -name '*.conf'

# 文件类型
# f 文件；d 目录；c 字符设备文件；
# b 块设备文件；l 链接文件；p 管道文件
➜  find /etc/ -type f

# 文件大小
# -n 小于等于；+n 大于等于
➜  find . -size +100M
➜  find . -size -10k

# 文件修改时间
# -n < n天以内修改过的文件；
# n = n 天修改过得文件；
# +n > n天以外修改过的文件；
➜  find . -mtime -3
➜  find . -mtime 3
➜  find . -mtime +3

# 排除目录
# -path ./test1 -prune 排除 test1 目录
# -path ./test2 -prune 排除 test2 目录
# -o type f 固定结尾写法
➜  find . -path ./test1 -prune -o -path ./test2 -prune -o type f
```

#### 操作

- `-print` 打印输出
- `-exec 'command' {} \;` 其中 `{}` 是前面查找匹配到的结果
- `-ok` 与 `exec` 功能一样，但每次操作都给用户提示，由用户决定是否执行对应的操作。

示例：

```bash
# 查找 30 天以前的日志文件并删除
➜  find /var/log -name '*.log' -mtime +30 -exec rm -f {} \;

# 查找所有 .conf 文件，并移动到指定目录
➜  find /etc/apache -name '*.conf' -exec cp {} /home/user1/backup \;
```

### 8.2. echo 命令

用于字符串的输出，基本格式 `echo string`。

使用示例：

```bash
# 显示普通字符
➜  echo "It is a test" # 输出 It is a test

# 显示转义字符
➜  echo "\"It is a test\"" # 输出 "It is a test"

# 显示变量
#!/bin/sh
NAME="xiaoming"
➜  echo "$NAME It is a test" # 输出 xiaoming is a test

# 显示换行
➜  echo -e "OK! \n" # -e 开启转义
➜  echo "It is a test"

# 显示不换行
➜  echo -e "OK! \c" # -e 开启转义 \c 不换行
➜  echo "It is a test"

# 显示结果定向至文件
➜  echo "It is a test" > myfile

# 显示命令执行结果
➜  echo `date`
```

### 8.3. printf 命令

模仿 C 程序库（library）里的 `printf()` 程序，主要用于格式化输出。

默认 `printf` 不会像 `echo` 自动添加换行符，我们可以手动添加 `\n`。

其基本语法格式为：

```bash
➜  printf  format-string  [arguments...]
```

说明：

- `format-string` 为格式控制字符串
- `arguments` 为参数列表。

示例：

```bash
➜  printf "%-10s %-8s %-4s\n" 姓名 性别 体重kg
➜  printf "%-10s %-8s %-4.2f\n" 郭靖 男 66.1234
➜  printf "%-10s %-8s %-4.2f\n" 杨过 男 48.6543
➜  printf "%-10s %-8s %-4.2f\n" 郭芙 女 47.9876
姓名     性别   体重kg
郭靖     男      66.12
杨过     男      48.65
郭芙     女      47.99
```

其中：

- `%s` `%c` `%d` `%f` 都是格式替代符；
- `%-10s` 指一个宽度为 10 个字符（`-` 表示左对齐，没有则表示右对齐），任何字符都会被显示在 10 个字符宽的字符内，如果不足则自动以空格填充，超过也会将内容全部显示出来。
- `%-4.2f` 指格式化为小数，其中 `.2` 指保留 2 位小数。

更多使用示例：

```bash
# 没有引号也可以输出
➜  printf %s abcdef

# 格式只指定了一个参数，但多出的参数仍然会按照该格式输出，format-string 被重用
➜  printf %s abc def
abcdef

➜  printf "%s\n" abc def
abc
def

# 如果没有 arguments，那么 %s 用NULL代替，%d 用 0 代替
➜  printf "%s and %d \n"
 and 0
```

### 8.4. test 命令

用于检查某个条件是否成立，它可以进行数值、字符和文件三个方面的测试（详见第 3 节运算符部分）。

基本使用示例：

```bash
cd /bin
if test -e ./bash
then
    echo '文件已存在!'
else
    echo '文件不存在!'
fi
```

### 8.5. xargs 命令

用于将第一个命令的结果当做参数传递给第二个命令。

示例：

```bash
➜  find -name "*.c" | xargs ls -l
```

### 8.6. sed 命令

`sed` 命令主要用于替换文本中的字符串。

示例：

```bash
# 将 filename.txt 中的 abc def 替换为 def abc
➜  sed -i 's@abc def@def abc@' filename.txt
```

在前面的例子中，`@` 可以是其他符号，它的主要作用在于区分需要替换的字符串和原始字符串。

### 8.7. tee 命令

`tee` 命令主要用于将一段文字写入文件。

```bash
cat <<EOF | tee ~/.config/pip/pip.conf
[global]
index-url=http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
EOF
```

## 9. 补充

### 9.1. 变量替换

| 规则                         | 说明                   | 示例 `var="Hello shell"`       |
| ---------------------------- | ---------------------- | ------------------------------ |
| `${变量#匹配规则}`           | 从头开始匹配，最短删除 | `${var#*e}` => `llo shell`     |
| `${变量##匹配规则}`          | 从头开始匹配，最长删除 | `${var##*e}` => `ll`           |
| `${变量%匹配规则}`           | 从尾开始匹配，最短删除 | `${var%e*}` => `Hello sh`      |
| `${变量%%匹配规则}`          | 从尾开始匹配，最长删除 | `${var%%e*}` => `H`            |
| `${变量/旧字符串/新字符串}`  | 只替换匹配到的第一个   | `${var/e/*}` => `H*llo shell`  |
| `${变量//旧字符串/新字符串}` | 全部替换               | `${var//e/*}` => `H*llo sh*ll` |

### 9.2. 有类型变量

Shell 中变量默认都是**字符串**，除非使用以下方式声明。

| declare 或 typeset 参数   | 说明                         |
| ------------------------- | ---------------------------- |
| `-r`                      | 只读                         |
| `-i`                      | 整数                         |
| `-a`                      | 数组                         |
| `-f`                      | 在脚本中显示定义的函数和内容 |
| `-F`                      | 在脚本中显示定义的函数       |
| `-X`                      | 将变量声明为环境变量         |

示例：

```bash
➜  declare -r var1="hello shell type"
➜  var1="hello lalala"
zsh: read-only variable: var1
```

### 9.3. 使用 bc 进行浮点数运算

系统内置，支持 `+`、`-`、`*`、`/`、`^ 指数`、`% 取余`，并使用 `scale` 指定小数位数，默认 `0`。

示例：

```bash
➜  which bc
/usr/bin/bc

# 示例
➜  echo "5+4" | bc
9
➜  echo "5-4" | bc
1
➜  echo "5*4" | bc
20
➜  echo "5/4" | bc
1
➜  echo "scale=3;5/4" | bc
1.250
➜  echo "5%4" | bc
1
➜  echo "5^4" | bc
625
```

### 9.4. [ ... ] 与 [[ ... ]]

- `[[` 是关键字，许多 Shell 并不支持这种方式。
  - 所有的字符都不会被文件扩展或是标记分割，但是会有参数引用和命令替换；
  - 更能防止脚本里的许多逻辑错误，比如说 `&&`, `||`, `<` 和 `>` 操作符能在一个 `[[ ... ]]` 测试里通过，但在 `[ ... ]` 结构会发生错误。
  - 会进行算术扩展。
- `[` 是一条命令，与 `test` 等价，大多数的 Shell 都支持。
  - 在其中的表达式应是它的命令行参数，所以串比较操作符 `>` 与 `<` 必须转义，否则就变成 IO 重定向操作符了。
  - 不会进行算术扩展。


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

## 命令行高亮

```{code-block} bash
PS1='\[\e]0;\w\a\]\n\[\e[32m\]\u@\h \[\e[33m\]\w\[\e[0m\]\n\$ '
```

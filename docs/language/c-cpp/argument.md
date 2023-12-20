# 命令行传参

```cpp
#include <getopt.h>
#include <iostream>

using namespace std;

int main(int argc, char *argv[])
{
    /**
     * struct option
     * {
     *      const char * name;
     *      int          has_arg;
     *      int        * flag;
     *      int          val;
     * }
     */
    static struct option long_options[] = {
        {"reqarg", required_argument, NULL, 'r'},
        {"optarg", optional_argument, NULL, 'o'},
        {"noarg", no_argument, NULL, 'n'},
        {NULL, 0, NULL, 0},
    };

    while (1)
    {
        int option_index = 0, opt;

        /**
         * getopt_long 会遍历 argv 数组，在每次迭代中，它会返回下一个选项字符（如果有），
         * 然后，这个字符与长选项列表进行比较，如果匹配，则对应的操作会被执行，如果没有匹配，那么函数将返回 -1。
         * 只有一个字符，不带冒号，只表示选项，如 -c
         * 一个字符，后接一个冒号，表示选项后面带一个参数，如 -a 100
         * 一个字符，后接两个冒号——表示选项后面带一个可选参数，即参数可有可无，如果带参数，则选项与参数直接不能有空格，如 -b200
         */
        opt = getopt_long(argc, argv, "a::b:c:d", long_options, &option_index);

        if (opt == -1)
            break;

        printf("opt = %c\t\t", opt);
        printf("optarg = %s\t\t", optarg);
        printf("optind = %d\t\t", optind);
        printf("argv[%d] = %s\t\t", optind, argv[optind]);
        printf("option_index = %d\n", option_index);
    }

    return 0;
}
// g++ -std=c++20 -O2 -Wall -pedantic -pthread main.cpp && ./a.out --reqarg 100 --optarg=200 --noarg
// g++ -std=c++20 -O2 -Wall -pedantic -pthread main.cpp && ./a.out –reqarg=100 --optarg=200 --noarg
// g++ -std=c++20 -O2 -Wall -pedantic -pthread main.cpp && ./a.out --reqarg 100 --optarg --noarg
```

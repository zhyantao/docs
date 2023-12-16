# stderr

```cpp
// stderr.cpp

#include <stdio.h>

void div2(int n)
{
    if (n % 2 != 0)
    {
        fprintf(stderr, "Error: The input must be an even number. Here it's %d\n", n);
    }
    else
    {
        int result = n / 2;
        fprintf(stdout, "Info: The result is %d\n", result);
    }
    return;
}

int main()
{
    for (int n = -5; n <= 5; n++)
        div2(n);
    return 0;
}
```

```c
// stderr.c

#include <stdio.h>

void div2(int n)
{
    if (n % 2 != 0)
    {
        fprintf(stderr, "Error: The input must be an even number. Here it's %d\n", n);
    }
    else
    {
        int result = n / 2;
        fprintf(stdout, "Info: The result is %d\n", result);
    }
    return;
}

int main()
{
    for (int n = -5; n <= 5; n++)
        div2(n);
    return 0;
}
```

```bash
./program | less

./program > output.log
./program 1> output.log
./program >> output.log

./program > /dev/null

./program 2> error.log

./program > output.log 2> error.log

./program &> all.log

./program > all.log 2>&1
```
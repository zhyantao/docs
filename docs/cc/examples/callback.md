# 回调函数

```cpp
#include <stdio.h>

typedef void (*callback_t)(char* str, int len);

// (1) 编写回调函数
void myfunction(char* str, int len) {
    for (int i = 0; i < len; i++) {
        printf("%c", str[i]);
    }
}

// (3) 调用回调函数
int callback(callback_t callback_fn, char* str, int len) {
    callback_fn(str, len);
    return 0;
}

int main() {
    // char *str = "hello world"; // error
    char str[] = "hello world";
    int len = sizeof(str);
    // (2) 注册回调函数
    callback(myfunction, str, len);
}
```

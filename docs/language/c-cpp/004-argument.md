# 命令行传参

```cpp
#include <iostream>

using namespace std;

int main(int argc, char *argv[])
{
    for (int i = 0; i < argc; i++)
        cout << i << ": " << argv[i] << endl;
}
```

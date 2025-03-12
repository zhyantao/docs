# ubus 工作原理

在使用 ubus 进行进程间通信时，通常不需要通过共享对象（`.so` 文件）来直接调用另一个守护进程的函数。ubus 提供了一种更高层次的抽象，使得进程可以通过消息传递的方式调用其他进程提供的服务或方法。

在 ubus 框架中，当一个守护进程注册了一个服务方法后，该方法的代码会被编译进守护进程的可执行文件中，并在守护进程启动时加载到内存中。然而，这个方法的实际执行是在被其他进程通过 ubus 调用时才发生的。具体来说，有以下几个关键点：

1. **守护进程启动**：

   - 当守护进程启动时，它会初始化 ubus 上下文，并注册一个或多个服务对象。
   - 注册的服务对象包含方法及其对应的处理函数。
   - 这些方法的代码和数据结构会被加载到内存中，但方法本身不会立即执行。

2. **方法注册**：

   - 守护进程通过调用 `ubus_add_object` 将服务对象注册到 ubus 服务器。
   - 这个过程中，ubus 服务器会记录服务对象及其方法的信息，但不会执行这些方法。

3. **方法调用**：
   - 当其他进程通过 ubus 调用注册的方法时，ubus 服务器会将调用请求转发给相应的守护进程。
   - 守护进程接收到请求后，会调用对应的方法处理函数来处理请求。
   - 方法处理函数在被调用时才会实际执行，处理请求并返回结果。

## 示例说明

假设有一个守护进程 `mydaemon`，它注册了一个名为 `exampleMethod` 的方法：

```cpp
#include <libubus.h>
#include <blobmsg_json.h>

struct ubus_context* ctx;
struct ubus_object obj;
struct ubus_method methods[] = {
    UBUS_METHOD("exampleMethod", example_method_handler, example_method_policy),
};

static const struct ubus_object_type obj_type = UBUS_OBJECT_TYPE("exampleService", methods);
static struct ubus_object obj = {
    .name = "exampleService",
    .type = &obj_type,
    .methods = methods,
    .n_methods = ARRAY_SIZE(methods),
};

// 方法处理函数
static int example_method_handler(struct ubus_context* ctx, struct ubus_object* obj,
                                  struct ubus_request_data* req, const char* method,
                                  struct blob_attr* msg) {
    // 处理请求
    printf("exampleMethod called\n");
    return 0;
}

int main() {
    // 初始化 ubus 上下文
    ctx = ubus_connect(NULL);
    if (!ctx) {
        fprintf(stderr, "Failed to connect to ubus\n");
        return -1;
    }

    // 注册对象
    ubus_add_object(ctx, &obj);

    // 进入事件循环
    ubus_loop(ctx, NULL, 0);

    return 0;
}
```

在这个示例中：

- `exampleMethod` 的处理函数 `example_method_handler` 会被编译进 `mydaemon` 的可执行文件中，并在守护进程启动时加载到内存中。
- 但是，`example_method_handler` 函数只有在其他进程通过 ubus 调用 `exampleMethod` 时才会被执行。

## 常用指令

### 查看已注册的 ubus objects

```bash
ubus list
```

### 查看 object 包含的 functions

```bash
ubus -v list system
```

## 总结

- **加载到内存**：方法的代码和数据结构在守护进程启动时会被加载到内存中。
- **实际执行**：方法的处理函数只有在被其他进程通过 ubus 调用时才会实际执行。

这种设计使得 ubus 能够高效地管理进程间通信，同时保持良好的性能和资源利用。

# __thread

`__thread` 是 GCC 提供的一个线程局部存储 (TLS) 的修饰符。

在 C 语言中，如果一个变量被 `__thread` 修饰，那么这个变量就可以被每个线程单独拥有一份实例，各个线程对这个变量的操作不会影响到其他线程。这种变量也被称为线程局部存储变量。

`__thread` 变量的生命周期是与线程相同的，当线程开始时创建，在线程结束时销毁。这意味着，对于每一个线程来说，所有使用了 `__thread` 修饰的变量都拥有一个独立的实例。

需要注意的是，`__thread` 只能用于修饰全局变量或静态变量，不能用于函数内部的局部变量。

参考文献：

1. <https://gcc.gnu.org/onlinedocs/gcc-3.3.1/gcc/Thread-Local.html>
2. <https://stackoverflow.com/questions/28523480/what-does-gcc-thread-do>

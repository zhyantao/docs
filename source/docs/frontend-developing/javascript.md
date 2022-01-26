# JavaScript

## 基本语法

### 变量声明

`var`（弃用）、`const`（变量不允许修改）、`let`（变量允许修改）

### 标识符

JS 保留关键字

### 注释

`//` 和 `/** */`

### 区块

`{}`，但是不构成单独的作用域（ES5）。

### 条件语句

用 `===` 表示判断

### 循环语句

用 `for...of` 遍历对象或数组比用 `for...in` 要更加简洁。

当然最笨的方法还是 `for...i` 的方式。

## 数据类型

### typeof 运算符

### 空值

null（0）、undefined（NaN）

### 数值

注意：`1 === 1.0 // true`，JS 中默认都是浮点数

常用函数：

- `parseInt()`
- `parseFloat()`
- `Boolean()`
- `isFinite()`
- `isNaN()`

### 字符串

建议统一使用单引号。

索引示例：`'hello'[1] // e`

JS 默认编码是 Unicode

Base64 编码和 ASCII 码的相互转换（不支持非 ASCII 码）：

- `btoa()`
- `atob()`

Tips：ES6 在表示字符串时，如果用反引号，可以分多行写一个字符串，但是单引号和双引号不行。

### 对象

格式：`{键值对的集合}`

Key 又叫属性，Value 可以是任意数据类型。

建议不要用 with 语句，因为它没有对作用域做清晰划分。

### 函数

函数的三种表达方法：

1. 普通表示：`function f() {}`
2. 匿名函数：`const f = function() {}`
3. 箭头函数：`const f = () => {}`

函数参数可以传值也可以传址。

闭包：解决 var 的作用域问题。
在函数内再定义一个函数，内部函数可以访问外部函数定义的变量。

立即调用函数：`(function() {})()`

### 数组

格式：`[]`

本质是特殊的对象。因此数组中的元素可以是任意数据类型。

数组中的可以含有空位：`[1, ,3]`

## 运算符

### 算术运算符

### 比较运算符

### 布尔运算符

### 二进制位运算符

### 运算顺序

## 语法专题

### 数据类型的转换

`Number()`、`String()`、`Boolean()`

### 错误处理机制

`const err = new Error('错误提示');`

六种错误：

- SyntaxError
- ReferenceError：引用不存在的变量
- RangeError：数组或堆栈越界
- TypeError
- URIError
- EvalError：eval 中的函数没有正常执行

`throw new Error('错误提示');`

`try...catch...finally`

### 编程风格

### cosole 对象与控制台

## 标准库

### Object 对象

凡是定义在 Object.prototype 对象上的属性和方法，将被所有实例对象共享

### JSON 对象

是一个值，且只能值一个值。

### 属性描述对象

一种内部数据结构，用来描述对象的属性，控制它的行为。比如该属性是否可写、可遍历等等。

### Array 对象

用于数组。

### 包装对象

常用的包装对象有：

- Boolean 对象。
- Number 对象
- String 对象

### Math 对象

### Date 对象

### RegExp 对象

提供正则表达式功能。

## 面向对象编程

JavaScript 语言的对象体系，不是基于 “类” 的，而是基于构造函数（constructor）和原型链（prototype）。

### 基本使用

ES5 声明类的模板：`const V = function() {this.a = 100;}` 跟普通函数的写法无异。ES6 有了 `class` 关键字。

使用 “类” 的模板创建对象：`const v = new V();`

`this` 指向当前对象。

### 继承

每一个函数都有 `prototype` 属性，指向一个对象：意思是继承这个对象。

所有对象都有自己的原型对象（`prototype`）。

用 `prototype` 属性定义的方法或属性，将被子类共享。

将 `prototype.constructor` 指向自己以声明默认构造函数。

### 模块

基本写法：

```{code-block} javascript
const module1 = new Object({
    _count : 0,
    m1 : function (){
        //...
    },
    m2 : function (){
        //...
    }
});
```

### Object 对象的相关方法

## 异步操作

JavaScript 现在采用单线程模型，将来也是。

AJAX = Asynchronous JavaScript and XML（异步的 JavaScript 和 XML）。
AJAX 最大的优点是在不重新加载整个页面的情况下，可以与服务器交换数据并更新部分网页内容。

### 异步操作的模式

回调函数：（意思是，我们在别的地方把函数定义好了，现在需要用到这个函数直接调用就好了）

```{code-block} javascript
function f1 (callback) {
    callback(); // 执行 callback 函数
}
```

事件监听：

```{code-block} javascript
f1.on('done', f2) // 如果 f1 执行完了，就开始执行 f2
```

发布/订阅：

```{code-block} javascript
jQuery.subscribe('done', f2)
```

### 异步操作的流程控制

串行执行：递归调用

并行执行：`items.forEach() {}`

串行和并行混合

### 定时器

`setTimeout()`：设定一段时间后执行某个函数

`setInterval()`：设定每隔一段时间执行某个函数，无限循环

`clearTimeout()`

`clearInterval()`

`debounce()`：防止用户在一段时间内重复提交

### Promise 对象

JavaScript 的异步操作解决方案，为异步操作提供统一接口。

`Promise` 是一个对象，也是一个构造函数。

优点：用 `then` 方法，像写同步操作一样编写异步操作。

`(new Promise(f1)).then(f2).then(f3);`

`then()` 用法解析：[Ref](https://wangdoc.com/javascript/async/promise.html#then-%E7%94%A8%E6%B3%95%E8%BE%A8%E6%9E%90)

## DOM

Node 接口

NodeList 接口、HTMLCollection 接口

ParentNode 接口、ChildNode 接口

Document 接口

Element 接口

属性操作

Text 节点、DocumentFragment 节点

CSS 操作

Mutation Observer API

## 事件

EventTarget 接口

事件模型

Event 对象

鼠标事件

键盘事件

进度事件

表单事件

触摸事件

拖拉事件

其他常见事件

GlobalEventHandlers 接口

## 浏览器模型

window 对象

Navigator 对象、Screen 对象

Cookie

XMLHttpRequest 对象

同源限制

CORS 通信

Storage 接口

History 对象

Location 对象、URL 对象、URLSearchParams 对象

ArrayBuffer 对象、Blob 对象File 对象

FileList 对象、FileReader 对象

表单、FormData 对象

IndexedDB API

Web Worker

## 参考文献

1. [JavaScript 基础教程](https://wangdoc.com/javascript/basic/introduction.html)
2. [现代 JavaScript 教程](https://zh.javascript.info/)
3. [JavaScript 思维导图](https://kdocs.cn/l/cqVRohCmQWBZ)

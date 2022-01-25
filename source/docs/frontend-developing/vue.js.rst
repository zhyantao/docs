.. _vue.js-basic:

=======
Vue.js
=======


`Vue.js <https://v3.cn.vuejs.org/>`__ 是一个用于创建用户界面的开源 JavaScript 框架，也是一个创建单页应用的 Web 应用框架，能够简化 Web 开发。
Vue 所关注的核心是 MVC 模式中的视图层，同时，它也能方便地获取数据更新，并通过组件内部特定的方法实现视图与模型的交互。

Vue 主要特性包括：

- 组件：组件是基础 `HTML 元素 <https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element>`_\ 的扩展，可以方便地自定义其\ **数据**\ 与\ **行为**\ 。
- 模板：使用基于 `HTML 模板 <https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/template>`_\ 语法，可以将 `DOM <https://developer.mozilla.org/zh-CN/docs/Web/API/Document_Object_Model/Introduction>`_ 元素与底层 `Vue 实例 <https://cn.vuejs.org/v2/guide/instance.html>`_\ 中的数据\ **绑定**\ 。满足响应式设计。
- 响应式设计：在视图与对应的模型绑定后，Vue **自动观测模型的变动**\ ，并重新绘图。
- 过渡效果：Vue 在插入、更新或者移除 DOM 时，提供多种不同方式的应用过渡效果。
- 单文件组件：为了更好地适应复杂的项目，Vue 支持以 ``.vue`` 为扩展名的文件来定义一个完整组件，用以替代使用 ``Vue.component`` 注册组件的方式。


安装与部署
----------

如果只是在一个页面中使用 Vue.js，那么普通的 JS 导入就可以直接使用了。
在项目中安装 Vue.js 只需要下载 `vue.js <https://vuejs.org/js/vue.js>`_ 然后，用代码引入就可以了。

.. code-block:: html

    <script src="vue.js" type="text/javascript" charset="utf-8"></script>

当然，如果项目更加复杂，一般通过单文件组件（后面会讲）的方式在构建应用，通常首先需要安装 npm、vue-cli、webpack 三个工具。
然后在命令行中键入 ``vue ui`` 创建一个项目。


创建第一个 Vue 应用
-------------------

在 JS 中用 ``new Vue()`` 即可创建一个 Vue 应用，它接收参数为 JSON 格式的对象。
众所周知，JSON 格式的对象是由很多键值对组成的，它的键一般都是字符串，而值的变化就比较多，可以是字符串，列表，也可以是函数。

这个 JSON 格式的对象负责完成 Vue.js 与 DOM 元素的数据绑定，采用 **声明式渲染** 的方式完成页面渲染。

JSON 对象中，除了 ``el`` 的值是一个字符串外，其他键（如 ``data`` 、 ``methods`` ）的值都是一个对象。

代码清单 1：

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title></title>
    <script src="vue.js" type="text/javascript" charset="utf-8"></script>
    </head>
    <body>
        <div id="app">                  <!-- 一般通过 id 索引模块 -->
            {{ message }} {{name}}      <!-- HTML 声明式模板语法，文本插值，双大括号 -->
        </div>
        
        <script type="text/javascript">
        var app = new Vue({
            el: '#app',                 // el：用于和对应的 DOM 元素一一对应（绑定）
            data: {                     // data：为相应 DOM 元素下的变量赋值
                message: 'Hello Vue!',
                name: 'vue'
            }
        });
        </script>

    </body>
    </html>


数据与方法
----------

在上一节，学习了如何修改 HTML 模板中的变量值，这一章学习如何修改 Vue 应用中的变量值。

在 Vue 实例中， ``$`` 表示该实例的属性或方法，访问 Vue 实例或 JS 对象的属性或方法用点操作符 ``.``\ 。
因为，在 JS 脚本中单大括号表示 ``{对象}``\ ，因此，下例中修改变量 a 的值时使用了两次点操作符，在默认情况下 ``$data`` 可以省略不写。
注意，\ ``vm.$watch`` 是 Vue 实例的方法，用于观测变量的值是否发生改变。

代码清单 2：

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title></title>
    <script src="vue.js" type="text/javascript" charset="utf-8"></script>
    </head>
    <body>
    <div id="app">
        {{a}}
    </div>

    <script type="text/javascript">

        var test = { a : 1 }; // 声明变量
        var vm = new Vue({
            el   : "#app",
            data : test // data 是 Vue 实例的属性
            // data : { a : 3 } // data : test 的等价形式
        });

        // 观察 a 的变化，如果 a 发生了变化，就执行function
        vm.$watch('a', function(to, from) {
            console.log(to, from);
        })

        // vm.$data.a = "test...." // 访问 vue 实例 $data 属性下的 a 变量
        vm.a = "123"    // vm.$data.a 的等价形式，$data 可以省略不写

    </script>

    </body>
    </html>


生命周期
---------

Vue 实例的生命周期如下图，要理解这个图现在还有些困难，随着学习的深入，后面可以回过头来回顾。

在 Vue 的生命周期中，他会做很多事情，图中的绿色部分时 Vue 的内部实现，红色部分使我们需要关注的。

红色部分表示钩子函数，也是我们在开发中 **可以重写** 的部分，在 Vue 运行到相应阶段的时候，会自动回调。

实际开发中，一般的工作流程是：

- 根组件在 ``created`` 阶段请求网络数据；
- 将数据保存在 Vue 实例的 ``data`` 部分；
- 通过父子组件之间的通信，子组件将数据展示在 DOM 上。

.. image:: ../../_static/images/vue-lifecycle.*

代码清单 3：

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title></title>
    <script src="vue.js" type="text/javascript" charset="utf-8"></script>
    </head>
    <body>
    <div id="app">
        {{msg}}
    </div>
    <script type="text/javascript">

        var vm = new Vue({

            el : "#app",

            data : {
                msg : "hi vue",
            },

            // 在实例初始化之后，数据观测 (data observer) 和 event/watcher 事件配置之前被调用。
            beforeCreate : function(){
                console.log('beforeCreate');
            },

            // 在实例创建完成后被立即调用。
            // 在这一步，实例已完成以下的配置：数据观测 (data observer)，属性和方法的运算，watch/event 事件回调。
            // 然而，挂载阶段还没开始，$el 属性目前不可见。
            created : function(){
                console.log('created');
            },

            // 在挂载开始之前被调用：相关的渲染函数首次被调用
            beforeMount : function(){
                console.log('beforeMount');
            },

            // el 被新创建的 vm.$el 替换, 挂载成功
            mounted : function(){
                console.log('mounted');
            },

            // 数据更新时调用
            beforeUpdate : function(){
                console.log('beforeUpdate');
            },

            // 组件 DOM 已经更新, 组件更新完毕
            updated : function(){
                console.log('updated');
            }
        });

        setTimeout(function(){
            vm.msg = "change ......";
        }, 3000);

    </script>
    </body>
    </html>


模板语法-插值
-------------

双大括号可以实现文本插值，如果是 HTML 代码的话，那么无法进行解析，
这时候可以借助 Vue 提供的 ``v-html`` 命令，将插值解析成 HTML 代码。

``v-bind:class="表达式"`` ，暂时可以忽略，后面会讲。

代码清单 4：

.. code-block:: html
    :emphasize-lines: 11, 12

    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title></title>
    <script src="vue.js" type="text/javascript" charset="utf-8"></script>
    </head>
    <body>
    <div id="app">
        {{msg}}
        <p>Using mustaches: {{ rawHtml }}</p>   <!-- 用 HTML 模板语法声明的变量 -->
        <p v-html="rawHtml"></p>                <!-- 用指令声明的变量（凡是带有 v- 开头的都是 Vue 指令） -->
        <div v-bind:class="color">test...</div>
        <p>{{ number + 1 }}</p>
        <p>{{ ok ? 'YES' : 'NO' }}</p>
        <p>{{ message.split('').reverse().join('') }}</p>
    </div>
    <script type="text/javascript">

        var vm = new Vue({

            el : "#app",
            
            data : {
                msg : "hi vue",
                rawHtml : '<span style="color:red">This should be red</span>',
                color : 'blue',
                number : 10,
                ok : 1,
                message : "vue"
            }
        });
        vm.msg = "hi....";

    </script>

    <style type="text/css">
        .red {
            color: red;
        }
        
        .blue {
            color: blue; 
            font-size: 100px;
        }
    </style>
    </body>
    </html>


模板语法-指令
-------------

如下代码清单 5 所示，展示了一些比较常用的指令：

- ``v-if="表达式"``
- ``v-on:事件名="表达式"``
- ``v-bind:属性名="表达式"``

``v-if`` 中的表达式结果为真的时候，Vue 会渲染当前的 DOM 元素，如果为假，该元素将不会出现在网页上。
``v-if`` 和 ``v-show`` 的不同之处就在于 ``v-show`` 不管表达式是真还是假，都会出现在网页上，只不过为假的时候， ``display=none`` 。

``v-on`` 中的事件名可以是鼠标单击、双击、键盘按下、抬起等浏览器自动监听的时间，也可以是自定义事件，
比如我们在父子组件通信的时候，子组件向父组件通过 ``$emit("事件名", 变量名)`` 发送的事件。
``v-on`` 中的表达式可以是一个函数名，事件发生时触发这个函数，也可以是普通的表达式语句表示做出什么动作。

``v-bind`` 是用的比较多的一个指令了，因此也有语法糖的写法形式，就是省略 ``v-bind`` ，直接用冒号代替。
当属性名为普通的属性（如 ``href`` 、 ``src`` ）时，我们可以在 Vue 实例的 ``data`` 选项中 **给表达式中的变量** 赋初值。
当属性名是 ``class`` 或 ``style`` 时，我们就可以动态地改变样式了，见下一节 ``class`` 与 ``style`` 绑定。


代码清单 5：

.. code-block:: text

    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title></title>
    <script src="vue.js" type="text/javascript" charset="utf-8"></script>
    </head>
    <body>
    <div id="app">
        <p v-if="seen">现在你看到我了</p>
        <a v-bind:href="url">可以更换的动态URL</a>
        <div v-on:click="click1">   <!-- 因为下面的 click.stop 这里的 click1 不会触发了 -->
            <div v-on:click.stop="click2">
            <!-- <div @click.stop="click2"> 和上面一行效果一样 -->
                click me
            </div>
        </div>
    </div>
    <script type="text/javascript">

        var vm = new Vue({

            el : "#app",

            data : {
                seen : true,
                url : "https://cn.vuejs.org/v2/guide/syntax.html"
            },

            methods:{
                click1 : function () {
                    console.log('click1......');
                },
                click2 : function () {
                    console.log('click2......');
                }
            }
        });

    </script>
    </body>
    </html>


class 与 style 绑定
-------------------

``class`` 和 ``内联样式`` 是 HTML 元素的常用属性，通过 ``v-bind`` 可以将两者进行绑定。
有了这个绑定，我们后面可以通过 ``class`` 来动态地修改 HTML 元素的样式了。

代码清单 6：

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title></title>
    <script src="vue.js" type="text/javascript" charset="utf-8"></script>
    </head>
    <body>
    <div id="app">
        <div class="test" 
            v-bind:class="[ isActive ? 'active' : '', isGreen ? 'green' : '']" 
            style="width:200px; height:200px; text-align:center; line-height:200px;">
                hi vue
        </div>
        
        <div :style="{color:color, fontSize:size, background: isRed ? '#FF0000' : ''}">
            hi vue
        </div>
    </div>
    <script type="text/javascript">

        var vm = new Vue({
        
            el : "#app",

            data : {
                isActive : true,
                isGreen : true,
                color : "#FFFFFF",
                size : '50px',
                isRed : true
            }
        });
    
    </script>

    <style>
        .test{font-size:30px;}
        .green{color:#00FF00;}
        .active{background:#FF0000;}
    </style>
    </body>
    </html>


条件渲染
--------

``v-if`` 是 Vue 的一个指令，我们上面已经用过了，因此这一章比较容易理解。

代码清单 7：

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title></title>
    <script src="vue.js" type="text/javascript" charset="utf-8"></script>
    </head>
    <body>
    <div id="app">
        <div v-if="type === 'A'"> <!-- if 和  else-if 语法，选择某一个 div 进行渲染 -->
            A
        </div>
        <div v-else-if="type === 'B'">
            B
        </div>
        <div v-else-if="type === 'C'">
            C
        </div>
        <div v-else>
            Not A/B/C
        </div>
        <h1 v-show="ok">Hello!</h1>
    </div>

    <script type="text/javascript">

        var vm = new Vue({
            el : "#app",
            data : {
                type : "B",
                ok : true
            }
        });
        
    </script>

    <style type="text/css">

    </style>
    </body>
    </html>


列表渲染
--------

列表渲染指的是有序列表或无序列表的渲染。通常用 ``v-for`` 来操作列表中的每个元素。语法为 ``v-for="表达式"`` 。

说到表达式，必然后变量和关键字，那么一般常用的表达式是 ``v-for="item,index in items"`` 。
这其中只有 ``in`` 是关键字，其他都是变量，可以在 ``data`` 选项中赋初值，在 ``methods`` 中定义函数进行修改（一般与 ``@click`` 搭配，有事件触发函数）。

需要注意的是，如果 ``items`` 是数组，第一个元素 ``item`` 表示数组的值，第二个返回值 ``index`` 表示数组的索引；
如果 ``items`` 是对象，第一个元素 ``item`` 表示对象的值，第二个返回值 ``index`` 表示对象的键。

代码清单 8：

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title></title>
    <script src="vue.js" type="text/javascript" charset="utf-8"></script>
    </head>
    <body>
    <div id="app">
        <ul>
            <li v-for="item, index in items" :key="index">
                {{ item }} : {{ index }} : {{ item.message }}
            </li>
        </ul>
        <ul>
            <li v-for="value, key in object">
                {{ key }} : {{ value }}
            </li>
        </ul>
    </div>

    <script type="text/javascript">
        var vm = new Vue({
            el : "#app",
            data : {
                items : [
                    { message: 'Foo' },
                    { message: 'Bar' }
                ],
                object: {
                    title: 'How to do lists in Vue',
                    author: 'Jane Doe',
                    publishedAt: '2016-04-10'
                }
            }
        });
    </script>
    </body>
    </html>


事件绑定
--------

``v-on`` 用来监听 DOM 事件，比如鼠标点击（ ``@click`` ），键盘抬起（ ``@keyup`` ），Enter 键抬起（ ``@keyup.enter`` ）。

语法 ``v-on:click="表达式"`` 。这里的表达式，既可以是一个函数名，也可以是一个逻辑表达式。

实际开发中，因为 ``v-on`` 比较常用，语法糖的写法是用 ``@`` 符号代替 ``v-on:`` 。

代码清单 9：

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title></title>
    <script src="vue.js" type="text/javascript" charset="utf-8"></script>
    </head>
    <body>
    <div id="app">
        <div id="example-1">
            <button v-on:click="counter += 1"> 数值 :  {{ counter }} </button><br />
            <button v-on:dblclick="greet('abc', $event)">Greet</button>
        </div>
    </div>
    <script type="text/javascript">
        var vm = new Vue({
            el : "#app",
            data : {
                counter: 0,
                name : "vue"
            },
            methods:{
                greet : function (str, e) {
                    alert(str);
                    console.log(e);
                }
            }
        });
    </script>
    <style type="text/css">

    </style>
    </body>
    </html>


表单输入绑定
------------

我们之前都是通过在后台修改数据，来让前端页面的内容得到修改，这时如果反过来，在前端页面修改值，
并不会修改后台中的 ``data`` 中变量的值，这是因为只有单向绑定。

而用 ``v-model`` 指令在表单 ``<input>`` 、 ``<textarea>`` 及 ``<select>`` 元素上创建\ **双向数据绑定**\ 。
使得前端页面的修改可以在后台收到改动，后台的改动也会在前端页面中展示出来。

尽管有些神奇，但 ``v-model`` 本质上不过是语法糖，它整合了 ``:value`` 和 ``@input`` 两个事件，是一个缩写版本。
但是双向绑定只在表单中实现了，如果想要自己在其他元素中实现双向绑定，则需要自己实现上面两个完整的事件。

代码清单 10：

.. code-block:: text

    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title></title>
    <script src="vue.js" type="text/javascript" charset="utf-8"></script>
    </head>
    <body>
    <div id="app">
        <div id="example-1">
            <input v-model="message" placeholder="edit me">
            <p>Message is: {{ message }}</p>
            <textarea v-model="message2" placeholder="add multiple lines"></textarea>
            <p style="white-space: pre-line;">{{ message2 }}</p>
            <br />

            <div style="margin-top:20px;">
                <input type="checkbox" id="jack" value="Jack" v-model="checkedNames">
                <label for="jack">Jack</label>

                <input type="checkbox" id="john" value="John" v-model="checkedNames">
                <label for="john">John</label>

                <input type="checkbox" id="mike" value="Mike" v-model="checkedNames">
                <label for="mike">Mike</label>
                <br>
                <span>Checked names: {{ checkedNames }}</span>
            </div>

            <div style="margin-top:20px;">
                <input type="radio" id="one" value="One" v-model="picked">
                <label for="one">One</label>
                <br>

                <input type="radio" id="two" value="Two" v-model="picked">
                <label for="two">Two</label>
                <br>
                <span>Picked: {{ picked }}</span>
            </div>
            <button type="button" @click="submit">提交</button>
        </div>

    </div>

    <script type="text/javascript">

        var vm = new Vue({
            
            el : "#app",

            data : {
                message : "test",
                message2 : "hi",
                checkedNames : ['Jack', 'John'],
                picked : "Two"
            },
            
            methods: {
                submit : function () {
                    console.log(this.message);
                }
            }
        });

    </script>

    <style type="text/css">
    </style>
    </body>
    </html>


父子组件通信
------------

组件是可复用的 Vue 实例，可以通过 ``Vue.component('组件名', JSON 对象)`` 创建组件。 ``JSON 对象`` 的一般格式为：

.. code-block:: html

    {
        template: `<div>某些 HTML 代码</div>`,
        ...
    }

需要明白的是，组件之间有父子关系，父组件和子组件之间的通信因此成为了很关键的一环。

父组件向子组件通信：在子组件中用 ``props=['子组件变量名']`` **接收消息**\ 。
在父组件模板中的通过属性 ``v-bind:子组件变量名="父组件变量名"`` **中转消息**\ 。
在父组件中通过 ``data`` 初始化父组件变量的值来 **发送消息**\ ，
又因为 ``data`` 中的变量值可以通过 ``methods`` 或 ``computed`` 方法进行修改，从而实现对网页内容的实时渲染。

子组件向父组件通信：在子组件的某个方法中用 ``$emit('子组件事件名', 子组件变量名)`` **发送消息**\ 。
在父组件模板中用 ``@子组件事件名='父组件事件名'`` 监听子组件的事件，触发父组件事件。
**消息本体** 就是 ``子组件变量名`` 这个参数保存了数据，因此实现消息的传递。
这样当父组件拿到变量后，可以保存到自己的 ``data`` 部分，就可以 **实现持久化** 了。


代码清单 11：

.. code-block:: text

    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title></title>
    <script src="vue.js" type="text/javascript" charset="utf-8"></script>
    </head>
    <body>

    <!-- HTML 代码中的变量只能在 根组件 中注册，不能在 子组件 中注册 -->
    <div id="app">
        <buttoncounter :ctitle="ptitle" @cclick="pclick"> <!-- 子组件向父组件发送事件 -->
            <h2>上面这个按钮接收由子组件发送过来的 cclick 事件，触发父组件的 pclick 事件</h2>
        </buttoncounter>
        <buttoncounter :ctitle="ptitle"></buttoncounter>
    </div>

    <script type="text/javascript">

        // 实现子组件
        const buttoncounter = {

            // 在子组件中写 props 列表/对象，获取父组件相关变量的值
            props: ['ctitle'],

            // 定义子组件的模板，在模板中使用变量
            template:
                `<div>
                    <button v-on:click="clickfunc">
                        {{ctitle}} 子组件在统计你点击了 {{ count }} 次.
                    </button>
                    <slot></slot>
                </div>`,

            // 子组件中的变量注册
            // data() 必须为函数，因为每个组件都希望有自己的变量且互不干扰
            data() {
                return {
                    count: 0
                }
            },

            // 定义子组件的方法
            methods:{
                clickfunc() { // ES6 的写法
                    this.count ++; // 你会发现子组件的 count 在增长
                    this.$emit('cclick', this.count); // 发出一个 cclick 事件，参数为 this.count
                }
            }
        }

        // Vue 实例（根组件、父组件）
        var vm = new Vue({
            el : "#app",
            data : {
                ptitle: '父组件赋予的标题：'
            },
            methods:{
                pclick(e) { // ES6 写法
                    console.log(e);
                }
            },

            // 局部组件注册，形成父子关系
            components: {
                buttoncounter // ES6 简写形式，全写是 buttoncounter: buttoncounter
            }
        });

    </script>
    <style type="text/css">

    </style>
    </body>
    </html>

如果父组件想直接访问子组件的方法或属性可以用 ``$children[i].func()`` 或 ``$refs.name`` 。

如果子组件想访问父组件的方法或属性用 ``$parent.func()`` 或 ``$root.func()`` 。

实际开发中，用 ``$children`` 和 ``$root`` 都比较少，因为 ``$children`` 在增加或删除子组件时会发生索引错误。

单文件组件
----------

到目前为止，我们学完了 Vue 主要的基础内容。基于组件的开发方式更适用于大项目。

首先，安装准备环境：

1. 安装 npm：\ ``npm -v``
2. 由于网络原因 安装 cnpm：\ ``npm install -g cnpm --registry=https://registry.npm.taobao.org``
3. 安装 vue-cli：\ ``cnpm install -g @vue/cli``
4. 安装 webpack：\ ``cnpm install -g webpack``

然后，在命令行中使用 ``vue ui`` 创建一个 Vue 项目，包管理器选择 ``npm`` 其他保持默认即可。

创建完成后，关闭浏览器，用 IDE 打开项目。可以看到， ``public`` 是项目开发完成后部署的文件。
``src`` 是源代码文件，我们将在这里完成开发工作。

1. ``src/App.vue`` 是项目的入口文件，在 ``script`` 中 ``import`` 自定义的组件；
2. 在 ``script`` 中使用 ``export default`` 注册组件；
   
   - 用 ``name:`` 给组件起个名字；
   - 用 ``props`` 在子组件中声明需要向父组件请求的数据；
   - 用 ``data() {}`` 给 ``template`` 中的变量赋予初值
   - 用 ``methods: {}`` 定义函数方法实现
   - 用 ``mounted() {}`` 自动调用函数（因为有些函数不需要监听鼠标或键盘事件）

3. 在 ``template`` 中使用已经注册的组件，即可完成整个开发流程。

以上，基础知识全部更新完毕。

进阶阅读
--------

实际项目开发中，我们可能需要 **频繁使用** 一些更加高级的功能，比如：

- 用 `插槽 <https://v3.cn.vuejs.org/guide/component-slots.html>`_ 占位，后面根据内容自定义补充到这个位置；
- 使用 `Vue Router <https://next.router.vuejs.org/>`_ 实现前端路由；
- 使用 `Vuex <https://next.vuex.vuejs.org/zh/>`_ 让多个组件可以共享某些信息，比如用户的登录状态等等；
- 使用 `Axios <https://axios-http.cn>`_ 处理并发的网络请求，借助
  `Promise 对象 <https://wangdoc.com/javascript/async/promise.html>`_ 良好的封装实现异步通信。

未来有更多的知识等待探索。比如，如何更加优雅地组织代码，如何尽量减少第三方库混在业务逻辑中。

当你检查是否已经掌握了上面的知识，可以通过阅读我的 
`代码仓库笔记 <https://gitee.com/zhyantao/learn-programing-languages/tree/master/vue.js>`_ 
检查一下，或者也可以当做复习用。

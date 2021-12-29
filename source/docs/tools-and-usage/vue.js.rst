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

在项目中安装 Vue.js 只需要下载 `vue.js <https://vuejs.org/js/vue.js>`_ 然后，用代码引入就可以了。

.. code-block:: html

    <script src="vue.js" type="text/javascript" charset="utf-8"></script>


创建第一个 Vue 应用
-------------------

在 JS 中用 ``new`` 即可创建一个 Vue 应用。把 DOM 元素的 ``id`` 赋值给 ``el`` 就可以把 Vue 应用与 DOM 元素绑定，数据绑定最常用方式就是使用双大括号。

在 HTML 模板语法中，双大括号通常表示 ``{{变量}}``\ ，这里满足插值语法。在 Vue 应用中可以使用 ``data`` 选项修改变量值。

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
        <div id="app">
            {{ message }} {{name}}
        </div>
        
        <script type="text/javascript">
        var app = new Vue({
            el: '#app',
            data: {
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
    var data = { a : 1 };
    var vm = new Vue({
        el   : "#app",
        data : data
    });

    vm.$watch('a', function(newVal, oldVal){ // 观察 a 的变化，如果 a 发生了变化，就执行function
        console.log(newVal, oldVal);
    })

    vm.$data.a = "test...."

    </script>

    </body>
    </html>


生命周期
---------

Vue 实例的生命周期如下图，要理解这个图现在还有些困难，随着学习的深入，后面可以回过头来回顾。

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
        beforeCreate:function(){
            console.log('beforeCreate');
        },
        // 在实例创建完成后被立即调用。
        // 在这一步，实例已完成以下的配置：数据观测 (data observer)，属性和方法的运算，watch/event 事件回调。
        // 然而，挂载阶段还没开始，$el 属性目前不可见。
        created	:function(){
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
注意，第 13 行用到 Class 与 Style 绑定的语法，对于本节来说有些超纲，很快后面就会学到。

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
        <p>Using mustaches: {{ rawHtml }}</p>
        <p v-html="rawHtml"></p>
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
            color:'blue',
            number : 10,
            ok : 1,
            message : "vue"
        }
    });
    vm.msg = "hi....";
    </script>
    <style type="text/css">
    .red{color:red;}
    .blue{color:blue; font-size:100px;}
    </style>
    </body>
    </html>


模板语法-指令
-------------

Vue 实例中提供了若干指令，比如 ``v-if="seen"``\ 。
注意，这里的 ``seen`` 虽然用双引号括起来，但是它是一个变量，可以在 ``data`` 选项中对其赋值，实现动态地控制网页行为。
在 ``data`` 选项中对变量赋值的时候，这里的值才是一个常量。
在 HTML 代码中用 ``@`` 符号来声明一个事件，在 Vue 中使用 ``methods`` 选项对相应的事件行为做出操作。
注意，下面的代码中 click me 虽然是普通文本，但是，网页也在统计点击行为。

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
        <div @click="click1">
            <div @click.stop="click2">
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

class 和内联样式是 HTML 元素的常用属性，通过 ``v-bind`` 可以将两者进行绑定。
class 和内联样式的属性值（结果）可以是字符串、数组、对象，只需要能够计算出结果即可。
因此，有了这个绑定，我们后面可以通过 class 来动态地修改 HTML 元素的样式了。

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
        <div 
        class="test" 
        v-bind:class="[ isActive ? 'active' : '', isGreen ? 'green' : '']" 
        style="width:200px; height:200px; text-align:center; line-height:200px;">
            hi vue
        </div>
        
        <div 
        :style="{color:color, fontSize:size, background: isRed ? '#FF0000' : ''}">
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
        <div v-if="type === 'A'">
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

列表渲染指的是有序列表或无序列表的渲染。通常用 ``v-for`` 来操作列表中的每个元素。

``v-for`` 这个语法很奇怪，比如 ``"item, index in items"`` 同样都是用双引号括起来的，但是只有 ``in`` 是关键字，其他都是变量，可以在 ``data`` 选项中修改。

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
            {{index}}{{ item.message }}
            </li>
        </ul>
        <ul>
            <li v-for="value, key in object">
                {{key}} : {{ value }}
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

``v-on`` 指令可以用来监听 DOM 事件，并在触发时运行一些 JavaScript 代码。

通过在 Vue 实例中提供相应的属性或方法即可完成绑定。

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

你可以用 ``v-model`` 指令在表单 ``<input>`` 、 ``<textarea>`` 及 ``<select>`` 元素上创建\ **双向数据绑定**\ 。
它会根据控件类型自动选取正确的方法来更新元素。
尽管有些神奇，但 ``v-model`` 本质上不过是语法糖。
它负责监听用户的输入事件以更新数据，并对一些极端场景进行一些特殊处理。

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
            message2 :"hi",
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


组件基础
--------

组件是可复用的 Vue 实例，可以通过 ``Vue.component('component_name', attrs)`` 创建一个组件。

- 用 ``props`` 来声明自定义组件的一组变量；
- 与 ``new`` 出来的 Vue 实例不同的是， ``data`` 必须是一个函数，来给变量赋初值；
- 在 ``template`` 中使用变量；
- 在 ``methods`` 中定义自定义组件的事件的响应。

在 Vue 实例的 ``methods`` 中定义 HTML 元素中的事件的响应。

``this.$emit('func_name', 'other_parameters')`` 将触发函数 ``func_name``\ ，该函数将 ``other_parameters`` 作为参数。

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
    <div id="app">
        <button-counter title="title1 : " @clicknow="clicknow">
            <h2>hi...h2</h2>
        </button-counter>
        <button-counter title="title2 : "></button-counter>
    </div>
    <script type="text/javascript">
    Vue.component('button-counter', {
        props: ['title'],
        data: function () {
            return {
            count: 0
            }
        },
        template: '<div><h1>hi...</h1><button v-on:click="clickfun">{{title}} You clicked me {{ count }} times.</button><slot></slot></div>',
        methods:{
            clickfun : function () {
                this.count ++;
                this.$emit('clicknow', this.count);
            }
        }
    })
    var vm = new Vue({
        el : "#app",
        data : {
            
        },
        methods:{
            clicknow : function (e) {
                console.log(e);
            }
        }
    });
    </script>
    <style type="text/css">

    </style>
    </body>
    </html>


组件注册
--------

有了上一节的基础，这一节的学习变得异常简单，组件注册只需要在 ``new`` 出来的 Vue 实例中的 ``components`` 选项中提供组件的属性和方法就可以了。

代码清单 12：

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
        <button-counter></button-counter>
        <test></test>
    </div>
    <script type="text/javascript">
    Vue.component('button-counter', {
        props: ['title'],
        data: function () { return {} },
        template: '<div><h1>hi...</h1></div>',
        methods:{}
    })
    var vm = new Vue({
        el : "#app",
        data : {
            
        },
        components:{
                test : {
                    props: ['title'],
                    data: function () { return {} },
                    template: '<div><h3>h3...</h3></div>',
                    methods:{}
            }
        }
    });
    </script>
    <style type="text/css">

    </style>
    </body>
    </html>


单文件组件
----------

到目前为止，我们学完了 Vue 主要的基础内容，后续开发，我们将基于此方法进行，它更适用于大项目。

首先，安装准备环境：

1. 安装 npm：\ ``npm -v``
2. 由于网络原因 安装 cnpm：\ ``npm install -g cnpm --registry=https://registry.npm.taobao.org``
3. 安装 vue-cli：\ ``cnpm install -g @vue/cli``
4. 安装 webpack：\ ``cnpm install -g webpack``

然后，在命令行中使用 ``vue ui`` 创建一个 Vue 项目，包管理器选择 ``npm`` 其他保持默认即可。

创建完成后，用 HBuilderX 打开项目。
可以看到， ``public`` 文件夹是项目开发完成后部署的文件。
``HelloWorld.vue`` 是单文件组件，src 是源代码文件，我们将在这里完成开发工作。步骤如下：

1. ``src/App.vue`` 是项目的入口文件，在 ``script`` 中 ``import`` 自定义的组件；
2. 在 ``script`` 中使用 ``export default`` 注册组件；
   
   - 用 ``name:`` 注册组件的名称（给组件起个名字）
   - 用 ``props`` 注册属性（声明在 ``template`` 中可以使用的全局变量）
   - 用 ``data() {}`` 注册对应的数据（声明在 ``script`` 中可以使用的全局变量）
   - 用 ``methods: {}`` 注册方法（函数方法定义）
   - 用 ``mounted() {}`` 调用方法（函数调用）

3. 在 ``template`` 中使用已经注册的组件，即可完成整个开发流程。

以上，全部更新完毕。

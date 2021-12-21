# Three.js 入门

由于 WebGL 较为底层，作为开发工具来讲，往往难以满足效率。
因此诞生了 Babylon.js、Three.js、Layabox.js、Scene.js、Thing.js 等上层框架。
关于它们之间的对比，参考 [WebGL 图库研究](https://cloud.tencent.com/developer/article/1746988)。

入门学习 Three.js 的资料并不太多，建议从官网开始 <https://threejs.org/manual/#zh/fundamentals>。

```{figure} ../../_static/images/threejs-structure.*
:height: 300px

基础的 three.js 应用结构
```

下方文字节选自 [基础 - three.js manual](https://threejs.org/manual/#zh/fundamentals)，
对上图进行了解释。

**渲染器（Renderer）** 可以说是 Three.js 的主要对象。
把一个场景和一个摄像机到渲染器中，然后它会将摄像机
*视椎体* 中的三维场景渲染成一个二维图片显示在画布上。

```{figure} ../../_static/images/frustum-3d.*
:height: 300px

视锥体（frustum）
```

**场景图** 是一个树状结构，由很多对象组成：

- 一个场景对象（Scene）
- 多个网格对象（Mesh）
- 光源对象（Light）
- 群组（Group）
- 三维物体（Object3D）
- 摄像机对象（Camera）

**场景（Scene）** 对象定义了场景图最基本的要素，并包了含背景色和雾等属性。

**摄像机（Camera）** 一半在场景图中，一半在场景图外。
这表示在 three.js 中，摄像机和其他对象不同的是，它不一定要在场景图中才能起作用。
相同的是，摄像机作为其他对象的子对象，同样会继承它父对象的位置和朝向。

**几何体（Geometry）** 对象代表一些几何体的顶点信息。
Three.js 内置了许多基本几何体如球体、立方体、平面、狗、猫、人、树、建筑等。
你也可以创建自定义几何体或从文件中加载几何体，比如 Blender，Maya，Cinema 4D。

**材质（Material）** 对象代表绘制几何体的表面属性，包括使用的颜色，和光亮程度。
一个材质可以引用一个或多个纹理，这些纹理将图像包裹到几何体的表面。
有些材质反光，有些无法反光，因此也就无法用光照来渲染。

**网格（Mesh）** 对象可以理解为用一种特定的 *材质* 来绘制的一个特定的 *几何体*。
材质和几何体可以被多个网格对象共享使用。

**纹理（Texture）** 对象是一个从文件中加载、画布上生成或由另一个场景渲染出的图像。

**光源（Light）** 对象代表不同种类的光。不添加光源，背景将一片漆黑。

下面是一段 `Vue` 代码：

```{code-block} html
<template>
    <div id="container" style="width: 100%; height: 100%"></div>
</template>

<script>
import * as THREE from 'three'

export default {
    name: 'ThreeTest',
    // 声明全局变量
    data () {
        return {
            container: null,
        }
    },
    // 声明函数方法
    methods: {
        init: function () {
            this.container = document.getElementById('container');

            // 设置渲染器（renderer）
            const renderder = new THREE.WebGLRenderer();
            renderder.setSize(this.container.clientWidth, this.container.clientHeight);
            this.container.appendChild(renderder.domElement);

            // 设置相机
            const camera = new THREE.PerspectiveCamera(
                75, this.container.clientWidth / this.container.clientHeight, 0.01, 1000
            );
            camera.position.set(0, 0, 5);


            // 设置场景
            const scene = new THREE.Scene();

            // 添加光照，让元素看起来更直观
            const light = new THREE.DirectionalLight(0xffffff, 1);
            light.position.set(-1, 2, 4);
            scene.add(light);

            // 向场景中添加元素
            const geometry = new THREE.BoxGeometry(1, 1, 1);  // 指定几何体（物体形状）
            // 制作立方体
            function makeInstance(geometry, color, x) {
                const material = new THREE.MeshPhongMaterial({color});  // 指定材质（物体表面）
                const cube = new THREE.Mesh(geometry, material);  // 创建网格对象
                scene.add(cube);  // 将创建的网格添加到场景中，此时它是静止的，观察不出是个立方体
                cube.position.x = x;
                return cube;
            }
            const cubes = [
                makeInstance(geometry, 0x44aa88, 0),
                makeInstance(geometry, 0x8844aa, -2),
                makeInstance(geometry, 0xaa8844, 2),
            ];

            // 让立方体转起来
            function render(time) {
                time *= 0.001; // 秒

                cubes.forEach((cube, ndx) => {
                    const speed = 1 + ndx * .1;
                    const rot = time * speed;
                    cube.rotation.x = rot;
                    cube.rotation.y = rot;

                });
                
                // 显示场景
                renderder.render(scene, camera);

                requestAnimationFrame(render);
            }

            requestAnimationFrame(render);  // 回调函数
        }
    },
    // 函数调用
    mounted () {
        this.init();
    }
}

</script>

<style>
</style>
```

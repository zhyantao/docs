# 数据结构与算法

## 栈和队列

栈的方法：

- void push(int number);
- int pop();
- int peek();

队列的方法：[^zuocy]

- void add(int number);
- int poll();
- int peek();

### 递归调用模板

```{code-block} java
public class Recursion {

    public static void r(int i) {

        // 一定要有 return，否则陷入死循环无法退出
        if ( i < 0 )
            return; 
        
        // 递归前的变量值会压入系统栈（常用于临时保存变量）
        System.out.print(i + " ");
        
        // 递归语句
        r(--i);

        // 递归后的语句可以从系统栈中取出刚刚压入的值
        System.out.print(i + " ");
    
    }

    public static void main(String[] args) {
        r(3);
    }

}
// 3 2 1 0 -1 0 1 2
```

尝试改变终止条件的位置，得到了不一样的输出。输出的内容基本上都是对称分布的，只不过对称轴位置不一样。

```{code-block} java
public class Recursion {

    public static void r(int i) {

        // 递归前的变量值会压入系统栈（常用于临时保存变量）
        System.out.print(i + " ");

        // 尝试改变 return 的位置，但是它一定不能出现在递归调用之后
        if ( i < 0 )
            return; 
           
        // 递归语句
        r(--i);
     
        // 递归后的语句可以从系统栈中取出刚刚压入的值
        System.out.print(i + " ");
    
    }

    public static void main(String[] args) {
        r(3);
    }

}
// 3 2 1 0 -1 -1 0 1 2
```

## 参考文献

[^zuocy]: 左程云. 程序员代码面试指南[M]. 电子工业出版社, 2019. URL: <https://kdocs.cn/l/cn65qULuDrFX>

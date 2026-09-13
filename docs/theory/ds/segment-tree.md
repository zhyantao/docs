# 线段树

> 线段树是一棵**完全二叉树**，每个节点维护数组上一段区间的聚合信息（和、最大值等），
> 支持 $O(\log n)$ 的**单点更新**与**区间查询**，配合懒标记还可 $O(\log n)$ 完成**区间更新**。
> 与树状数组相比：线段树功能更全（可维护区间最值、可区间更新），代价是代码更长、常数更大。
> 属于灵茶山艾府"常用数据结构"题单（前缀和/栈/队列/堆/字典树/并查集/树状数组/线段树）的最后一块。

## 一、原理

- 根节点 `1` 代表整个区间 `[0, n-1]`；
- 节点 `p` 代表区间 `[l, r]`，其左右孩子 `2p`、`2p+1` 分别代表 `[l, mid]`、`[mid+1, r]`，其中 `mid = (l+r)/2`；
- 区间信息自底向上合并（`tree[p] = tree[2p] + tree[2p+1]`）；
- 数组大小开 **4 倍 n** 保证不越界。

## 二、单点更新 + 区间求和

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
struct SegTree {
    int n;
    vector<int> tree;
    SegTree(vector<int>& a) : n(a.size()), tree(4 * n) { build(a, 1, 0, n - 1); }

    void build(vector<int>& a, int p, int l, int r) {
        if (l == r) { tree[p] = a[l]; return; }
        int mid = (l + r) / 2;
        build(a, p * 2, l, mid);
        build(a, p * 2 + 1, mid + 1, r);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }

    void update(int idx, int val, int p, int l, int r) { // 单点改为 val
        if (l == r) { tree[p] = val; return; }
        int mid = (l + r) / 2;
        if (idx <= mid) update(idx, val, p * 2, l, mid);
        else            update(idx, val, p * 2 + 1, mid + 1, r);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }

    int query(int ql, int qr, int p, int l, int r) {     // 区间 [ql, qr] 的和
        if (ql <= l && r <= qr) return tree[p];          // 完全覆盖
        int mid = (l + r) / 2, res = 0;
        if (ql <= mid) res += query(ql, qr, p * 2, l, mid);
        if (qr > mid)  res += query(ql, qr, p * 2 + 1, mid + 1, r);
        return res;
    }
};
```

:::

:::{tab-item} Java
:sync: java

```java
class SegTree {
    int n;
    int[] tree;
    SegTree(int[] a) {
        n = a.length;
        tree = new int[4 * n];
        build(a, 1, 0, n - 1);
    }
    void build(int[] a, int p, int l, int r) {
        if (l == r) { tree[p] = a[l]; return; }
        int mid = (l + r) / 2;
        build(a, p * 2, l, mid);
        build(a, p * 2 + 1, mid + 1, r);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }
    void update(int idx, int val, int p, int l, int r) {
        if (l == r) { tree[p] = val; return; }
        int mid = (l + r) / 2;
        if (idx <= mid) update(idx, val, p * 2, l, mid);
        else            update(idx, val, p * 2 + 1, mid + 1, r);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }
    int query(int ql, int qr, int p, int l, int r) {
        if (ql <= l && r <= qr) return tree[p];
        int mid = (l + r) / 2, res = 0;
        if (ql <= mid) res += query(ql, qr, p * 2, l, mid);
        if (qr > mid)  res += query(ql, qr, p * 2 + 1, mid + 1, r);
        return res;
    }
}
```

:::
::::

```{note}
区间查询的关键是**分三类**讨论：完全覆盖直接返回；否则下放到左右孩子；完全不相交的区间不会被递归到（由调用处条件保证）。
```

## 三、区间更新 + 懒标记（Lazy）

区间整体加 `v` 时，若对每个叶子都更新则退化为 $O(n)$。**懒标记**让更新"停在完全覆盖的节点"：
先只改该节点并打上标记，等将来查询/更新下放到孩子时再"下推"标记。

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
struct SegTreeLazy {
    int n;
    vector<long long> tree, lazy;   // lazy[p] 表示节点 p 待下推的区间增量
    SegTreeLazy(vector<int>& a) : n(a.size()), tree(4 * n), lazy(4 * n) { build(a, 1, 0, n - 1); }

    void build(vector<int>& a, int p, int l, int r) {
        if (l == r) { tree[p] = a[l]; return; }
        int mid = (l + r) / 2;
        build(a, p * 2, l, mid);
        build(a, p * 2 + 1, mid + 1, r);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }

    void pushDown(int p, int l, int r) {          // 下推懒标记
        if (lazy[p] == 0 || l == r) return;
        int mid = (l + r) / 2;
        tree[p * 2] += lazy[p] * (mid - l + 1);
        tree[p * 2 + 1] += lazy[p] * (r - mid);
        lazy[p * 2] += lazy[p];
        lazy[p * 2 + 1] += lazy[p];
        lazy[p] = 0;
    }

    void rangeAdd(int ql, int qr, int v, int p, int l, int r) { // 区间 [ql, qr] 加 v
        if (ql <= l && r <= qr) { tree[p] += (long long)v * (r - l + 1); lazy[p] += v; return; }
        pushDown(p, l, r);
        int mid = (l + r) / 2;
        if (ql <= mid) rangeAdd(ql, qr, v, p * 2, l, mid);
        if (qr > mid)  rangeAdd(ql, qr, v, p * 2 + 1, mid + 1, r);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }

    long long query(int ql, int qr, int p, int l, int r) {
        if (ql <= l && r <= qr) return tree[p];
        pushDown(p, l, r);
        int mid = (l + r) / 2;
        long long res = 0;
        if (ql <= mid) res += query(ql, qr, p * 2, l, mid);
        if (qr > mid)  res += query(ql, qr, p * 2 + 1, mid + 1, r);
        return res;
    }
};
```

:::
::::

```{note}
- 更新/查询**经过**某个带标记的节点时，必须先 `pushDown`，否则孩子信息是过期的；
- 懒标记的值要随子区间长度按比例计入 `tree`（区间加 v 时，长度为 len 的区间总和增加 `v * len`）；
- 若维护的是区间最大值而非和，把"求和 + 贡献"改为"取 max"即可，思路不变。
```

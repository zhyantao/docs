# 排序与查找

> 堆排序、归并、插入、快速排序、大根堆重建、希尔排序；二分查找与 KMP 模板。

## 排序算法

### 堆排序

::::{tab-set}
:::{tab-item} Java
:sync: java

`PriorityQueue` 就是一个小根堆结构，可以直接使用。

```java
void heapSort(int[] arr) {
    if (arr == null || arr.length < 2)
        return;
    // 构建大根堆（方法一）
    // for (int i = 0; i < arr.length; i++)
    // heapInsert(arr, i);
    // 构建大根堆（方法二，更快）
    for (int i = arr.length - 1; i >= 0; i--)
        heapify(arr, i, arr.length);
    // 每次选择并移除堆顶元素，放到末尾
    int heapSize = arr.length;
    swap(arr, 0, --heapSize);
    while (heapSize > 0) {
        heapify(arr, 0, heapSize);
        swap(arr, 0, --heapSize);
    }
}
```

:::
::::

### 归并排序

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
void mergeSort(int[] arr, int[] tmp, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSort(arr, tmp, left, mid);
        mergeSort(arr, tmp, mid + 1, right);
        merge(arr, tmp, left, mid, right);
    }
}

void merge(int[] arr, int[] tmp, int left, int mid, int right) {
    int pLeft = left;
    int pRight = mid + 1;
    int pTmp = left;
    // 将左右子数组较小的元素依次插入到 tmp 中
    while (pLeft <= mid && pRight <= right) {
        if (arr[pLeft] <= arr[pRight])
            tmp[pTmp++] = arr[pLeft++];
        else
            tmp[pTmp++] = arr[pRight++];
    }
    // 复制剩余元素到 tmp 中
    while (pLeft <= mid)
        tmp[pTmp++] = arr[pLeft++];
    while (pRight <= right)
        tmp[pTmp++] = arr[pRight++];
    // 必须保存局部的排序结果，否则下次还是乱序
    for (int i = left; i <= right; i++)
        arr[i] = tmp[i];
}

// 调用：int[] arr = new int[]{7, 3, 2, 6};
int[] tmp = new int[arr.length]; // 辅助空间
mergeSort(arr, tmp, 0, arr.length - 1);
```

::::

### 插入排序

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
void insertSort(int[] arr) {
    int j; // 用于扫描 i 之前的元素
    for (int i = 1; i < arr.length; i++) {
        int tmp = arr[i];
        for (j = i; j > 0 && arr[j - 1] > tmp; j--)
            arr[j] = arr[j - 1]; // 向后移动元素
        arr[j] = tmp;
    }
}
```

::::

### 快速排序

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
void quickSort(int[] arr, int left, int right) {
    if (left < right) {
        int pivot = arr[left]; // 随机选基准点
        int i = left, j = right; // 不修改原变量
        while (i < j) {
            while (i < j && arr[j] > pivot)
                j--; // 从右往左：首个比 pivot 小的值
            if (i < j) {
                arr[i] = arr[j]; // 丢失 arr[i]
                i++;
            }
            while (i < j && arr[i] < pivot)
                i++; // 从左往右：首个比 pivot 大的值
            if (i < j) {
                arr[j] = arr[i];
                j--;
            }
        }
        arr[i] = pivot; // 找回 arr[i]
        // -- partition 和递归代码的分割线 -- //
        quickSort(arr, left, i - 1);
        quickSort(arr, i + 1, right);
    }
}
// 调用：quickSort(arr, 0, arr.length - 1);
```

::::

### 重建大根堆

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
// 向已有堆的末尾插入元素，重建大根堆
void heapInsert(int[] arr, int i) {
    while (arr[i] > arr[(i - 1) / 2]) {
        swap(arr, i, (i - 1) / 2);
        i = (i - 1) / 2;
    }
}

// 移除堆顶元素(放在末尾)，重建大根堆
void heapify(int[] arr, int i, int heapSize) {
    while (i < heapSize) {
        int l = 2 * i + 1; // 左孩子指针
        int r = 2 * i + 2; // 右孩子指针
        int max = i;
        if (l < heapSize && arr[l] > arr[max])
            max = l;
        if (r < heapSize && arr[r] > arr[max])
            max = r;
        if (max == i)
            break;
        swap(arr, i, max);
        i = max;
    }
}
```

::::

### 希尔排序

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
void shellSort(int[] arr) {
    for (int step = arr.length / 2; step >= 1; step /= 2) {
        for (int r = step; r < arr.length; r++) {
            int tmp = arr[r]; // 把 r 放到最终位置
            int l = r - step;
            while (l >= 0 && arr[l] > tmp) {
                arr[l + step] = arr[l]; // 将 l 右移
                l -= step;
            }
            arr[l + step] = tmp; // 放置
        }
    }
}
```

::::

## 查找算法

### 二分查找

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
// 注意这里有多处使用 return
int binarySearch(int[] arr, int target, int left, int right) {
    if (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target)
            return mid;

        if (arr[mid] > target) // 向左查找
            return binarySearch(arr, target, left, mid - 1);

        if (arr[mid] < target) // 向右查找
            return binarySearch(arr, target, mid + 1, right);
    }
    return -1; // 没找到
}
```

:::
::::

### 二分答案

当问题具有**单调性**（可行/不可行以某个答案为分界）时，可以对"答案"本身二分，用 `check(mid)` 判断当前答案是否可行。这是灵茶山艾府"二分算法"题单的核心（二分答案/最小化最大值/最大化最小值/第 K 小）。

**模板：最大化最小值**（如分割数组的最大值最小、分配糖果）：

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
// check(mid) 判断"答案至少为 mid"是否可行，具有单调性
bool check(int mid) { /* 贪心/模拟验证 */ }

int maxMin(vector<int>& nums, int lo, int hi) {
    int ans = lo;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (check(mid)) {      // mid 可行，尝试更大的答案
            ans = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return ans;
}
```

:::

:::{tab-item} Java
:sync: java

```java
boolean check(int mid) { /* 贪心/模拟验证 */ }

int maxMin(int lo, int hi) {
    int ans = lo;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (check(mid)) {      // mid 可行，尝试更大的答案
            ans = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return ans;
}
```

:::
::::

**模板：最小化最大值**（如机器人能否在时限内完成、划分 k 段的最大段和）：

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
// check(mid) 判断"最大值不超过 mid"是否可行
bool check(int mid) { /* 贪心分段验证 */ }

int minMax(vector<int>& nums, int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (check(mid)) hi = mid;     // 可行则收窄上界
        else lo = mid + 1;
    }
    return lo;
}
```

:::

:::{tab-item} Java
:sync: java

```java
boolean check(int mid) { /* 贪心分段验证 */ }

int minMax(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (check(mid)) hi = mid;     // 可行则收窄上界
        else lo = mid + 1;
    }
    return lo;
}
```

:::
::::

```{note}
- **边界选取**：`lo`/`hi` 取答案的上下界（如数组最大值、总和）；无法确定时用 `0` 与"足够大"（如 `1e9`）；
- **判断单调性**：`check(mid)` 必须随 mid 单调变化（mid 越大越容易/越难满足），否则不能二分；
- 典型应用：`LC410 分割数组的最大值`、`LC875 爱吃香蕉的珂珂`、`LC1482 制作 m 束花所需的最少天数`；
- "第 K 小"类问题（如 `LC668 乘法表中第 k 小的数`）同样二分答案，统计 <= mid 的个数与 k 比较。
```

### KMP 算法

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
// next[] = 构建最长公共前后缀长度数组
void getNext(vector<int>& next, string pat) {
    // 初始化 next 数组的第一个元素为 0
    int j   = 0;
    next[0] = 0;

    for (int i = 1; i < pat.size(); i++) {
        // 当前字符不匹配时，回退 j 到 next[j-1] 的位置
        while (j > 0 && pat[i] != pat[j]) {
            j = next[j - 1];
        }
        // 当前字符匹配时，则 j 自增
        if (pat[i] == pat[j]) {
            j++;
        }
        // next[i] 表示当前位置与模式串匹配的起始位置
        next[i] = j;
    }
}

// 返回 pat 匹配 txt 的起始位置，若匹配失败则返回 -1
int kmp(string pat, string txt) {
    int n = txt.size();
    int m = pat.size();
    vector<int> next(m);
    getNext(next, pat);
    int j = 0;
    for (int i = 0; i < n; i++) {
        // 当当前字符不匹配且 j 大于 0 时，调整 j 的位置
        while (j > 0 && txt[i] != pat[j]) {
            j = next[j - 1];
        }
        // 当前字符匹配时，j 自增
        if (txt[i] == pat[j]) {
            j++;
        }
        // 匹配成功，返回匹配的起始位置
        if (j == m) {
            return i - m + 1;
        }
    }
    // 匹配失败，返回 -1
    return -1;
}
```

:::

:::{tab-item} Java
:sync: java

```java
// next 数组记录最长相等的前后缀长度
void getNext(int[] next, String pat) {
    next[0] = 0;
    int j = 0; // 失配后的回退点
    // 循环从 1 开始，不是 0
    for (int i = 1; i < pat.length(); i++) {
        char chi = pat.charAt(i);
        char chj = pat.charAt(j);
        while (j > 0 && chi != chj)
            j = next[j - 1]; // 回退
        if (chi == chj)
            j++;
        next[i] = j;
    }
}

int strStr(String txt, String pat) {
    if (pat.length() == 0)
        return 0;
    int[] next = new int[pat.length()];
    getNext(next, pat);
    int j = 0;
    for (int i = 0; i < txt.length(); i++) {
        chi = txt.charAt(i);
        chj = pat.charAt(j);
        while (j > 0 && chi != chj)
            j = next[j - 1];
        if (chi == chj)
            j++;
        if (j == pat.length())
            return i - pat.length() + 1;
    }
    return -1;
}
```

::::

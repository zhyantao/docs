# 回溯算法

> 组合、组合总和、非递减子序列、全排列、N 皇后、解数独等回溯模板。

## 回溯算法

### 组合 k 个数

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
// n 个数字的组合问题，其实等价于 n 个数字的全连接图问题
// 每个数字都可以作为起点，每个数字都可以作为终点，但是两条路径不能重合
void dfs(vector<vector<int>>& paths, vector<int>& path, int start, int n, int k) {
    if (path.size() == k) {
        paths.push_back(path);
        return;
    }

    // for (int i = start; i <= n - (k - path.size()) + 1; i++) { // 剪枝优化
    for (int i = start; i <= n; i++) {
        path.push_back(i);
        dfs(paths, path, i + 1, n, k); // dfs(i+1) 表示不可重复选
        path.pop_back();               // 回溯
    }

    return;
}

vector<vector<int>> combine(int n, int k) {
    vector<vector<int>> paths;
    vector<int> path;
    dfs(paths, path, 1, n, k);
    return paths;
}
```

:::
::::

### 组合总和（可重复选）

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
void dfs(vector<vector<int>>& paths, vector<int>& path, int start, vector<int>& candidates,
         int target) {
    if (target < 0) {
        return;
    }

    if (target == 0) {
        paths.push_back(path);
        return;
    }

    for (int i = start; i < candidates.size(); i++) {
        path.push_back(candidates[i]);
        dfs(paths, path, i, candidates, target - candidates[i]); // dfs(i) 表示可重复选
        path.pop_back();
    }
}

vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
    vector<vector<int>> paths;
    vector<int> path;
    dfs(paths, path, 0, candidates, target);
    return paths;
}
```

:::
::::

### 非递减子序列（去重）

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
// 判断是否为递增序列
bool isValid(vector<int>& path) {
    for (int i = 1; i < path.size(); i++) {
        if (path[i] < path[i - 1]) {
            return false;
        }
    }
    return true;
}

void dfs(vector<vector<int>>& paths, vector<int>& path, int start, vector<int>& nums) {
    if (path.size() > 1) {
        if (isValid(path)) {
            paths.push_back(path);
        }
    }

    unordered_set<int> used_set; // 对本层应用去重
    for (int i = start; i < nums.size(); i++) {
        if (used_set.find(nums[i]) != used_set.end()) { // 已经使用过 nums[i] 了
            continue;
        }

        path.push_back(nums[i]);
        used_set.insert(nums[i]);
        dfs(paths, path, i + 1, nums);
        // used_set.erase(nums[i]); // 不能解开注释
        path.pop_back();
    }
}

vector<vector<int>> findSubsequences(vector<int>& nums) {
    vector<vector<int>> paths;
    vector<int> path;
    dfs(paths, path, 0, nums);
    return paths;
}
```

:::
::::

### 全排列（不含重复元素）

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
void dfs(vector<vector<int>>& paths, vector<int>& path, vector<int>& nums,
         vector<bool>& used) {
    if (path.size() == nums.size()) {
        paths.push_back(path);
        return;
    }

    for (int i = 0; i < nums.size(); i++) {
        if (used[i]) {
            continue;
        }
        path.push_back(nums[i]);
        used[i] = true;
        dfs(paths, path, nums, used);
        used[i] = false;
        path.pop_back();
    }
}

vector<vector<int>> permute(vector<int>& nums) {
    vector<vector<int>> paths;
    vector<int> path;
    vector<bool> used(nums.size(), false);
    dfs(paths, path, nums, used);
    return paths;
}
```

:::
:::{tab-item} Java
:sync: java

```java
// 比如：模拟从黑箱子中取球的过程（有放回）
// 回溯不同于动态规划，动态规划有公式可循
// 用 arr 表示原始数组，用 used 剪枝优化
// 用 i == arr.length 判断递归是否终止
List<List<Integer>> ans = new ArrayList<>();
List<Integer> path = new ArrayList<>();

void dfs(int[] arr, boolean[] used, int i) {
    if (i == arr.length) {
        // 注意，深拷贝
        ans.add(new ArrayList<>(path));
        return;
    }
    // 每次都向 path 的第 j 个位置推送不同数字
    for (int j = 0; j < nums.length; j++) {
        if (!used[j]) {
            path.add(nums[j]);
            used[j] = true;
            dfs(nums, used, i + 1);
            used[j] = false; // 撤销原操作
            path.remove(path.size() - 1);
        }
    }
}
```

:::
::::

### 全排列（含重复元素）

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
void dfs(vector<vector<int>>& paths, vector<int>& path, vector<int>& nums,
         vector<bool>& used) {
    if (path.size() == nums.size()) {
        paths.push_back(path);
        return;
    }

    for (int i = 0; i < nums.size(); i++) {
        if (used[i] || (i > 0 && nums[i] == nums[i - 1] && !used[i - 1])) {
            continue;
        }

        path.push_back(nums[i]);
        used[i] = true;
        dfs(paths, path, nums, used);
        used[i] = false;
        path.pop_back();
    }
}

vector<vector<int>> permuteUnique(vector<int>& nums) {
    vector<vector<int>> paths;
    vector<int> path;
    vector<bool> used(nums.size(), false);
    sort(nums.begin(), nums.end());
    dfs(paths, path, nums, used);
    return paths;
}
```

:::
::::

### N 皇后问题

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
void dfs(vector<vector<string>>& paths, vector<string>& path, int row, int n) {
    if (row == n) { // 遍历到最后一行，说明已经找到了一种解法
        paths.push_back(path);
        return;
    }

    // 遍历当前行的每一列，判断当前位置是否可以放置皇后
    for (int col = 0; col < n; col++) {
        // 判断当前位置是否可以放置皇后
        if (path[row][col] == '.') {
            bool flag = true; // flag 为 true 表示当前位置可以放置皇后

            // 判断同一列上是否有皇后
            for (int i = 0; i < row; i++) {
                if (path[i][col] == 'Q') {
                    flag = false;
                    break;
                }
            }

            // 判断同一斜线上是否有皇后
            if (flag) {
                for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
                    if (path[i][j] == 'Q') {
                        flag = false;
                        break;
                    }
                }
            }
            if (flag) {
                for (int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++) {
                    if (path[i][j] == 'Q') {
                        flag = false;
                        break;
                    }
                }
            }

            // 如果当前位置可以放置皇后，则递归调用 dfs 函数，继续向下一行进行遍历
            if (flag) {
                path[row][col] = 'Q';
                dfs(paths, path, row + 1, n);
                path[row][col] = '.';
            }
        }
    }
}

vector<vector<string>> solveNQueens(int n) {
    vector<vector<string>> paths;
    vector<string> path(n, string(n, '.'));
    dfs(paths, path, 0, n);
    return paths;
}
```

:::
::::

### 解数独

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
bool isValid(vector<vector<char>>& board, int row, int col, char num) {
    // 检查当前行或列是否有重复的数字
    for (int i = 0; i < 9; i++) {
        if (board[row][i] == num || board[i][col] == num) {
            return false;
        }
    }

    // 检查 3 x 3 宫格内是否有重复的数字
    int startRow = row - row % 3, startCol = col - col % 3;
    for (int i = startRow; i < startRow + 3; i++) {
        for (int j = startCol; j < startCol + 3; j++) {
            if (board[i][j] == num) {
                return false;
            }
        }
    }

    return true;
}

void dfs(vector<vector<char>>& temp, vector<vector<char>>& board, int row, int col) {
    if (row == 9) {
        temp = board;
        return;
    }

    if (col == 9) {
        dfs(temp, board, row + 1, 0);
        return;
    }

    if (board[row][col] != '.') {
        dfs(temp, board, row, col + 1);
        return;
    }

    for (char num = '1'; num <= '9'; num++) {
        if (isValid(board, row, col, num)) {
            board[row][col] = num;
            dfs(temp, board, row, col + 1);
            board[row][col] = '.'; // 回溯
        }
    }
}

void solveSudoku(vector<vector<char>>& board) {
    // 回溯后 board 会恢复原样，因此需要创建一个临时变量保存 board 的状态
    vector<vector<char>> temp = board;
    dfs(temp, board, 0, 0);
    board = temp;
}
```

:::
::::

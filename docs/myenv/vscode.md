# VS Code

## LeetCode 插件配置方法

```bash
VsCode Error: EACCES: permission denied
```

参考链接：<https://github.com/LeetCode-OpenSource/vscode-leetcode/issues/770>

注释掉 `%appdata%/Code/User/settings.json` 中的 `"leetcode.workspaceFolder"` 字段。

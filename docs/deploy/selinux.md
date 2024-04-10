# 配置 SELinux 安全策略

## 查看违规记录

```bash
cat /var/log/audit/audit.log | grep avc
```

## 添加规则

简单来讲，需要手动创建或修改三个文件：`.te`、`.fc`、`.if`。

参考 <https://github.com/SELinuxProject/refpolicy/wiki/GettingStarted>

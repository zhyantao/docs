# procd

```bash
#!/bin/sh /etc/rc.common

START=90
STOP=10
USE_PROCD=1

# 可选配置组名：SERVICE_OPTS
SERVICE_INSTANCE_NAME="HD_TEST"
SERVICE_OPTS_COMMAND="/etc_rw/HD_TEST/test -e"
SERVICE_OPTS_RESPAWN="3600 5 5"  # respawn_threshold respawn_timeout respawn_retry
# SERVICE_OPTS_USER="admin" # 确保 admin 用户具有执行权限
SERVICE_OPTS_PIDFILE="/var/run/hdbd.pid"

start_service() {
    procd_open_instance ${SERVICE_INSTANCE_NAME}

    # 主命令及参数
    procd_set_param command ${SERVICE_OPTS_COMMAND}

    # 自动重启策略
    procd_set_param respawn ${SERVICE_OPTS_RESPAWN}

    # 用户权限和 PID 文件
    # procd_set_param user ${SERVICE_OPTS_USER}
    procd_set_param pidfile ${SERVICE_OPTS_PIDFILE}

    # 日志输出重定向到 logd
    procd_set_param stdout 1
    procd_set_param stderr 1

    # 设置 TERM 信号等待时间（秒）
    procd_set_param term_timeout 60

    procd_close_instance
}

restart_service() {
    stop
    start
}

reload_service() {
    restart
}
```

参考链接：

- <https://openwrt.org/docs/guide-developer/procd-init-scripts#defining_service_instances>
- <https://openwrt.org/docs/guide-developer/procd-init-script-example>

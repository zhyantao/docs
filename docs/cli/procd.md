# procd

## 开机自启动配置文件

```bash
#!/bin/sh /etc/rc.common

START=90
STOP=10
USE_PROCD=1

# Optional service group name: SERVICE_OPTS
SERVICE_INSTANCE_NAME="HD_TEST"
SERVICE_OPTS_COMMAND="/etc_rw/HD_TEST/test -e"
SERVICE_OPTS_RESPAWN="3600 5 5"  # respawn_threshold respawn_timeout respawn_retry
# SERVICE_OPTS_USER="admin" # Ensure admin user has execution permissions
SERVICE_OPTS_PIDFILE="/var/run/hdbd.pid"

start_service() {
    procd_open_instance ${SERVICE_INSTANCE_NAME}

    # Main command and arguments
    procd_set_param command ${SERVICE_OPTS_COMMAND}

    # Auto-restart policy
    procd_set_param respawn ${SERVICE_OPTS_RESPAWN}

    # User permission and PID file
    # procd_set_param user ${SERVICE_OPTS_USER}
    procd_set_param pidfile ${SERVICE_OPTS_PIDFILE}

    # Redirect stdout and stderr to logd
    procd_set_param stdout 1
    procd_set_param stderr 1

    # Set TERM signal wait timeout (in seconds)
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

## 使能开机自启动

```bash
/etc/init.d/autostart_demo enable
/etc/init.d/autostart_demo start
sync
reboot
```

## 参考链接

- <https://openwrt.org/docs/guide-developer/procd-init-scripts#defining_service_instances>
- <https://openwrt.org/docs/guide-developer/procd-init-script-example>

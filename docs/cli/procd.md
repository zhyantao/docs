# procd

```bash
#!/bin/sh /etc/rc.common

START=90
STOP=01
USE_PROCD=1

start_service() {
         procd_open_instance [instance_name]
         
         # 设置服务的主命令和参数，确保服务以前台模式运行。
         procd_set_param command /sbin/your_service_daemon -b -a --foo
         # 追加额外的命令行参数到服务启动命令中。
         procd_append_param command -bar 42

         # 配置进程自动重启策略：
         # 如果进程在 respawn_threshold 时间内退出，则认为是异常退出，并尝试重新启动。
         # 如果连续5次尝试重启失败，则停止尝试并终止服务。
         # 如果进程正常运行超过 respawn_threshold 时间后退出，则无论退出码如何都会无条件重启。
         # 注意：这是直接重启进程，而不是基于失败检测的重启机制。
         procd_set_param respawn ${respawn_threshold:-3600} ${respawn_timeout:-5} ${respawn_retry:-5}

         # 设置环境变量传递给服务进程。
         procd_set_param env SOME_VARIABLE=funtimes
         # 设置进程的资源限制，例如核心文件大小为无限大。
         procd_set_param limits core="unlimited"
         # 指定配置文件，当此文件发生变化时，将触发服务重新加载或重启。
         procd_set_param file /var/etc/your_service.conf
         # 监控网络设备变化，当指定设备的 ifindex 发生变化时，触发服务操作。
         procd_set_param netdev dev
         # 监控特定数据的变化，当这些数据发生更改时，触发服务操作。
         procd_set_param data name=value ...
         # 将服务的标准输出重定向到系统日志服务 logd。
         procd_set_param stdout 1
         # 将服务的标准错误输出也重定向到系统日志服务 logd。
         procd_set_param stderr 1
         # 指定服务运行的用户身份，这里设置为 nobody 用户。
         procd_set_param user nobody
         # 设置 pid 文件路径，在服务启动时创建并在服务停止时删除该文件。
         procd_set_param pidfile /var/run/somefile.pid
         # 设置发送 SIGKILL 信号前的等待时间，单位为秒。
         procd_set_param term_timeout 60

         procd_close_instance
}
```

参考链接：

- <https://openwrt.org/docs/guide-developer/procd-init-scripts#defining_service_instances>
- <https://openwrt.org/docs/guide-developer/procd-init-script-example>

# procd

```bash
#!/bin/sh /etc/rc.common

START=90
STOP=01
USE_PROCD=1

start_service() {
         procd_open_instance [instance_name]
         procd_set_param command /sbin/your_service_daemon -b -a --foo # service executable that has to run in **foreground**.
         procd_append_param command -bar 42 # append command parameters

         # respawn automatically if something died, be careful if you have an alternative process supervisor
         # if process exits sooner than respawn_threshold, it is considered crashed and after 5 retries the service is stopped
         # if process finishes later than respawn_threshold, it is restarted unconditionally, regardless of error code
         # notice that this is literal respawning of the process, not in a respawn-on-failure sense
         procd_set_param respawn ${respawn_threshold:-3600} ${respawn_timeout:-5} ${respawn_retry:-5}

         procd_set_param env SOME_VARIABLE=funtimes  # pass environment variables to your process
         procd_set_param limits core="unlimited"  # If you need to set ulimit for your process
         procd_set_param file /var/etc/your_service.conf # /etc/init.d/your_service reload will restart the daemon when these files have changed
         procd_set_param netdev dev # likewise, but for when dev's ifindex changes.
         procd_set_param data name=value ... # likewise, but for when this data changes.
         procd_set_param stdout 1 # forward stdout of the command to logd
         procd_set_param stderr 1 # same for stderr
         procd_set_param user nobody # run service as user nobody
         procd_set_param pidfile /var/run/somefile.pid # write a pid file on instance start and remove it on stop
         procd_set_param term_timeout 60 # wait before sending SIGKILL
         procd_close_instance
}
```

参考链接：

- <https://openwrt.org/docs/guide-developer/procd-init-scripts#defining_service_instances>
- <https://openwrt.org/docs/guide-developer/procd-init-script-example>

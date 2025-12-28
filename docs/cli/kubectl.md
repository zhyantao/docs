# kubectl

本页面提供了常用的 `kubectl` 命令和选项的快速参考。

## Kubectl 自动补全

### BASH

```bash
# 在当前 bash 会话中启用 kubectl 自动补全（需先安装 bash-completion）
source <(kubectl completion bash)

# 将自动补全永久添加到 bash 配置中
echo "source <(kubectl completion bash)" >> ~/.bashrc
```

可以为 `kubectl` 设置简短的别名并启用补全：

```bash
alias k=kubectl
complete -o default -F __start_kubectl k
```

### ZSH

```bash
# 在当前 zsh 会话中启用 kubectl 自动补全
source <(kubectl completion zsh)

# 将自动补全永久添加到 zsh 配置中
echo '[[ $commands[kubectl] ]] && source <(kubectl completion zsh)' >> ~/.zshrc
```

### 关于 `--all-namespaces` 的提示

`--all-namespaces` 是常用参数，其简写形式为：

`kubectl -A`

## Kubectl 上下文与配置

设置 `kubectl` 与 Kubernetes 集群通信的相关配置。  
有关配置文件详情，请参阅 [使用 kubeconfig 进行跨集群认证](https://kubernetes.io/zh-cn/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)。

```bash
kubectl config view # 显示合并后的 kubeconfig 配置

# 同时使用多个 kubeconfig 文件查看合并配置
KUBECONFIG=~/.kube/config:~/.kube/kubconfig2 kubectl config view

# 获取 e2e 用户的密码
kubectl config view -o jsonpath='{.users[?(@.name=="e2e")].user.password}'

kubectl config view -o jsonpath='{.users[].name}'    # 显示第一个用户名
kubectl config view -o jsonpath='{.users[*].name}'   # 显示所有用户名
kubectl config get-contexts                          # 列出所有上下文
kubectl config current-context                       # 显示当前上下文
kubectl config use-context my-cluster-name           # 切换到指定上下文

kubectl config set-cluster my-cluster-name           # 配置集群信息

# 为集群设置代理服务器地址
kubectl config set-cluster my-cluster-name --proxy-url=my-proxy-url

# 添加使用基础认证的用户凭据
kubectl config set-credentials kubeuser/foo.kubernetes.com --username=kubeuser --password=kubepassword

# 在当前上下文中设置默认命名空间
kubectl config set-context --current --namespace=ggckad-s2

# 创建新上下文并切换到该上下文
kubectl config set-context gce --user=cluster-admin --namespace=foo && kubectl config use-context gce

kubectl config unset users.foo                       # 删除用户配置

# 上下文和命名空间的快捷别名（适用于 bash 及兼容 shell）
alias kx='f() { [ "$1" ] && kubectl config use-context $1 || kubectl config current-context ; } ; f'
alias kn='f() { [ "$1" ] && kubectl config set-context --current --namespace $1 || kubectl config view --minify | grep namespace | cut -d" " -f6 ; } ; f'
```

## Kubectl Apply

`apply` 命令通过声明式配置文件管理 Kubernetes 应用资源，是生产环境推荐的管理方式。  
更多信息请参阅 [Kubectl 文档](https://kubectl.docs.kubernetes.io/zh/)。

## 创建资源

Kubernetes 资源配置支持 YAML（`.yaml`、`.yml`）或 JSON（`.json`）格式。

```bash
kubectl apply -f ./my-manifest.yaml           # 创建资源
kubectl apply -f ./my1.yaml -f ./my2.yaml     # 使用多个文件创建
kubectl apply -f ./dir                        # 创建目录下所有清单定义的资源
kubectl apply -f https://git.io/vPieo         # 通过 URL 创建资源
kubectl create deployment nginx --image=nginx # 创建单实例 nginx Deployment

# 创建打印 “Hello World” 的 Job
kubectl create job hello --image=busybox:1.28 -- echo "Hello World"

# 创建每分钟打印 “Hello World” 的 CronJob
kubectl create cronjob hello --image=busybox:1.28 --schedule="*/1 * * * *" -- echo "Hello World"

kubectl explain pods                          # 查看 Pod 资源配置说明

# 通过标准输入创建多个 YAML 对象
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: busybox-sleep
spec:
  containers:
  - name: busybox
    image: busybox:1.28
    args:
    - sleep
    - "1000000"
---
apiVersion: v1
kind: Pod
metadata:
  name: busybox-sleep-less
spec:
  containers:
  - name: busybox
    image: busybox:1.28
    args:
    - sleep
    - "1000"
EOF

# 创建包含多个键的 Secret
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  password: $(echo -n "s33msi4" | base64 -w0)
  username: $(echo -n "jane" | base64 -w0)
EOF
```

## 查看与检索资源

```bash
# 基础 get 命令
kubectl get services                          # 列出当前命名空间的所有 Service
kubectl get pods --all-namespaces             # 列出所有命名空间的 Pod
kubectl get pods -o wide                      # 显示 Pod 详细信息
kubectl get deployment my-dep                 # 查看特定 Deployment
kubectl get pod my-pod -o yaml                # 以 YAML 格式输出 Pod 配置

# 详细描述资源
kubectl describe nodes my-node
kubectl describe pods my-pod

# 按名称排序列出 Service
kubectl get services --sort-by=.metadata.name

# 按重启次数排序列出 Pod
kubectl get pods --sort-by='.status.containerStatuses[0].restartCount'

# 按容量排序列出持久卷（PV）
kubectl get pv --sort-by=.spec.capacity.storage

# 获取带有 app=cassandra 标签的 Pod 的 version 标签
kubectl get pods --selector=app=cassandra -o jsonpath='{.items[*].metadata.labels.version}'

# 检索键名包含点号（如 ca.crt）的 ConfigMap 值
kubectl get configmap myconfig -o jsonpath='{.data.ca\.crt}'

# 获取 Secret 中键名包含连字符的 base64 编码值
kubectl get secret my-secret --template='{{index .data "key-name-with-dashes"}}'

# 获取所有工作节点（排除控制平面节点）
kubectl get node --selector='!node-role.kubernetes.io/control-plane'

# 获取当前命名空间中处于 Running 状态的 Pod
kubectl get pods --field-selector=status.phase=Running

# 获取所有节点的 ExternalIP 地址
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="ExternalIP")].address}'

# 列出属于某 ReplicationController 的 Pod 名称（使用 jq 处理复杂 JSON）
sel=${$(kubectl get rc my-rc --output=json | jq -j '.spec.selector | to_entries | .[] | "\(.key)=\(.value),"')%?}
echo $(kubectl get pods --selector=$sel --output=jsonpath={.items..metadata.name})

# 显示所有 Pod 的标签
kubectl get pods --show-labels

# 检查节点就绪状态
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}' \
 && kubectl get nodes -o jsonpath="$JSONPATH" | grep "Ready=True"

# 解码 Secret 内容
kubectl get secret my-secret -o go-template='{{range $k,$v := .data}}{{"### "}}{{$k}}{{"\n"}}{{$v|base64decode}}{{"\n\n"}}{{end}}'

# 列出被 Pod 使用的所有 Secret
kubectl get pods -o json | jq '.items[].spec.containers[].env[]?.valueFrom.secretKeyRef.name' | grep -v null | sort | uniq

# 列出所有 Pod 中初始化容器的容器 ID（便于清理时排除初始化容器）
kubectl get pods --all-namespaces -o jsonpath='{range .items[*].status.initContainerStatuses[*]}{.containerID}{"\n"}{end}' | cut -d/ -f3

# 按时间排序查看事件
kubectl get events --sort-by=.metadata.creationTimestamp

# 对比当前集群状态与应用清单后的差异
kubectl diff -f ./my-manifest.yaml

# 生成节点键名的点分隔路径树（用于定位复杂 JSON 结构）
kubectl get nodes -o json | jq -c 'paths|join(".")'

# 为所有 Pod 生成环境变量（假设容器支持 env 命令）
for pod in $(kubectl get po --output=jsonpath={.items..metadata.name}); do echo $pod && kubectl exec -it $pod -- env; done

# 获取 Deployment 的 status 子资源
kubectl get deployment nginx-deployment --subresource=status
```

## 更新资源

```bash
kubectl set image deployment/frontend www=image:v2               # 更新 Deployment 的容器镜像
kubectl rollout history deployment/frontend                      # 查看 Deployment 发布历史
kubectl rollout undo deployment/frontend                         # 回滚到上一版本
kubectl rollout undo deployment/frontend --to-revision=2         # 回滚到指定版本
kubectl rollout status -w deployment/frontend                    # 监控滚动更新状态
kubectl rollout restart deployment/frontend                      # 重启 Deployment

cat pod.json | kubectl replace -f -                              # 通过标准输入替换 Pod

# 强制替换（删除后重建，会导致服务中断）
kubectl replace --force -f ./pod.json

# 为多副本 nginx RC 创建 Service，端口映射 80:8000
kubectl expose rc nginx --port=80 --target-port=8000

# 更新 Pod 镜像版本
kubectl get pod mypod -o yaml | sed 's/\(image: myimage\):.*$/\1:v4/' | kubectl replace -f -

kubectl label pods my-pod new-label=awesome                      # 添加标签
kubectl annotate pods my-pod icon-url=http://goo.gl/XXBTWq       # 添加注解
kubectl autoscale deployment foo --min=2 --max=10                # 设置 Deployment 自动扩缩容
```

## 部分更新资源

```bash
# 将节点标记为不可调度
kubectl patch node k8s-node-1 -p '{"spec":{"unschedulable":true}}'

# 更新 Pod 中指定容器的镜像
kubectl patch pod valid-pod -p '{"spec":{"containers":[{"name":"kubernetes-serve-hostname","image":"new image"}]}}'

# 使用 JSON patch 更新容器镜像
kubectl patch pod valid-pod --type='json' -p='[{"op": "replace", "path": "/spec/containers/0/image", "value":"new image"}]'

# 使用 JSON patch 移除容器的存活探针
kubectl patch deployment valid-deployment --type json -p='[{"op": "remove", "path": "/spec/template/spec/containers/0/livenessProbe"}]'

# 向数组添加元素
kubectl patch sa default --type='json' -p='[{"op": "add", "path": "/secrets/1", "value": {"name": "whatever" } }]'

# 通过 scale 子资源更新副本数
kubectl patch deployment nginx-deployment --subresource='scale' --type='merge' -p '{"spec":{"replicas":2}}'
```

## 编辑资源

使用默认编辑器或指定编辑器修改资源配置。

```bash
kubectl edit svc/docker-registry                      # 编辑 Service
KUBE_EDITOR="nano" kubectl edit svc/docker-registry   # 使用指定编辑器
```

## 扩缩容资源

```bash
kubectl scale --replicas=3 rs/foo                                 # 伸缩副本集
kubectl scale --replicas=3 -f foo.yaml                            # 伸缩配置文件中的资源
kubectl scale --current-replicas=2 --replicas=3 deployment/mysql  # 基于当前副本数伸缩
kubectl scale --replicas=5 rc/foo rc/bar rc/baz                   # 伸缩多个副本控制器
```

## 删除资源

```bash
kubectl delete -f ./pod.json                                      # 删除配置文件定义的资源
kubectl delete pod,service baz foo                                # 删除指定 Pod 和 Service
kubectl delete pods,services -l name=myLabel                      # 删除带有指定标签的资源
kubectl -n my-ns delete pod,svc --all                             # 删除命名空间内所有 Pod 和 Service
# 使用 awk 模式匹配删除 Pod
kubectl get pods -n mynamespace --no-headers=true | awk '/pattern1|pattern2/{print $1}' | xargs kubectl delete -n mynamespace pod
```

## 与运行中的 Pod 交互

```bash
kubectl logs my-pod                                 # 查看 Pod 日志
kubectl logs -l name=myLabel                        # 查看带指定标签 Pod 的日志
kubectl logs my-pod --previous                      # 查看上一个容器实例的日志
kubectl logs my-pod -c my-container                 # 查看指定容器的日志
kubectl logs -l name=myLabel -c my-container        # 查看带标签 Pod 中指定容器的日志
kubectl logs my-pod -c my-container --previous      # 查看指定容器上一个实例的日志
kubectl logs -f my-pod                              # 实时流式输出日志
kubectl logs -f my-pod -c my-container              # 实时流式输出指定容器日志
kubectl logs -f -l name=myLabel --all-containers    # 实时输出带标签 Pod 的所有容器日志
kubectl run -i --tty busybox --image=busybox:1.28 -- sh  # 以交互模式运行 Pod
kubectl run nginx --image=nginx -n mynamespace      # 在指定命名空间运行 Pod
kubectl run nginx --image=nginx --dry-run=client -o yaml > pod.yaml
                                                    # 生成 Pod 配置并保存到文件

kubectl attach my-pod -i                            # 附加到运行中的容器
kubectl port-forward my-pod 5000:6000               # 端口转发到 Pod
kubectl exec my-pod -- ls /                         # 在 Pod 中执行命令
kubectl exec --stdin --tty my-pod -- /bin/sh        # 进入 Pod 的交互式 Shell
kubectl exec my-pod -c my-container -- ls /         # 在 Pod 的指定容器中执行命令
kubectl top pod POD_NAME --containers               # 显示 Pod 及其容器的资源使用
kubectl top pod POD_NAME --sort-by=cpu              # 按 CPU 使用率排序显示 Pod 指标
```

## 复制文件和目录

```bash
kubectl cp /tmp/foo_dir my-pod:/tmp/bar_dir            # 复制本地目录到 Pod
kubectl cp /tmp/foo my-pod:/tmp/bar -c my-container    # 复制本地文件到 Pod 的指定容器
kubectl cp /tmp/foo my-namespace/my-pod:/tmp/bar       # 复制到指定命名空间的 Pod
kubectl cp my-namespace/my-pod:/tmp/foo /tmp/bar       # 从 Pod 复制到本地

# 使用 tar 进行高级复制（当容器内无 tar 时使用）
tar cf - /tmp/foo | kubectl exec -i -n my-namespace my-pod -- tar xf - -C /tmp/bar
kubectl exec -n my-namespace my-pod -- tar cf - /tmp/foo | tar xf - -C /tmp/bar
```

{{< note >}}
`kubectl cp` 要求容器镜像中包含 `tar` 可执行文件。如果不存在，可考虑使用 `kubectl exec` 配合 `tar` 进行替代。
{{< /note >}}

## 与 Deployments 和 Services 交互

```bash
kubectl logs deploy/my-deployment                         # 查看 Deployment 的 Pod 日志
kubectl logs deploy/my-deployment -c my-container         # 查看 Deployment 指定容器的日志

kubectl port-forward svc/my-service 5000                  # 转发到 Service 的默认端口
kubectl port-forward svc/my-service 5000:my-service-port  # 转发到 Service 的指定端口

kubectl port-forward deploy/my-deployment 5000:6000       # 转发到 Deployment 的 Pod 端口
kubectl exec deploy/my-deployment -- ls                   # 在 Deployment 的 Pod 中执行命令
```

## 与节点和集群交互

```bash
kubectl cordon my-node                                                # 将节点设为不可调度
kubectl drain my-node                                                 # 清空节点（维护前准备）
kubectl uncordon my-node                                              # 将节点设为可调度
kubectl top node my-node                                              # 显示节点资源指标
kubectl cluster-info                                                  # 显示集群信息
kubectl cluster-info dump                                             # 导出集群状态
kubectl cluster-info dump --output-directory=/path/to/cluster-state   # 导出集群状态到目录

# 查看节点污点
kubectl get nodes -o='custom-columns=NodeName:.metadata.name,TaintKey:.spec.taints[*].key,TaintValue:.spec.taints[*].value,TaintEffect:.spec.taints[*].effect'

# 添加或更新节点污点
kubectl taint nodes foo dedicated=special-user:NoSchedule
```

### 资源类型

列出所有支持的资源类型及其缩写、API 组、命名空间作用域和 Kind。

```bash
kubectl api-resources
```

其他 API 资源查询操作：

```bash
kubectl api-resources --namespaced=true      # 仅显示命名空间作用域的资源
kubectl api-resources --namespaced=false     # 仅显示集群作用域的资源
kubectl api-resources -o name                # 仅显示资源名称
kubectl api-resources -o wide                # 显示详细信息（wide 格式）
kubectl api-resources --verbs=list,get       # 支持 list 和 get 操作的资源
kubectl api-resources --api-group=extensions # 指定 API 组的资源
```

### 输出格式

使用 `-o`（`--output`）参数指定输出格式。

| 输出格式                            | 描述                           |
| ----------------------------------- | ------------------------------ |
| `-o=custom-columns=<spec>`          | 自定义列输出                   |
| `-o=custom-columns-file=<filename>` | 从文件读取自定义列模板         |
| `-o=json`                           | JSON 格式输出                  |
| `-o=jsonpath=<template>`            | 输出 JSONPath 表达式定义的字段 |
| `-o=jsonpath-file=<filename>`       | 从文件读取 JSONPath 表达式     |
| `-o=name`                           | 仅输出资源名称                 |
| `-o=wide`                           | 扩展信息输出（包含节点等）     |
| `-o=yaml`                           | YAML 格式输出                  |

`-o=custom-columns` 示例：

```bash
# 列出所有 Pod 使用的镜像
kubectl get pods -A -o=custom-columns='DATA:spec.containers[*].image'

# 按 Pod 分组列出默认命名空间的镜像
kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,IMAGE:.spec.containers[*].image"

# 排除指定镜像的其他所有镜像
kubectl get pods -A -o=custom-columns='DATA:spec.containers[?(@.image!="registry.k8s.io/coredns:1.6.2")].image'

# 输出 metadata 下所有字段
kubectl get pods -A -o=custom-columns='DATA:metadata.*'
```

更多示例请参阅 [kubectl 参考文档](https://kubernetes.io/zh-cn/docs/reference/kubectl/#custom-columns)。

### Kubectl 日志输出级别

通过 `-v` 或 `--v` 加数字控制日志详细程度。

| 级别    | 描述                               |
| ------- | ---------------------------------- |
| `--v=0` | 始终对运维人员可见的基本信息       |
| `--v=1` | 默认推荐级别，无冗余信息           |
| `--v=2` | 服务状态和重要变更信息             |
| `--v=3` | 系统状态变化的扩展信息             |
| `--v=4` | 调试级别信息                       |
| `--v=5` | 跟踪级别详细信息                   |
| `--v=6` | 显示请求的资源                     |
| `--v=7` | 显示 HTTP 请求头                   |
| `--v=8` | 显示 HTTP 请求内容                 |
| `--v=9` | 显示完整的 HTTP 请求内容（不截断） |

## 延伸阅读

- [kubectl 概述](https://kubernetes.io/zh-cn/docs/reference/kubectl/) 和 [JsonPath 指南](https://kubernetes.io/zh-cn/docs/reference/kubectl/jsonpath)
- [kubectl 选项](https://kubernetes.io/zh-cn/docs/reference/kubectl/kubectl/)
- [kubectl 使用约定](https://kubernetes.io/zh-cn/docs/reference/kubectl/conventions/)（用于编写可复用脚本）
- 社区提供的其他 [kubectl 备忘单](https://github.com/dennyzhang/cheatsheet-kubernetes-A4)

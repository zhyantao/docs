# Linux 驱动开发完整指南：从入门到实践

## 一、驱动开发核心概念与关系

### 1.1 四大组件的关系图

```text
   ┌─────────────────────────────────────────┐
   │          用户空间应用程序
   └─────────────┬───────────────────────────┘
                 │ 系统调用 (open/read/write)
   ┌─────────────▼───────────────────────────┐
   │          字符设备驱动框架                 ← 提供标准接口
   ├─────────────────────────────────────────┤
   │          GPIO 子系统                     ← 抽象硬件操作
   ├─────────────────────────────────────────┤
   │          中断处理机制                     ← 处理异步事件
   └─────────────┬───────────────────────────┘
                 │ 硬件寄存器操作
   ┌─────────────▼───────────────────────────┐
   │           设备树 (DTS)                   ← 硬件描述层
   └─────────────┬───────────────────────────┘
                 │ 描述硬件连接和配置
   ┌─────────────▼───────────────────────────┐
   │           物理硬件
   └─────────────────────────────────────────┘
```

### 1.2 组件间的关系说明

| 组件          | 角色       | 依赖关系               | 修改顺序 |
| ------------- | ---------- | ---------------------- | -------- |
| **设备树**    | 硬件描述层 | 独立存在，描述硬件连接 | 第 1 步  |
| **GPIO 驱动** | 硬件抽象层 | 依赖设备树获取硬件信息 | 第 2 步  |
| **中断驱动**  | 事件处理层 | 依赖 GPIO 驱动和硬件   | 第 3 步  |
| **字符驱动**  | 接口提供层 | 依赖所有底层组件       | 第 4 步  |

### 1.3 开发顺序逻辑

:::{mermaid}
graph TD
A[分析硬件原理图] --> B[编写设备树节点]
B --> C[实现 GPIO 操作]
C --> D[添加中断支持]
D --> E[构建字符设备接口]
E --> F[编写测试应用]
F --> G[调试与优化]
:::

## 二、完整的驱动开发步骤

### 2.1 分析硬件与规划

#### 硬件分析要点

```bash
# 1. 查看硬件连接（以 LED 为例）
LED1 → GPIOA.10 (低电平点亮)
BUTTON1 → GPIOC.13 (按下为低电平)

# 2. 确定所需资源
- GPIO：2 个（输入和输出各 1）
- 中断：1 个（按键中断）
- 内存：少量（用于状态缓存）

# 3. 设计数据结构
struct led_button_device {
    // GPIO
    struct gpio_desc *led_gpio;
    struct gpio_desc *button_gpio;

    // 中断
    int irq;

    // 同步机制
    struct mutex lock;
    wait_queue_head_t wait_queue;

    // 设备状态
    atomic_t button_pressed;
    u8 led_state;
};
```

#### 项目规划文件

```bash
# project_plan.txt
硬件：
  - LED: GPIOA.10, 低电平有效
  - 按键: GPIOC.13, 下降沿触发

软件需求：
  - 字符设备：/dev/led_button
  - 功能：
      1. 控制 LED 开关
      2. 读取按键状态
      3. 支持阻塞/非阻塞读取
      4. 支持 poll 和异步通知

设备树节点：
  - 名称：led_button
  - 兼容性：custom,led-button-v1
  - 属性：led-gpio, button-gpio
```

### 2.2 设备树配置

#### 2.2.1 创建设备树节点

```dts
// custom-led-button.dts - 设备树源文件
/dts-v1/;
/plugin/;  // 声明为设备树覆盖（可动态加载）

/**
 * 设备树覆盖片段
 * @fragment@0: 第一个片段
 * @target-path: 目标路径，这里挂载到根节点
 */
&{/} {
    // 在根节点下添加我们的设备
    led_button_device {
        /**
         * compatible 属性：驱动匹配的关键
         * 格式："制造商,设备型号"
         * 可以有多个，按优先级排序
         */
        compatible = "custom,led-button-v1", "generic-led-button";

        /**
         * status 属性：设备状态
         * "okay" - 启用设备
         * "disabled" - 禁用设备
         * "fail" - 设备故障
         * "fail-sss" - 特定故障
         */
        status = "okay";

        /**
         * LED GPIO 配置
         * &gpioa: 引用 GPIOA 控制器节点
         * 10: 引脚编号
         * GPIO_ACTIVE_LOW: 低电平有效
         */
        led-gpios = <&gpioa 10 GPIO_ACTIVE_LOW>;

        /**
         * 按键 GPIO 配置
         * GPIOC.13, 高电平有效
         * 添加中断属性
         */
        button-gpios = <&gpioc 13 (GPIO_ACTIVE_HIGH | GPIO_PULL_DOWN)>;

        /**
         * 中断配置
         * interrupt-parent: 中断父控制器
         * interrupts: 中断号和触发方式
         * IRQ_TYPE_EDGE_FALLING: 下降沿触发
         * IRQ_TYPE_EDGE_RISING: 上升沿触发
         * IRQ_TYPE_EDGE_BOTH: 双边沿触发
         * IRQ_TYPE_LEVEL_HIGH: 高电平触发
         * IRQ_TYPE_LEVEL_LOW: 低电平触发
         */
        interrupt-parent = <&gpioc>;
        interrupts = <13 IRQ_TYPE_EDGE_FALLING>;

        /**
         * 自定义属性示例
         * 驱动可以根据需要解析这些属性
         */
        debounce-interval = <20>;    // 消抖时间 20ms
        default-brightness = <128>;  // 默认亮度 50%

        /**
         * 标签和别名（可选）
         * 标签: 在其他地方可以用 &led_button 引用
         * 别名: 在 /proc/device-tree/aliases 中创建快捷方式
         */
        label = "user_button";
        linux,name = "my_button";
    };
};
```

#### 2.2.2 编译和加载设备树

```bash
#!/bin/bash
# compile_dts.sh - 设备树编译脚本

# 1. 编译设备树覆盖
echo "编译设备树..."
dtc -@ -I dts -O dtb -o custom-led-button.dtbo custom-led-button.dts

# 2. 检查语法
echo "检查设备树语法..."
dtc -I dtb -O dts custom-led-button.dtbo > /dev/null

# 3. 加载到开发板（方法 1：动态加载）
echo "加载设备树覆盖..."
mkdir -p /config/device-tree/overlays/led_button
cp custom-led-button.dtbo /config/device-tree/overlays/led_button/dtbo

# 4. 验证加载结果
echo "验证设备树节点..."
if [ -d /proc/device-tree/led_button_device ]; then
    echo "✅ 设备树节点创建成功"

    # 查看节点属性
    echo "设备树节点信息："
    cat /proc/device-tree/led_button_device/compatible
    echo ""
    hexdump -C /proc/device-tree/led_button_device/led-gpios
else
    echo "❌ 设备树节点创建失败"
fi

# 5. 或者方法 2：替换完整设备树
echo "方法 2：替换完整设备树"
# a. 反编译当前设备树
dtc -I dtb -O dts /boot/board.dtb > current.dts

# b. 添加我们的节点到 current.dts
# c. 重新编译
dtc -I dts -O dtb -o new-board.dtb current.dts

# d. 替换并重启
# cp new-board.dtb /boot/board.dtb
# reboot
```

#### 2.2.3 设备树调试技巧

```bash
# 查看系统中所有设备树节点
find /proc/device-tree -type f -name "*" | sort

# 查看特定节点
ls -la /proc/device-tree/led_button_device/

# 查看节点属性
cat /proc/device-tree/led_button_device/compatible
cat /proc/device-tree/led_button_device/status

# 查看 GPIO 属性（二进制格式）
hexdump -C /proc/device-tree/led_button_device/led-gpios

# 使用 oftree 工具（如果安装）
oftree -p /proc/device-tree -f led_button_device

# 动态修改属性（调试用）
echo 1 > /proc/device-tree/led_button_device/status
```

### 2.3 实现 GPIO 驱动

#### 2.3.1 驱动源码：gpio_core.c

```cpp
// gpio_core.c - GPIO 核心操作实现
#include <linux/module.h>
#include <linux/init.h>
#include <linux/gpio/consumer.h>
#include <linux/err.h>
#include <linux/slab.h>
#include <linux/of.h>
#include <linux/platform_device.h>

/**
 * struct gpio_control - GPIO 控制结构体
 * 封装 GPIO 操作相关的数据和状态
 */
struct gpio_control {
    struct device *dev;              // 关联的设备
    struct gpio_desc *led_gpio;      // LED GPIO 描述符
    struct gpio_desc *button_gpio;   // 按键 GPIO 描述符
    int led_state;                   // LED 当前状态
    int button_state;                // 按键当前状态
    struct mutex lock;               // 保护并发访问
};

/**
 * gpio_setup() - 初始化 GPIO
 * @dev: 设备指针
 * @gc: GPIO 控制结构体指针
 *
 * 从设备树获取 GPIO 配置并进行初始化
 * 返回值：成功返回 0，失败返回错误码
 */
static int gpio_setup(struct device *dev, struct gpio_control *gc)
{
    int ret = 0;

    pr_info("%s: 开始初始化 GPIO\n", __func__);

    // 1. 获取 LED GPIO
    gc->led_gpio = devm_gpiod_get(dev, "led", GPIOD_OUT_LOW);
    if (IS_ERR(gc->led_gpio)) {
        ret = PTR_ERR(gc->led_gpio);
        dev_err(dev, "无法获取 LED GPIO: %d\n", ret);

        // 尝试备用名称
        gc->led_gpio = devm_gpiod_get(dev, "led-gpio", GPIOD_OUT_LOW);
        if (IS_ERR(gc->led_gpio)) {
            ret = PTR_ERR(gc->led_gpio);
            dev_err(dev, "无法获取 LED GPIO（备用名）: %d\n", ret);
            return ret;
        }
    }

    // 2. 获取按键 GPIO
    gc->button_gpio = devm_gpiod_get(dev, "button", GPIOD_IN);
    if (IS_ERR(gc->button_gpio)) {
        ret = PTR_ERR(gc->button_gpio);
        dev_err(dev, "无法获取按键 GPIO: %d\n", ret);
        return ret;
    }

    // 3. 配置 GPIO 属性（可选）
    // 设置 LED GPIO 标签
    gpiod_set_consumer_name(gc->led_gpio, "user_led");

    // 设置按键 GPIO 标签
    gpiod_set_consumer_name(gc->button_gpio, "user_button");

    // 4. 初始化状态
    gc->led_state = 0;      // 初始关闭
    gc->button_state = gpiod_get_value(gc->button_gpio);

    // 5. 初始化互斥锁
    mutex_init(&gc->lock);

    dev_info(dev, "GPIO 初始化成功\n");
    dev_info(dev, "  LED GPIO: %s, 状态: %s\n",
             desc_to_gpio(gc->led_gpio) ? "有效" : "无效",
             gc->led_state ? "亮" : "灭");
    dev_info(dev, "  按键 GPIO: %s, 状态: %s\n",
             desc_to_gpio(gc->button_gpio) ? "有效" : "无效",
             gc->button_state ? "按下" : "释放");

    return 0;
}

/**
 * gpio_led_set() - 控制 LED
 * @gc: GPIO 控制结构体指针
 * @state: 目标状态 (1=亮, 0=灭)
 *
 * 线程安全的 LED 控制函数
 */
int gpio_led_set(struct gpio_control *gc, int state)
{
    int ret = 0;

    if (!gc || !gc->led_gpio) {
        pr_err("%s: 无效参数或 GPIO 未初始化\n", __func__);
        return -EINVAL;
    }

    mutex_lock(&gc->lock);

    if (gc->led_state != state) {
        /**
         * gpiod_set_value() - 设置 GPIO 输出值
         * @gpio: GPIO 描述符
         * @value: 输出值 (0/1)
         * 注意：对于 ACTIVE_LOW 的 GPIO，值会反转
         */
        gpiod_set_value(gc->led_gpio, state);
        gc->led_state = state;

        dev_dbg(gc->dev, "LED 状态改变: %s\n", state ? "亮" : "灭");
    }

    mutex_unlock(&gc->lock);
    return ret;
}

/**
 * gpio_led_get() - 获取 LED 状态
 * @gc: GPIO 控制结构体指针
 *
 * 返回 LED 当前状态
 */
int gpio_led_get(struct gpio_control *gc)
{
    int state;

    if (!gc) {
        return -EINVAL;
    }

    mutex_lock(&gc->lock);
    state = gc->led_state;
    mutex_unlock(&gc->lock);

    return state;
}

/**
 * gpio_button_get() - 获取按键状态
 * @gc: GPIO 控制结构体指针
 *
 * 读取 GPIO 引脚的实际电平
 */
int gpio_button_get(struct gpio_control *gc)
{
    int state;

    if (!gc || !gc->button_gpio) {
        return -EINVAL;
    }

    /**
     * gpiod_get_value() - 读取 GPIO 输入值
     * @gpio: GPIO 描述符
     * 返回值：GPIO 当前电平 (0/1)
     */
    state = gpiod_get_value(gc->button_gpio);

    mutex_lock(&gc->lock);
    gc->button_state = state;
    mutex_unlock(&gc->lock);

    return state;
}

/**
 * gpio_led_toggle() - 翻转 LED 状态
 * @gc: GPIO 控制结构体指针
 */
int gpio_led_toggle(struct gpio_control *gc)
{
    int new_state;

    if (!gc) {
        return -EINVAL;
    }

    mutex_lock(&gc->lock);
    new_state = !gc->led_state;

    gpiod_set_value(gc->led_gpio, new_state);
    gc->led_state = new_state;

    dev_dbg(gc->dev, "LED 翻转: %s\n", new_state ? "亮" : "灭");

    mutex_unlock(&gc->lock);
    return new_state;
}

/**
 * gpio_cleanup() - 清理 GPIO 资源
 * @gc: GPIO 控制结构体指针
 *
 * 注意：我们使用 devm_gpiod_get() 申请的资源会自动释放
 * 这里只需要销毁互斥锁
 */
void gpio_cleanup(struct gpio_control *gc)
{
    if (gc) {
        mutex_destroy(&gc->lock);
        dev_info(gc->dev, "GPIO 资源已清理\n");
    }
}

EXPORT_SYMBOL(gpio_setup);
EXPORT_SYMBOL(gpio_led_set);
EXPORT_SYMBOL(gpio_led_get);
EXPORT_SYMBOL(gpio_button_get);
EXPORT_SYMBOL(gpio_led_toggle);
EXPORT_SYMBOL(gpio_cleanup);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("通用 GPIO 控制模块");
MODULE_AUTHOR("Driver Developer");
```

#### 2.3.2 GPIO 调试方法

```bash
# 1. 查看 GPIO 状态
cat /sys/kernel/debug/gpio

# 2. 使用 GPIO Sysfs 接口（旧方式）
# 导出 GPIO
echo 10 > /sys/class/gpio/export
echo 13 > /sys/class/gpio/export

# 查看 GPIO 信息
ls /sys/class/gpio/gpio10/
cat /sys/class/gpio/gpio10/direction
cat /sys/class/gpio/gpio10/value

# 3. 使用 libgpiod 工具（新方式）
# 安装工具
sudo apt-get install gpiod

# 查看 GPIO 信息
gpiodetect
gpioinfo
gpiofind "LED"
gpioget gpiochip0 10
gpioset gpiochip0 10=1

# 4. 在内核中添加调试信息
echo "file gpio_core.c +p" > /sys/kernel/debug/dynamic_debug/control
```

### 2.4 实现中断驱动

#### 2.4.1 驱动源码：irq_handler.c

```cpp
// irq_handler.c - 中断处理实现
#include <linux/module.h>
#include <linux/interrupt.h>
#include <linux/workqueue.h>
#include <linux/timer.h>
#include <linux/atomic.h>

/**
 * struct interrupt_data - 中断处理数据结构
 * 管理中断相关的状态和资源
 */
struct interrupt_data {
    struct device *dev;              // 关联的设备
    int irq_number;                  // 中断号
    atomic_t irq_count;              // 中断计数（原子操作）
    struct timer_list debounce_timer; // 消抖定时器
    struct work_struct work;         // 工作队列项
    struct workqueue_struct *wq;     // 工作队列

    // 状态标志
    unsigned long last_irq_time;     // 上次中断时间
    atomic_t button_pressed;         // 按键状态
    wait_queue_head_t wait_queue;    // 等待队列

    // 回调函数
    void (*callback)(void *data);    // 用户回调
    void *callback_data;             // 回调数据
};

/**
 * button_work_handler() - 工作队列处理函数
 * @work: 工作队列项
 *
 * 在进程上下文中处理中断的耗时操作
 * 可以安全地使用可能引起休眠的函数
 */
static void button_work_handler(struct work_struct *work)
{
    struct interrupt_data *idata = container_of(work, struct interrupt_data, work);

    dev_info(idata->dev, "工作队列处理：按键事件\n");

    // 可以执行耗时操作
    // msleep(10);  // 如果需要可以休眠

    // 更新系统状态
    sysfs_notify(&idata->dev->kobj, NULL, "button");

    // 调用用户回调（如果设置）
    if (idata->callback) {
        idata->callback(idata->callback_data);
    }

    // 唤醒等待进程
    wake_up_interruptible(&idata->wait_queue);
}

/**
 * button_debounce_timer() - 消抖定时器回调
 * @timer: 定时器指针
 *
 * 用于按键消抖，定时器到期后读取稳定的按键状态
 */
static void button_debounce_timer(struct timer_list *timer)
{
    struct interrupt_data *idata = from_timer(idata, timer, debounce_timer);
    int state;

    // 读取稳定的 GPIO 状态
    state = gpio_button_get(idata->gpio_control);

    if (state != atomic_read(&idata->button_pressed)) {
        atomic_set(&idata->button_pressed, state);

        // 调度工作队列处理
        queue_work(idata->wq, &idata->work);

        dev_dbg(idata->dev, "消抖完成，按键状态: %s\n",
                state ? "按下" : "释放");
    }
}

/**
 * button_irq_handler() - 中断处理函数（上半部）
 * @irq: 中断号
 * @dev_id: 设备标识符
 *
 * 中断上半部，处理要尽可能快
 * 返回值：IRQ_WAKE_THREAD 表示需要下半部处理
 */
static irqreturn_t button_irq_handler(int irq, void *dev_id)
{
    struct interrupt_data *idata = dev_id;
    unsigned long current_time = jiffies;

    // 原子操作增加中断计数
    atomic_inc(&idata->irq_count);

    // 简单的时间戳记录
    idata->last_irq_time = current_time;

    /**
     * 中断消抖逻辑：
     * 1. 取消之前的定时器（如果还在运行）
     * 2. 重新启动定时器
     * 这样可以避免按键抖动引起的多次中断
     */
    del_timer(&idata->debounce_timer);

    // 设置定时器 20ms 后触发消抖检查
    mod_timer(&idata->debounce_timer, jiffies + msecs_to_jiffies(20));

    dev_dbg(idata->dev, "中断触发 #%d\n", atomic_read(&idata->irq_count));

    /**
     * 返回 IRQ_HANDLED 表示中断已处理
     * 如果使用线程化中断，可以返回 IRQ_WAKE_THREAD
     */
    return IRQ_HANDLED;
}

/**
 * threaded_irq_handler() - 线程化中断处理函数（下半部）
 * @irq: 中断号
 * @dev_id: 设备标识符
 *
 * 线程化中断的下半部，可以执行耗时操作
 */
static irqreturn_t threaded_irq_handler(int irq, void *dev_id)
{
    struct interrupt_data *idata = dev_id;

    // 在线程上下文中可以安全地休眠
    // msleep(1);

    // 执行实际的处理工作
    button_work_handler(&idata->work);

    return IRQ_HANDLED;
}

/**
 * interrupt_setup() - 初始化中断处理
 * @dev: 设备指针
 * @gpio_desc: 按键 GPIO 描述符
 * @idata: 中断数据结构指针
 *
 * 返回值：成功返回 0，失败返回错误码
 */
int interrupt_setup(struct device *dev, struct gpio_desc *button_gpio,
                   struct interrupt_data *idata)
{
    int ret, irq;

    if (!dev || !button_gpio || !idata) {
        return -EINVAL;
    }

    // 初始化数据结构
    idata->dev = dev;
    atomic_set(&idata->irq_count, 0);
    atomic_set(&idata->button_pressed, 0);

    // 1. 获取中断号
    irq = gpiod_to_irq(button_gpio);
    if (irq < 0) {
        dev_err(dev, "无法获取 GPIO 中断号: %d\n", irq);
        return irq;
    }
    idata->irq_number = irq;

    // 2. 初始化等待队列
    init_waitqueue_head(&idata->wait_queue);

    // 3. 初始化定时器（用于消抖）
    timer_setup(&idata->debounce_timer, button_debounce_timer, 0);

    // 4. 创建工作队列
    idata->wq = create_singlethread_workqueue("button_wq");
    if (!idata->wq) {
        dev_err(dev, "无法创建工作队列\n");
        return -ENOMEM;
    }

    // 5. 初始化工作
    INIT_WORK(&idata->work, button_work_handler);

    // 6. 注册中断处理函数
    dev_info(dev, "注册中断 %d (GPIO: %d)\n", irq,
             desc_to_gpio(button_gpio));

    /**
     * 方法1：普通中断 + 工作队列
     */
    ret = request_irq(irq, button_irq_handler,
                     IRQF_TRIGGER_FALLING | IRQF_TRIGGER_RISING,
                     "button_irq", idata);

    /**
     * 方法2：线程化中断（推荐，更简单）
     * ret = request_threaded_irq(irq, button_irq_handler,
     *                           threaded_irq_handler,
     *                           IRQF_TRIGGER_FALLING | IRQF_TRIGGER_RISING | IRQF_ONESHOT,
     *                           "button_irq", idata);
     */

    if (ret) {
        dev_err(dev, "无法注册中断: %d\n", ret);
        destroy_workqueue(idata->wq);
        return ret;
    }

    // 7. 启用中断（默认就是启用的）
    enable_irq(irq);

    dev_info(dev, "中断初始化成功 (IRQ: %d)\n", irq);
    return 0;
}

/**
 * interrupt_cleanup() - 清理中断资源
 * @idata: 中断数据结构指针
 */
void interrupt_cleanup(struct interrupt_data *idata)
{
    if (!idata) {
        return;
    }

    // 1. 禁用中断
    if (idata->irq_number > 0) {
        disable_irq(idata->irq_number);
    }

    // 2. 释放中断
    free_irq(idata->irq_number, idata);

    // 3. 删除定时器
    del_timer_sync(&idata->debounce_timer);

    // 4. 销毁工作队列
    if (idata->wq) {
        flush_workqueue(idata->wq);
        destroy_workqueue(idata->wq);
    }

    dev_info(idata->dev, "中断资源已清理\n");
}

/**
 * interrupt_wait_event() - 等待中断事件
 * @idata: 中断数据结构指针
 * @timeout_ms: 超时时间（毫秒）
 *
 * 供应用程序调用，等待按键事件
 */
int interrupt_wait_event(struct interrupt_data *idata, int timeout_ms)
{
    int ret;
    long timeout_jiffies = msecs_to_jiffies(timeout_ms);

    /**
     * wait_event_interruptible_timeout() - 可中断的超时等待
     * @wq: 等待队列头
     * @condition: 等待条件（当为真时返回）
     * @timeout: 超时时间（jiffies）
     * 返回值：>0 条件满足，0 超时，<0 被信号中断
     */
    ret = wait_event_interruptible_timeout(idata->wait_queue,
                                          atomic_read(&idata->button_pressed) != 0,
                                          timeout_jiffies);
    return ret;
}

EXPORT_SYMBOL(interrupt_setup);
EXPORT_SYMBOL(interrupt_cleanup);
EXPORT_SYMBOL(interrupt_wait_event);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("通用中断处理模块");
MODULE_AUTHOR("Driver Developer");
```

#### 2.4.2 中断调试技巧

```bash
#!/bin/bash
# interrupt_debug.sh - 中断调试脚本

echo "=== 中断系统状态 ==="

# 1. 查看所有中断统计
echo "1. 系统中断统计:"
cat /proc/interrupts | grep -E "(button|gpio|irq)"

# 2. 查看特定中断信息
echo -e "\n2. 按键中断详情:"
IRQ_NUM=$(cat /proc/interrupts | grep button | awk '{print $1}' | sed 's/://')
if [ ! -z "$IRQ_NUM" ]; then
    echo "中断号: $IRQ_NUM"
    cat /proc/irq/$IRQ_NUM/spurious
    cat /proc/irq/$IRQ_NUM/affinity_hint
fi

# 3. 查看中断亲和性（多核CPU）
echo -e "\n3. CPU 中断分布:"
for cpu in /sys/devices/system/cpu/cpu[0-9]*; do
    cpu_num=$(basename $cpu | sed 's/cpu//')
    echo -n "CPU$cpu_num: "
    cat $cpu/topology/thread_siblings_list
done

# 4. 动态调整中断亲和性
echo -e "\n4. 调整中断亲和性示例:"
# 将中断绑定到 CPU0
# echo 1 > /proc/irq/$IRQ_NUM/smp_affinity

# 5. 监控中断频率
echo -e "\n5. 实时监控中断（按 Ctrl+C 停止）:"
watch -n 1 "cat /proc/interrupts | head -20"

# 6. 使用 ftrace 跟踪中断
echo -e "\n6. 使用 ftrace 跟踪中断流:"
echo 0 > /sys/kernel/debug/tracing/tracing_on
echo function_graph > /sys/kernel/debug/tracing/current_tracer
echo "handle_irq_event*" > /sys/kernel/debug/tracing/set_ftrace_filter
echo "request_threaded_irq" >> /sys/kernel/debug/tracing/set_ftrace_filter
echo 1 > /sys/kernel/debug/tracing/tracing_on
# 等待中断发生...
sleep 2
echo 0 > /sys/kernel/debug/tracing/tracing_on
cat /sys/kernel/debug/tracing/trace > /tmp/interrupt_trace.txt
echo "跟踪结果保存到: /tmp/interrupt_trace.txt"
```

### 2.5 实现字符设备驱动

#### 2.5.1 驱动源码：char_device.c

```cpp
// char_device.c - 字符设备驱动实现
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/poll.h>
#include <linux/fcntl.h>
#include <linux/slab.h>
#include <linux/wait.h>
#include <linux/sched.h>
#include <linux/version.h>

/**
 * struct char_device_data - 字符设备私有数据
 * 管理字符设备的所有状态和资源
 */
struct char_device_data {
    struct cdev cdev;                // 字符设备结构
    struct device *device;           // 关联的设备
    dev_t devno;                     // 设备号

    // 同步机制
    struct mutex mutex;              // 保护设备操作
    struct rw_semaphore rwsem;       // 读写信号量
    wait_queue_head_t read_queue;    // 读等待队列
    wait_queue_head_t write_queue;   // 写等待队列

    // 缓冲区管理
    char *buffer;                    // 数据缓冲区
    size_t buffer_size;              // 缓冲区大小
    size_t data_len;                 // 当前数据长度
    loff_t read_pos;                 // 读位置
    loff_t write_pos;                // 写位置

    // 异步通知
    struct fasync_struct *fasync_queue;

    // 下层组件引用
    struct gpio_control *gpio_ctrl;
    struct interrupt_data *irq_data;

    // 设备状态
    unsigned int open_count;         // 打开计数
    bool is_open;                    // 打开状态
    atomic_t available;              // 数据可用标志
};

/**
 * char_device_open() - 打开设备
 * @inode: 设备 inode
 * @filp: 文件结构指针
 *
 * 当应用程序调用 open() 时触发
 */
static int char_device_open(struct inode *inode, struct file *filp)
{
    struct char_device_data *cdata;

    // 从 inode 获取设备私有数据
    cdata = container_of(inode->i_cdev, struct char_device_data, cdev);

    // 检查设备是否已经打开（可选）
    mutex_lock(&cdata->mutex);
    if (cdata->is_open) {
        mutex_unlock(&cdata->mutex);
        pr_warn("设备已经被打开\n");
        return -EBUSY;
    }

    // 更新状态
    cdata->open_count++;
    cdata->is_open = true;

    // 将私有数据保存到文件结构中
    filp->private_data = cdata;

    mutex_unlock(&cdata->mutex);

    pr_info("设备已打开，打开计数: %u\n", cdata->open_count);
    return 0;
}

/**
 * char_device_release() - 关闭设备
 * @inode: 设备 inode
 * @filp: 文件结构指针
 *
 * 当应用程序调用 close() 时触发
 */
static int char_device_release(struct inode *inode, struct file *filp)
{
    struct char_device_data *cdata = filp->private_data;

    if (!cdata) {
        return -ENODEV;
    }

    mutex_lock(&cdata->mutex);

    // 清除异步通知队列
    if (cdata->fasync_queue) {
        fasync_helper(-1, filp, 0, &cdata->fasync_queue);
    }

    // 更新状态
    cdata->open_count--;
    if (cdata->open_count == 0) {
        cdata->is_open = false;
        // 清理缓冲区
        cdata->data_len = 0;
        cdata->read_pos = 0;
        cdata->write_pos = 0;
    }

    mutex_unlock(&cdata->mutex);

    pr_info("设备已关闭，剩余打开计数: %u\n", cdata->open_count);
    return 0;
}

/**
 * char_device_read() - 读取设备数据
 * @filp: 文件结构指针
 * @buf: 用户空间缓冲区
 * @count: 请求读取的字节数
 * @f_pos: 文件位置指针
 *
 * 支持阻塞和非阻塞读取
 */
static ssize_t char_device_read(struct file *filp, char __user *buf,
                               size_t count, loff_t *f_pos)
{
    struct char_device_data *cdata = filp->private_data;
    ssize_t retval = 0;
    size_t available;

    if (!cdata) {
        return -ENODEV;
    }

    // 非阻塞模式检查
    if (filp->f_flags & O_NONBLOCK) {
        if (!atomic_read(&cdata->available)) {
            return -EAGAIN;
        }
    } else {
        // 阻塞等待数据可用
        retval = wait_event_interruptible(cdata->read_queue,
                                         atomic_read(&cdata->available));
        if (retval) {
            return retval;  // 被信号中断
        }
    }

    // 获取读信号量（允许并发读）
    down_read(&cdata->rwsem);

    // 计算可用数据量
    available = cdata->data_len - cdata->read_pos;
    if (available == 0) {
        up_read(&cdata->rwsem);
        return 0;  // EOF
    }

    // 限制读取数量
    if (count > available) {
        count = available;
    }

    // 复制数据到用户空间
    if (copy_to_user(buf, cdata->buffer + cdata->read_pos, count)) {
        up_read(&cdata->rwsem);
        return -EFAULT;
    }

    // 更新位置
    cdata->read_pos += count;
    if (cdata->read_pos >= cdata->data_len) {
        // 所有数据已读完
        cdata->read_pos = 0;
        cdata->write_pos = 0;
        cdata->data_len = 0;
        atomic_set(&cdata->available, 0);
    }

    up_read(&cdata->rwsem);

    // 唤醒可能的写等待
    wake_up_interruptible(&cdata->write_queue);

    pr_debug("读取 %zu 字节，剩余 %zu 字节\n",
             count, cdata->data_len - cdata->read_pos);

    return count;
}

/**
 * char_device_write() - 写入设备数据
 * @filp: 文件结构指针
 * @buf: 用户空间数据缓冲区
 * @count: 写入字节数
 * @f_pos: 文件位置指针
 *
 * 支持阻塞和非阻塞写入
 */
static ssize_t char_device_write(struct file *filp, const char __user *buf,
                                size_t count, loff_t *f_pos)
{
    struct char_device_data *cdata = filp->private_data;
    ssize_t retval = 0;
    size_t free_space;

    if (!cdata) {
        return -ENODEV;
    }

    // 参数检查
    if (count == 0) {
        return 0;
    }
    if (count > cdata->buffer_size) {
        count = cdata->buffer_size;
    }

    // 阻塞等待缓冲区空间（如果不是非阻塞模式）
    if (!(filp->f_flags & O_NONBLOCK)) {
        retval = wait_event_interruptible(cdata->write_queue,
                                         cdata->data_len + count <= cdata->buffer_size);
        if (retval) {
            return retval;
        }
    } else {
        // 非阻塞模式检查空间
        if (cdata->data_len + count > cdata->buffer_size) {
            return -EAGAIN;
        }
    }

    // 获取写信号量（独占访问）
    down_write(&cdata->rwsem);

    // 计算可用空间
    free_space = cdata->buffer_size - cdata->data_len;
    if (count > free_space) {
        count = free_space;
    }

    // 复制用户数据到内核缓冲区
    if (copy_from_user(cdata->buffer + cdata->write_pos, buf, count)) {
        up_write(&cdata->rwsem);
        return -EFAULT;
    }

    // 更新缓冲区状态
    cdata->write_pos += count;
    cdata->data_len += count;

    // 如果缓冲区已满，更新写位置
    if (cdata->write_pos >= cdata->buffer_size) {
        cdata->write_pos = 0;
    }

    up_write(&cdata->rwsem);

    // 设置数据可用标志
    atomic_set(&cdata->available, 1);

    // 唤醒可能的读等待
    wake_up_interruptible(&cdata->read_queue);

    // 发送异步通知（如果有注册）
    if (cdata->fasync_queue) {
        kill_fasync(&cdata->fasync_queue, SIGIO, POLL_IN);
    }

    pr_debug("写入 %zu 字节，缓冲区使用率: %zu/%zu\n",
             count, cdata->data_len, cdata->buffer_size);

    return count;
}

/**
 * char_device_ioctl() - 设备控制命令
 * @filp: 文件结构指针
 * @cmd: 命令号
 * @arg: 命令参数
 *
 * 实现自定义的设备控制命令
 */
static long char_device_ioctl(struct file *filp, unsigned int cmd,
                             unsigned long arg)
{
    struct char_device_data *cdata = filp->private_data;
    int retval = 0;
    int value;

    if (!cdata) {
        return -ENODEV;
    }

    // 检查命令权限
    if (_IOC_TYPE(cmd) != 'L') {
        return -ENOTTY;
    }

    mutex_lock(&cdata->mutex);

    switch (cmd) {
    case LED_ON:
        if (cdata->gpio_ctrl) {
            retval = gpio_led_set(cdata->gpio_ctrl, 1);
        }
        break;

    case LED_OFF:
        if (cdata->gpio_ctrl) {
            retval = gpio_led_set(cdata->gpio_ctrl, 0);
        }
        break;

    case LED_TOGGLE:
        if (cdata->gpio_ctrl) {
            retval = gpio_led_toggle(cdata->gpio_ctrl);
        }
        break;

    case GET_BUTTON_STATE:
        if (cdata->gpio_ctrl) {
            value = gpio_button_get(cdata->gpio_ctrl);
            retval = put_user(value, (int __user *)arg);
        }
        break;

    case WAIT_FOR_BUTTON:
        if (cdata->irq_data) {
            retval = interrupt_wait_event(cdata->irq_data, arg);
        }
        break;

    case GET_BUFFER_INFO: {
        struct buffer_info info;
        info.size = cdata->buffer_size;
        info.used = cdata->data_len;
        info.free = cdata->buffer_size - cdata->data_len;
        retval = copy_to_user((void __user *)arg, &info, sizeof(info)) ?
                 -EFAULT : 0;
        break;
    }

    default:
        retval = -ENOTTY;
        break;
    }

    mutex_unlock(&cdata->mutex);
    return retval;
}

/**
 * char_device_poll() - 轮询设备状态
 * @filp: 文件结构指针
 * @wait: 轮询表
 *
 * 支持 select() 和 poll() 系统调用
 */
static __poll_t char_device_poll(struct file *filp, poll_table *wait)
{
    struct char_device_data *cdata = filp->private_data;
    __poll_t mask = 0;

    if (!cdata) {
        return EPOLLERR;
    }

    // 注册等待队列
    poll_wait(filp, &cdata->read_queue, wait);
    poll_wait(filp, &cdata->write_queue, wait);

    // 检查可读状态
    if (atomic_read(&cdata->available)) {
        mask |= EPOLLIN | EPOLLRDNORM;
    }

    // 检查可写状态
    if (cdata->data_len < cdata->buffer_size) {
        mask |= EPOLLOUT | EPOLLWRNORM;
    }

    // 检查错误状态
    if (!cdata->is_open) {
        mask |= EPOLLERR;
    }

    return mask;
}

/**
 * char_device_fasync() - 异步通知支持
 * @fd: 文件描述符
 * @filp: 文件结构指针
 * @on: 启用/禁用标志
 *
 * 支持异步通知（信号驱动 I/O）
 */
static int char_device_fasync(int fd, struct file *filp, int on)
{
    struct char_device_data *cdata = filp->private_data;

    if (!cdata) {
        return -ENODEV;
    }

    return fasync_helper(fd, filp, on, &cdata->fasync_queue);
}

/**
 * char_device_mmap() - 内存映射支持
 * @filp: 文件结构指针
 * @vma: 虚拟内存区域
 *
 * 将设备缓冲区映射到用户空间
 */
static int char_device_mmap(struct file *filp, struct vm_area_struct *vma)
{
    struct char_device_data *cdata = filp->private_data;
    unsigned long size = vma->vm_end - vma->vm_start;

    if (!cdata || !cdata->buffer) {
        return -ENODEV;
    }

    // 检查映射大小
    if (size > cdata->buffer_size) {
        return -EINVAL;
    }

    // 将内核缓冲区映射到用户空间
    return remap_pfn_range(vma, vma->vm_start,
                          virt_to_phys(cdata->buffer) >> PAGE_SHIFT,
                          size, vma->vm_page_prot);
}

/**
 * 文件操作结构体
 * 定义设备支持的所有操作
 */
static const struct file_operations char_device_fops = {
    .owner = THIS_MODULE,
    .open = char_device_open,
    .release = char_device_release,
    .read = char_device_read,
    .write = char_device_write,
    .unlocked_ioctl = char_device_ioctl,
    .compat_ioctl = compat_ptr_ioctl,
    .poll = char_device_poll,
    .fasync = char_device_fasync,
    .mmap = char_device_mmap,
    .llseek = no_llseek,
};

/**
 * char_device_create() - 创建字符设备
 * @parent: 父设备
 * @gpio_ctrl: GPIO 控制结构
 * @irq_data: 中断数据结构
 * @buffer_size: 缓冲区大小
 *
 * 返回值：成功返回设备指针，失败返回 ERR_PTR
 */
struct char_device_data *char_device_create(struct device *parent,
                                          struct gpio_control *gpio_ctrl,
                                          struct interrupt_data *irq_data,
                                          size_t buffer_size)
{
    struct char_device_data *cdata;
    int ret;
    dev_t devno;

    if (!parent) {
        return ERR_PTR(-EINVAL);
    }

    // 1. 分配设备数据结构
    cdata = devm_kzalloc(parent, sizeof(*cdata), GFP_KERNEL);
    if (!cdata) {
        return ERR_PTR(-ENOMEM);
    }

    // 2. 分配缓冲区
    cdata->buffer = devm_kzalloc(parent, buffer_size, GFP_KERNEL);
    if (!cdata->buffer) {
        return ERR_PTR(-ENOMEM);
    }

    cdata->buffer_size = buffer_size;
    cdata->data_len = 0;
    cdata->read_pos = 0;
    cdata->write_pos = 0;
    cdata->gpio_ctrl = gpio_ctrl;
    cdata->irq_data = irq_data;
    cdata->device = parent;
    cdata->open_count = 0;
    cdata->is_open = false;
    atomic_set(&cdata->available, 0);

    // 3. 初始化同步机制
    mutex_init(&cdata->mutex);
    init_rwsem(&cdata->rwsem);
    init_waitqueue_head(&cdata->read_queue);
    init_waitqueue_head(&cdata->write_queue);

    // 4. 动态分配设备号
    ret = alloc_chrdev_region(&devno, 0, 1, "led_button");
    if (ret < 0) {
        dev_err(parent, "无法分配设备号: %d\n", ret);
        return ERR_PTR(ret);
    }
    cdata->devno = devno;

    // 5. 初始化字符设备
    cdev_init(&cdata->cdev, &char_device_fops);
    cdata->cdev.owner = THIS_MODULE;

    // 6. 添加到系统
    ret = cdev_add(&cdata->cdev, devno, 1);
    if (ret) {
        dev_err(parent, "无法添加字符设备: %d\n", ret);
        unregister_chrdev_region(devno, 1);
        return ERR_PTR(ret);
    }

    // 7. 创建设备节点（可选，udev 会自动创建）
    cdata->device = device_create(class_led_button, parent,
                                 devno, NULL, "led_button");
    if (IS_ERR(cdata->device)) {
        dev_err(parent, "无法创建设备节点\n");
        cdev_del(&cdata->cdev);
        unregister_chrdev_region(devno, 1);
        return ERR_CAST(cdata->device);
    }

    dev_info(parent, "字符设备创建成功，主设备号: %d，次设备号: %d\n",
             MAJOR(devno), MINOR(devno));
    dev_info(parent, "设备节点: /dev/led_button\n");

    return cdata;
}

/**
 * char_device_destroy() - 销毁字符设备
 * @cdata: 字符设备数据指针
 */
void char_device_destroy(struct char_device_data *cdata)
{
    if (!cdata) {
        return;
    }

    // 1. 删除设备节点
    if (!IS_ERR_OR_NULL(cdata->device)) {
        device_destroy(class_led_button, cdata->devno);
    }

    // 2. 删除字符设备
    cdev_del(&cdata->cdev);

    // 3. 释放设备号
    unregister_chrdev_region(cdata->devno, 1);

    // 4. 销毁同步机制
    mutex_destroy(&cdata->mutex);

    dev_info(cdata->device, "字符设备已销毁\n");
}

EXPORT_SYMBOL(char_device_create);
EXPORT_SYMBOL(char_device_destroy);

// 创建设备类（模块全局）
static struct class *class_led_button;

static int __init char_device_init(void)
{
    // 创建设备类
    class_led_button = class_create(THIS_MODULE, "led_button");
    if (IS_ERR(class_led_button)) {
        pr_err("无法创建设备类\n");
        return PTR_ERR(class_led_button);
    }

    pr_info("字符设备模块初始化成功\n");
    return 0;
}

static void __exit char_device_exit(void)
{
    // 销毁设备类
    if (class_led_button) {
        class_destroy(class_led_button);
    }

    pr_info("字符设备模块卸载成功\n");
}

module_init(char_device_init);
module_exit(char_device_exit);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("通用字符设备驱动框架");
MODULE_AUTHOR("Driver Developer");
```

### 2.6 整合所有组件的主驱动

#### 2.6.1 主驱动源码：led_button_driver.c

```cpp
// led_button_driver.c - 主驱动整合
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/of.h>
#include <linux/err.h>
#include <linux/slab.h>

/**
 * struct led_button_driver_data - 主驱动私有数据
 * 整合所有子模块
 */
struct led_button_driver_data {
    struct device *dev;
    struct platform_device *pdev;

    // 子模块
    struct gpio_control *gpio_ctrl;
    struct interrupt_data *irq_data;
    struct char_device_data *char_data;

    // 资源管理
    bool gpio_initialized;
    bool irq_initialized;
    bool char_initialized;
};

/**
 * led_button_probe() - 驱动探测函数
 * @pdev: 平台设备指针
 *
 * 当设备树节点匹配时自动调用
 */
static int led_button_probe(struct platform_device *pdev)
{
    struct device *dev = &pdev->dev;
    struct led_button_driver_data *data;
    struct gpio_desc *button_gpio;
    int ret = 0;

    dev_info(dev, "开始探测设备...\n");

    // 1. 分配主数据结构
    data = devm_kzalloc(dev, sizeof(*data), GFP_KERNEL);
    if (!data) {
        return -ENOMEM;
    }

    data->dev = dev;
    data->pdev = pdev;
    platform_set_drvdata(pdev, data);

    // 2. 初始化 GPIO 子系统
    dev_info(dev, "初始化 GPIO...\n");
    data->gpio_ctrl = devm_kzalloc(dev, sizeof(struct gpio_control), GFP_KERNEL);
    if (!data->gpio_ctrl) {
        return -ENOMEM;
    }

    ret = gpio_setup(dev, data->gpio_ctrl);
    if (ret) {
        dev_err(dev, "GPIO 初始化失败: %d\n", ret);
        goto err_gpio;
    }
    data->gpio_initialized = true;

    // 3. 初始化中断处理
    dev_info(dev, "初始化中断...\n");
    data->irq_data = devm_kzalloc(dev, sizeof(struct interrupt_data), GFP_KERNEL);
    if (!data->irq_data) {
        ret = -ENOMEM;
        goto err_irq_alloc;
    }

    // 获取按键 GPIO（从 gpio_ctrl 中获取或重新获取）
    button_gpio = devm_gpiod_get(dev, "button", GPIOD_IN);
    if (IS_ERR(button_gpio)) {
        ret = PTR_ERR(button_gpio);
        dev_err(dev, "无法获取按键 GPIO: %d\n", ret);
        goto err_irq;
    }

    ret = interrupt_setup(dev, button_gpio, data->irq_data);
    if (ret) {
        dev_err(dev, "中断初始化失败: %d\n", ret);
        goto err_irq;
    }
    data->irq_initialized = true;

    // 4. 创建设备节点
    dev_info(dev, "创建字符设备...\n");
    data->char_data = char_device_create(dev, data->gpio_ctrl, data->irq_data, 4096);
    if (IS_ERR(data->char_data)) {
        ret = PTR_ERR(data->char_data);
        dev_err(dev, "字符设备创建失败: %d\n", ret);
        goto err_char;
    }
    data->char_initialized = true;

    // 5. 创建设备属性文件（sysfs 接口）
    ret = sysfs_create_group(&dev->kobj, &led_button_attr_group);
    if (ret) {
        dev_warn(dev, "无法创建设备属性: %d\n", ret);
        // 继续执行，这不是致命错误
    }

    // 6. 创建设备树属性文件（调试用）
    device_create_file(dev, &dev_attr_debug);
    device_create_file(dev, &dev_attr_status);

    dev_info(dev, "驱动加载成功！\n");
    dev_info(dev, "设备节点: /dev/led_button\n");
    dev_info(dev, "调试接口: /sys/class/led_button/led_button.*\n");

    return 0;

// 错误处理（按初始化顺序反向清理）
err_char:
    if (data->char_initialized) {
        char_device_destroy(data->char_data);
    }

err_irq:
    if (data->irq_initialized) {
        interrupt_cleanup(data->irq_data);
    }

err_irq_alloc:
    if (data->gpio_initialized) {
        gpio_cleanup(data->gpio_ctrl);
    }

err_gpio:
    return ret;
}

/**
 * led_button_remove() - 驱动移除函数
 * @pdev: 平台设备指针
 */
static int led_button_remove(struct platform_device *pdev)
{
    struct led_button_driver_data *data = platform_get_drvdata(pdev);
    struct device *dev = &pdev->dev;

    dev_info(dev, "开始移除驱动...\n");

    // 按初始化顺序反向清理

    // 1. 移除 sysfs 属性
    sysfs_remove_group(&dev->kobj, &led_button_attr_group);
    device_remove_file(dev, &dev_attr_debug);
    device_remove_file(dev, &dev_attr_status);

    // 2. 销毁字符设备
    if (data->char_initialized) {
        char_device_destroy(data->char_data);
        data->char_initialized = false;
    }

    // 3. 清理中断资源
    if (data->irq_initialized) {
        interrupt_cleanup(data->irq_data);
        data->irq_initialized = false;
    }

    // 4. 清理 GPIO 资源
    if (data->gpio_initialized) {
        gpio_cleanup(data->gpio_ctrl);
        data->gpio_initialized = false;
    }

    dev_info(dev, "驱动已完全移除\n");
    return 0;
}

/**
 * 设备树匹配表
 * 驱动通过此表匹配设备树中的节点
 */
static const struct of_device_id led_button_of_match[] = {
    { .compatible = "custom,led-button-v1" },
    { .compatible = "custom,led-button-v2" },
    { .compatible = "generic,led-button" },
    {},  // 结束标记
};
MODULE_DEVICE_TABLE(of, led_button_of_match);

/**
 * 平台驱动结构体
 * 定义驱动的基本信息
 */
static struct platform_driver led_button_driver = {
    .probe = led_button_probe,
    .remove = led_button_remove,
    .driver = {
        .name = "led_button_driver",
        .of_match_table = led_button_of_match,
        .owner = THIS_MODULE,
    },
};

/**
 * 模块初始化函数
 */
static int __init led_button_init(void)
{
    int ret;

    pr_info("LED 按键驱动开始加载...\n");

    ret = platform_driver_register(&led_button_driver);
    if (ret) {
        pr_err("平台驱动注册失败: %d\n", ret);
        return ret;
    }

    pr_info("LED 按键驱动加载成功\n");
    return 0;
}

/**
 * 模块清理函数
 */
static void __exit led_button_exit(void)
{
    pr_info("开始卸载 LED 按键驱动...\n");

    platform_driver_unregister(&led_button_driver);

    pr_info("LED 按键驱动卸载完成\n");
}

module_init(led_button_init);
module_exit(led_button_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Driver Developer");
MODULE_DESCRIPTION("完整的 LED 和按键驱动示例");
MODULE_VERSION("1.0");
```

### 2.7 编译和测试

#### 2.7.1 完整的 Makefile

```makefile
# Makefile - 驱动编译配置
KDIR ?= /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

# 驱动模块列表
obj-m := led_button_driver.o
led_button_driver-objs := \
    gpio_core.o \
    irq_handler.o \
    char_device.o \
    led_button_driver.o

# 内核模块编译标志
ccflags-y := -I$(src)/include -DDEBUG
ccflags-y += -Wno-declaration-after-statement

# 用户空间测试程序
TEST_PROGS := led_button_test

all: modules test_apps

modules:
    @echo "编译内核模块..."
    $(MAKE) -C $(KDIR) M=$(PWD) modules

test_apps: $(TEST_PROGS)

led_button_test: test/led_button_test.c
    @echo "编译测试程序..."
    $(CC) -o $@ $< -lpthread

clean:
    @echo "清理编译文件..."
    $(MAKE) -C $(KDIR) M=$(PWD) clean
    rm -f $(TEST_PROGS)
    rm -f *.o *.ko *.mod.c *.mod.o *.order *.symvers

install: modules
    @echo "安装驱动模块..."
    sudo cp led_button_driver.ko /lib/modules/$(shell uname -r)/kernel/drivers/misc/
    sudo depmod -a

load: modules
    @echo "加载驱动模块..."
    sudo insmod led_button_driver.ko
    sudo dmesg | tail -10

unload:
    @echo "卸载驱动模块..."
    sudo rmmod led_button_driver
    sudo dmesg | tail -10

reload: unload load

# 调试目标
debug:
    @echo "启用调试输出..."
    echo "module led_button_driver +p" | sudo tee /sys/kernel/debug/dynamic_debug/control

.PHONY: all modules clean install load unload reload debug
```

#### 2.7.2 测试应用程序

```cpp
// test/led_button_test.c - 完整的测试程序
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <poll.h>
#include <signal.h>
#include <pthread.h>
#include <sys/ioctl.h>

// 定义与驱动一致的 IOCTL 命令
#define LED_ON           _IO('L', 1)
#define LED_OFF          _IO('L', 2)
#define LED_TOGGLE       _IO('L', 3)
#define GET_BUTTON_STATE _IOR('L', 4, int)
#define WAIT_FOR_BUTTON  _IOW('L', 5, int)
#define GET_BUFFER_INFO  _IOR('L', 6, struct buffer_info)

struct buffer_info {
    size_t size;
    size_t used;
    size_t free;
};

// 全局变量
static volatile int running = 1;
static int fd = -1;

// 信号处理函数
void signal_handler(int sig)
{
    printf("\n收到信号 %d，准备退出...\n", sig);
    running = 0;
}

// 异步通知回调
void async_callback(int sig)
{
    char buffer[256];
    int n;

    if (sig == SIGIO) {
        n = read(fd, buffer, sizeof(buffer) - 1);
        if (n > 0) {
            buffer[n] = '\0';
            printf("[异步通知] 收到数据: %s\n", buffer);
        }
    }
}

// 测试用例 1：基本 LED 控制
void test_led_control(void)
{
    printf("\n=== 测试 LED 控制 ===\n");

    // 打开 LED
    if (ioctl(fd, LED_ON) < 0) {
        perror("LED_ON 失败");
    } else {
        printf("✓ LED 已打开\n");
        sleep(1);
    }

    // 关闭 LED
    if (ioctl(fd, LED_OFF) < 0) {
        perror("LED_OFF 失败");
    } else {
        printf("✓ LED 已关闭\n");
        sleep(1);
    }

    // 翻转 LED
    for (int i = 0; i < 5; i++) {
        if (ioctl(fd, LED_TOGGLE) < 0) {
            perror("LED_TOGGLE 失败");
            break;
        }
        printf("✓ LED 翻转 %d\n", i + 1);
        usleep(500000);  // 500ms
    }
}

// 测试用例 2：按键状态读取
void test_button_read(void)
{
    int state;

    printf("\n=== 测试按键读取 ===\n");
    printf("请按下按键（按 Ctrl+C 跳过）...\n");

    for (int i = 0; i < 10 && running; i++) {
        if (ioctl(fd, GET_BUTTON_STATE, &state) < 0) {
            perror("GET_BUTTON_STATE 失败");
            break;
        }

        printf("  按键状态: %s\n", state ? "按下" : "释放");
        usleep(500000);  // 500ms
    }
}

// 测试用例 3：阻塞等待按键
void test_button_wait(void)
{
    int timeout = 5000;  // 5 秒

    printf("\n=== 测试阻塞等待按键 ===\n");
    printf("请在 %d 毫秒内按下按键...\n", timeout);

    if (ioctl(fd, WAIT_FOR_BUTTON, &timeout) < 0) {
        if (errno == ETIMEDOUT) {
            printf("✗ 等待超时，按键未按下\n");
        } else {
            perror("WAIT_FOR_BUTTON 失败");
        }
    } else {
        printf("✓ 检测到按键按下！\n");
    }
}

// 测试用例 4：读写数据
void test_data_rw(void)
{
    char write_buf[64];
    char read_buf[64];
    int n;

    printf("\n=== 测试数据读写 ===\n");

    // 写入数据
    snprintf(write_buf, sizeof(write_buf),
             "测试数据，时间戳: %ld", time(NULL));

    n = write(fd, write_buf, strlen(write_buf));
    if (n < 0) {
        perror("写入失败");
    } else {
        printf("✓ 写入 %d 字节: %s\n", n, write_buf);
    }

    // 读取数据
    n = read(fd, read_buf, sizeof(read_buf) - 1);
    if (n < 0) {
        perror("读取失败");
    } else {
        read_buf[n] = '\0';
        printf("✓ 读取 %d 字节: %s\n", n, read_buf);
    }
}

// 测试用例 5：poll 机制
void test_poll(void)
{
    struct pollfd pfd;
    int ret;

    printf("\n=== 测试 poll 机制 ===\n");

    pfd.fd = fd;
    pfd.events = POLLIN | POLLOUT;
    pfd.revents = 0;

    printf("等待设备可读或可写（3秒超时）...\n");

    ret = poll(&pfd, 1, 3000);
    if (ret < 0) {
        perror("poll 失败");
    } else if (ret == 0) {
        printf("✗ poll 超时\n");
    } else {
        printf("✓ poll 返回 %d\n", ret);
        if (pfd.revents & POLLIN) {
            printf("  设备可读\n");
        }
        if (pfd.revents & POLLOUT) {
            printf("  设备可写\n");
        }
        if (pfd.revents & POLLERR) {
            printf("  设备错误\n");
        }
    }
}

// 测试用例 6：异步通知
void *async_thread(void *arg)
{
    struct sigaction sa;
    int oflags;

    // 设置信号处理
    memset(&sa, 0, sizeof(sa));
    sa.sa_handler = async_callback;
    sa.sa_flags = 0;
    sigaction(SIGIO, &sa, NULL);

    // 设置异步通知
    fcntl(fd, F_SETOWN, getpid());
    oflags = fcntl(fd, F_GETFL);
    fcntl(fd, F_SETFL, oflags | FASYNC);

    printf("异步通知已启用，等待信号...\n");

    // 等待信号
    while (running) {
        pause();
    }

    return NULL;
}

// 主测试函数
int main(int argc, char **argv)
{
    pthread_t async_tid;
    int test_mode = 0;

    // 解析命令行参数
    if (argc > 1) {
        if (strcmp(argv[1], "all") == 0) {
            test_mode = 0;  // 全部测试
        } else if (strcmp(argv[1], "led") == 0) {
            test_mode = 1;  // 只测试 LED
        } else if (strcmp(argv[1], "button") == 0) {
            test_mode = 2;  // 只测试按键
        } else if (strcmp(argv[1], "async") == 0) {
            test_mode = 3;  // 只测试异步
        }
    }

    // 设置信号处理
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);

    // 打开设备
    printf("打开设备 /dev/led_button...\n");
    fd = open("/dev/led_button", O_RDWR);
    if (fd < 0) {
        perror("无法打开设备");
        return EXIT_FAILURE;
    }
    printf("✓ 设备打开成功 (fd=%d)\n", fd);

    // 运行测试用例
    switch (test_mode) {
    case 0:  // 全部测试
        test_led_control();
        test_button_read();
        test_button_wait();
        test_data_rw();
        test_poll();

        // 异步测试在后台运行
        pthread_create(&async_tid, NULL, async_thread, NULL);
        sleep(5);
        running = 0;
        pthread_join(async_tid, NULL);
        break;

    case 1:  // 只测试 LED
        test_led_control();
        break;

    case 2:  // 只测试按键
        test_button_read();
        test_button_wait();
        break;

    case 3:  // 只测试异步
        pthread_create(&async_tid, NULL, async_thread, NULL);
        printf("异步测试运行中，按 Ctrl+C 退出...\n");
        while (running) {
            sleep(1);
        }
        pthread_join(async_tid, NULL);
        break;
    }

    // 清理
    close(fd);
    printf("\n测试完成！\n");

    return EXIT_SUCCESS;
}
```

#### 2.7.3 自动化测试脚本

```bash
#!/bin/bash
# test_all.sh - 完整的驱动测试脚本

set -e  # 遇到错误立即退出

echo "=== LED 按键驱动完整测试 ==="
echo "开始时间: $(date)"
echo ""

# 1. 检查环境
echo "1. 检查编译环境..."
if [ ! -f "/lib/modules/$(uname -r)/build/Makefile" ]; then
    echo "错误: 内核构建目录不存在"
    exit 1
fi

# 2. 清理旧文件
echo "2. 清理旧编译文件..."
make clean

# 3. 编译驱动
echo "3. 编译驱动模块..."
make modules
if [ ! -f "led_button_driver.ko" ]; then
    echo "错误: 驱动编译失败"
    exit 1
fi
echo "✓ 驱动编译成功"

# 4. 编译测试程序
echo "4. 编译测试程序..."
make test_apps
if [ ! -f "led_button_test" ]; then
    echo "错误: 测试程序编译失败"
    exit 1
fi
echo "✓ 测试程序编译成功"

# 5. 加载驱动
echo "5. 加载驱动模块..."
sudo rmmod led_button_driver 2>/dev/null || true
sudo insmod led_button_driver.ko

# 检查是否加载成功
if ! lsmod | grep -q led_button_driver; then
    echo "错误: 驱动加载失败"
    dmesg | tail -20
    exit 1
fi
echo "✓ 驱动加载成功"

# 检查设备节点
sleep 1
if [ ! -e "/dev/led_button" ]; then
    echo "警告: 设备节点未自动创建，尝试手动创建..."
    sudo mknod /dev/led_button c $(cat /proc/devices | grep led_button | awk '{print $1}') 0
    sudo chmod 666 /dev/led_button
fi

if [ -e "/dev/led_button" ]; then
    echo "✓ 设备节点创建成功: /dev/led_button"
else
    echo "错误: 设备节点创建失败"
    exit 1
fi

# 6. 运行基本测试
echo "6. 运行基本功能测试..."
echo ""
sudo ./led_button_test led
echo "✓ LED 控制测试通过"

echo ""
sudo ./led_button_test button
echo "✓ 按键测试通过"

# 7. 运行高级测试
echo ""
echo "7. 运行高级功能测试..."
echo ""
sudo ./led_button_test all &
TEST_PID=$!

# 等待测试完成
sleep 10
if ps -p $TEST_PID > /dev/null; then
    echo "测试超时，强制终止..."
    kill -9 $TEST_PID 2>/dev/null
else
    wait $TEST_PID
    echo "✓ 完整测试通过"
fi

# 8. 压力测试
echo ""
echo "8. 运行压力测试..."
for i in {1..100}; do
    sudo ./led_button_test led >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "压力测试失败，第 $i 次迭代"
        break
    fi
    echo -n "."
    if [ $(($i % 50)) -eq 0 ]; then
        echo " $i"
    fi
done
echo ""
echo "✓ 压力测试通过（100 次迭代）"

# 9. 查看内核日志
echo ""
echo "9. 查看内核日志..."
echo "最后 20 条内核消息:"
dmesg | tail -20

# 10. 检查系统状态
echo ""
echo "10. 检查系统状态..."
echo "中断统计:"
cat /proc/interrupts | grep -E "(button|led_button)"

echo ""
echo "驱动信息:"
modinfo led_button_driver.ko | grep -E "(version|author|description)"

# 11. 清理
echo ""
echo "11. 清理测试环境..."
sudo rmmod led_button_driver
echo "✓ 驱动已卸载"

make clean
echo "✓ 编译文件已清理"

echo ""
echo "=== 所有测试完成 ==="
echo "结束时间: $(date)"
echo "测试结果: ✅ 通过"
```

## 三、调试技巧和问题排查

### 3.1 分层调试方法

```bash
#!/bin/bash
# debug_driver.sh - 分层调试脚本

echo "=== 驱动分层调试 ==="
echo ""

# 第 1 层：设备树调试
echo "1. 检查设备树..."
if [ -d "/proc/device-tree/led_button_device" ]; then
    echo "✓ 设备树节点存在"
    echo "  兼容性: $(cat /proc/device-tree/led_button_device/compatible)"
    echo "  状态: $(cat /proc/device-tree/led_button_device/status)"
else
    echo "✗ 设备树节点不存在"
    echo "  尝试重新加载设备树..."
    dtc -I dtb -O dts /boot/board.dtb > /tmp/current.dts
    if grep -q "led_button_device" /tmp/current.dts; then
        echo "  设备树节点已定义但未生效"
    else
        echo "  设备树节点未定义"
    fi
fi

echo ""

# 第 2 层：GPIO调试
echo "2. 检查 GPIO 状态..."
if [ -f "/sys/kernel/debug/gpio" ]; then
    echo "GPIO 状态:"
    grep -E "(led|button)" /sys/kernel/debug/gpio || echo "  未找到相关 GPIO"
else
    echo "✗ GPIO 调试文件不存在"
fi

echo ""

# 第 3 层：中断调试
echo "3. 检查中断状态..."
echo "中断统计:"
if grep -q "button" /proc/interrupts; then
    grep "button" /proc/interrupts
    IRQ_NUM=$(grep "button" /proc/interrupts | awk '{print $1}' | sed 's/://')
    echo "  中断号: $IRQ_NUM"
    if [ -f "/proc/irq/$IRQ_NUM/spurious" ]; then
        echo "  假中断计数: $(cat /proc/irq/$IRQ_NUM/spurious)"
    fi
else
    echo "✗ 未找到按键中断"
fi

echo ""

# 第 4 层：字符设备调试
echo "4. 检查字符设备..."
if [ -e "/dev/led_button" ]; then
    echo "✓ 设备节点存在"
    echo "  设备号: $(ls -l /dev/led_button | awk '{print $5,$6}')"
    echo "  权限: $(ls -l /dev/led_button | awk '{print $1}')"

    # 测试打开设备
    echo "  测试打开设备..."
    if timeout 1 cat /dev/led_button 2>&1 | grep -q "设备"; then
        echo "✓ 设备可正常访问"
    else
        echo "✗ 设备访问失败"
    fi
else
    echo "✗ 设备节点不存在"
    echo "  尝试创建设备节点..."
    MAJOR=$(grep led_button /proc/devices | awk '{print $1}')
    if [ ! -z "$MAJOR" ]; then
        sudo mknod /dev/led_button c $MAJOR 0
        sudo chmod 666 /dev/led_button
        echo "  已创建设备节点"
    else
        echo "  无法确定主设备号"
    fi
fi

echo ""

# 第 5 层：内核日志分析
echo "5. 分析内核日志..."
echo "最后 50 条相关日志:"
dmesg | grep -E "(led_button|gpio|irq)" | tail -50

echo ""
echo "=== 调试完成 ==="
```

### 3.2 常见问题排查表

| 问题现象           | 可能原因       | 排查步骤                   | 解决方法            |
| ------------------ | -------------- | -------------------------- | ------------------- |
| **insmod 失败**    | 内核版本不匹配 | 查看 dmesg 错误信息        | 使用正确内核编译    |
|                    | 依赖缺失       | 检查内核版本               | 按顺序加载依赖模块  |
|                    | 符号未导出     | 查看模块依赖               | 导出需要的符号      |
| **设备节点不存在** | 驱动未注册成功 | 检查 `/proc/devices`       | 手动 mknod 创建设备 |
|                    | udev 规则问题  | 查看内核日志               | 修改 udev 规则      |
|                    | 权限问题       | 检查 devtmpfs              | 检查驱动注册代码    |
| **GPIO 无法控制**  | GPIO 号错误    | 检查设备树配置             | 修正设备树 GPIO 号  |
|                    | 方向设置错误   | 使用 `gpiodetect` 验证     | 确认 GPIO 方向      |
|                    | 时钟未使能     | 查看硬件手册               | 检查时钟配置        |
| **中断不触发**     | 中断号错误     | 查看 `/proc/interrupts`    | 修正中断配置        |
|                    | 触发方式错误   | 检查设备树 interrupts 属性 | 检查中断控制器      |
|                    | 中断被屏蔽     | 使用示波器验证信号         | 验证硬件连接        |
| **读写操作阻塞**   | 缓冲区满/空    | 检查缓冲区状态             | 调整缓冲区大小      |
|                    | 等待队列未唤醒 | 查看等待队列               | 正确使用唤醒函数    |
|                    | 锁未释放       | 使用 lockdep 检查死锁      | 修复锁的使用        |
| **系统崩溃/死锁**  | 内存越界       | 使用 kasan 检查内存        | 修复内存访问        |
|                    | 中断上下文错误 | 分析内核转储               | 避免中断中睡眠      |
|                    | 锁使用不当     | 使用 lockdep               | 正确使用锁          |

### 3.3 性能优化技巧

```cpp
// 1. 使用 DMA 缓冲区减少拷贝
static int optimize_with_dma(struct device *dev)
{
    dma_addr_t dma_handle;
    void *buffer;

    // 分配 DMA 缓冲区
    buffer = dma_alloc_coherent(dev, BUFFER_SIZE, &dma_handle, GFP_KERNEL);
    if (!buffer) {
        return -ENOMEM;
    }

    // 使用 DMA 传输
    dma_map_single(dev, buffer, BUFFER_SIZE, DMA_TO_DEVICE);

    // ... 操作完成后
    dma_unmap_single(dev, dma_handle, BUFFER_SIZE, DMA_TO_DEVICE);
    dma_free_coherent(dev, BUFFER_SIZE, buffer, dma_handle);

    return 0;
}

// 2. 优化中断处理延迟
static irqreturn_t low_latency_irq_handler(int irq, void *dev_id)
{
    struct device_data *data = dev_id;

    // 快速处理：只记录时间戳
    data->irq_timestamp = ktime_get_ns();

    // 延迟处理放到工作队列
    queue_work(system_highpri_wq, &data->work);

    return IRQ_HANDLED;
}

// 3. 使用 RCU 保护只读数据
static struct config_data *global_config;

static void update_config(struct config_data *new_config)
{
    struct config_data *old_config;

    rcu_read_lock();
    old_config = rcu_dereference(global_config);
    rcu_assign_pointer(global_config, new_config);
    synchronize_rcu();
    kfree(old_config);
    rcu_read_unlock();
}

// 4. 批量处理减少系统调用开销
static ssize_t batch_write(struct file *filp, const char __user *buf,
                          size_t count, loff_t *f_pos)
{
    struct iov_iter iter;
    struct iovec iov = {
        .iov_base = (void __user *)buf,
        .iov_len = count,
    };

    iov_iter_init(&iter, WRITE, &iov, 1, count);
    return drv_write_iter(filp, &iter, f_pos);
}
```

## 四、总结和最佳实践

### 4.1 开发流程回顾

1. **硬件分析**（1-2 天）

   - 查看原理图和硬件手册
   - 确定硬件连接和接口
   - 规划所需的软件资源

2. **设备树配置**（1 天）

   - 编写设备树节点
   - 定义硬件属性和中断
   - 编译和加载设备树

3. **GPIO 驱动实现**（1-2 天）

   - 实现 GPIO 初始化和控制
   - 添加必要的同步机制
   - 测试基本的硬件控制

4. **中断驱动实现**（1-2 天）

   - 注册中断处理函数
   - 实现中断消抖和下半部处理
   - 测试中断触发和处理

5. **字符设备实现**（2-3 天）

   - 实现文件操作接口
   - 添加高级功能（poll、异步通知等）
   - 测试用户空间接口

6. **整合和测试**（2-3 天）

   - 整合所有组件
   - 编写测试程序
   - 进行完整的功能和压力测试

7. **优化和调试**（持续）
   - 性能优化
   - 稳定性测试
   - 问题修复

### 4.2 关键注意事项

1. **内存管理**

   - 使用 `devm_` 系列函数自动管理资源
   - 检查所有内存分配的错误情况
   - 避免内存泄漏和悬空指针

2. **并发控制**

   - 正确使用锁保护共享数据
   - 区分中断上下文和进程上下文
   - 避免死锁和优先级反转

3. **错误处理**

   - 所有函数都要有适当的错误处理
   - 提供有意义的错误信息
   - 实现完整的资源清理

4. **兼容性**
   - 支持多种硬件变体
   - 保持向后兼容性
   - 遵循内核编码规范

### 4.3 推荐的调试工具

| 工具       | 用途         | 示例命令                                                   |
| ---------- | ------------ | ---------------------------------------------------------- |
| **dmesg**  | 查看内核日志 | `dmesg -w`                                                 |
| **strace** | 跟踪系统调用 | `strace -p <pid>`                                          |
| **perf**   | 性能分析     | `perf record -g <command>`                                 |
| **ftrace** | 内核函数跟踪 | `echo function > /sys/kernel/debug/tracing/current_tracer` |
| **kgdb**   | 内核调试     | `kgdboc=ttyS0,115200`                                      |
| **sysrq**  | 系统请求     | `echo t > /proc/sysrq-trigger`                             |
| **/proc**  | 系统信息     | `cat /proc/interrupts`                                     |
| **/sys**   | 内核对象     | `ls /sys/class/gpio/`                                      |

### 4.4 下一步学习建议

1. **深入学习内核机制**

   - 内存管理（slab、vmalloc、DMA）
   - 进程调度和实时性
   - 电源管理和休眠唤醒

2. **掌握更多驱动类型**

   - 网络设备驱动
   - USB 设备驱动
   - 输入子系统驱动
   - 显示和 GPU 驱动

3. **性能优化技巧**

   - 使用 DMA 和零拷贝
   - 优化中断延迟
   - 多核并行处理

4. **参与开源社区**
   - 阅读内核源码
   - 提交补丁和修复
   - 参与邮件列表讨论

通过这个完整的驱动开发流程，您应该能够：

- ✅ 理解驱动开发的整体架构
- ✅ 掌握设备树、GPIO、中断、字符设备的开发方法
- ✅ 能够独立开发和调试完整的驱动
- ✅ 具备解决实际问题的能力

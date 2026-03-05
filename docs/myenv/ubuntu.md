# Ubuntu

## 安装中文输入法

```bash
sudo apt update
sudo apt install ibus-libpinyin -y # 安装 iBUS
im-config -n ibus                  # 设置为默认输入法
sudo apt install fonts-noto-cjk -y # 安装中文字体
reboot
```

# Autoconf

## 使用方法

```bash
cd /path/to/src && autoreconf -vi

cd /path/to/src && ./configure \
--build=i686-pc-linux-gnu \
--target=aarch64-linux \
--host=aarch64-linux \

make -C /path/to/src
make -C /path/to/src install
```

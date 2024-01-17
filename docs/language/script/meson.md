# Meson

## 使用方法

```bash
cat <<EOF | tee /path/to/aarch64-linux.ini
[constants]
sdk_dir = '/path/to/sdk'
sysroot_dir = sdk_dir + '/sysroot'
toochain_dir = sysroot_dir + '/usr/bin'
crosstools_prefix = toolchain_dir + '/aarch64-linux-'

[binaries]
c = crosstools_prefix + 'gcc'
cpp = crosstools_prefix + 'g++'
strip = crosstools_prefix + 'strip'
pkgconfig = 'pkg-config'

[build-in options]
has_function_print = true
has_function_hfkerhisadf = false
allow_default_for_cross = true

[host_machine]
system = 'linux'
cpu_family = 'arm'
cpu = 'cortex-a9'
endian = 'little'

[build_machine]
system = 'linux'
cpu_family = 'x86_64'
cpu = 'i686'
EOF
```

```bash
export CMAKE := /path/to/bin/cmake

export PKG_CONFIG_PATH :=
export PKG_CONFIG_LIBDIR := /path/to/usr/lib/pkgconfig:/path/to/usr/share/pkgconfig
export PKG_CONFIG_SYSROOT_DIR := /path/to/sysroot

CURR_DIR := $(shell pwd)

meson build_dir \
--prefix=$(CURR_DIR) \
--build-type=plain \
--cross-file /path/to/aarch64-linux.ini

cd build_dir && meson compile -C output_dir

meson install -C output_dir
```

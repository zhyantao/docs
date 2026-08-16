# venv

`venv` 是 Python 3 自带的创建虚拟环境的工具（Python 3.3+）。它允许你在自己的电脑上同时存在多个 Python 环境，各环境之间互不干扰。

## 准备工作：安装 pip

```bash
# 通常系统自带的 Python 3 已包含 pip 和 venv
python3 -m pip --version

# 如果没有 pip，可以通过以下方式安装
curl https://bootstrap.pypa.io/get-pip.py | python3
```

## 创建 venv 环境

```bash
python3 -m venv ~/venv/python3
```

## 激活 venv 环境

```bash
source ~/venv/python3/bin/activate
```

激活后命令行提示符前会显示 `(python3)`，此时 `python` 和 `pip` 都指向虚拟环境中的版本。

## 关闭 venv 环境

```bash
deactivate
```

## 删除 venv 环境

```bash
rm -rf ~/venv/python3
```

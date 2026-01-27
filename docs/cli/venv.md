# venv

virtualenv 是创建 Python 隔离环境的一个工具。它允许你在自己的电脑上同时存在多个 Python 版本，而又互不干扰。

## 准备工作：安装 pip

```bash
curl https://bootstrap.pypa.io/get-pip.py | python
```

## 创建 virtualenv 环境

```bash
# for python3
python3 -m venv ~/venv/python3

# for python2
pip install virtualenv
virtualenv -p python2.7 ~/venv/python2
```

## 激活 virtualenv 环境

```bash
source ~/venv/python3/bin/activate
```

## 关闭 virtualenv 环境

```bash
deactivate
```

## 删除 virtualenv 环境

```bash
rm -rf ~/venv/python3
```

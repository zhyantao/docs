# 用 NPU 训练神经网络

## 检查是否支持 NPU

```bash
pip install openvino
python -c "from openvino import Core; print(Core().available_devices)"
```

```{dropdown}
['CPU', 'GPU', 'NPU']
```

## 下载和运行示例代码

```bash
git clone https://github.com/openvinotoolkit/openvino_notebooks
```

在 Windows 上安装环境：<https://github.com/openvinotoolkit/openvino_notebooks/wiki/Windows>

将示例代码中运行实例的载体改为 NPU：

```python
device = widgets.Dropdown(
    options=core.available_devices + ["AUTO"],
    value='NPU',  # 改为 NPU 既可使用 NPU 资源
    description='Device:',
    disabled=False,
)
```

## 观察实验结果

```{figure} ../_static/images/intel-ai-boost.png
```
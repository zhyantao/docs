# JMatPro 二次开发

JMatPro 是一个用于预测材料性能的软件。
它可以基于预存于软件内部的专家经验规则来预测材料的物理性能，比如导热系数等。

JMatPro 主要用来做相图计算。包括平衡相图和非平衡相图。在使用软件时，一般按照如下步骤进行：

1. 选择数据库 Meterial Types
2. 设置合金成分（保存成分）
3. 设置窗口右侧参数
4. 按软件提示完成后续流程

针对连铸项目，因为中重院只购买了通用钢模块和不锈钢模块，所以我们仅考虑 General Steel 和
Stainless Steel 的相关功能。

```{image} ../../../_static/images/JMatPro_CerzEekEK8.png
:name: jmatpro_main_page
```

2021年11月26日，经过讨论，发现 JMatPro 软件存在一些缺陷：

- 硅（Si）含量超过 3 后，无法计算凝固非平衡相图。需要确定在数学模型中有没有上下限的限制。
- 钢种规则库是有限的，对于新出现的成分，出现无法计算的情况。
- 凝固过程中的平衡相图和非平衡相图是一样的，这有违常识。

我们希望经过二次开发，实现 **一键连铸**，能够用一次鼠标点击操作，完成后续的操作。

从开始计算到控制 PLC 上位机一共需要 5 秒钟，因此，理想的并行计算速度和渲染时间应该控制在 3 秒左右。
现在初步可供参考的思路有：

- 变网格划分，提高计算效率。温度变化大的地方更细致地划分。
- 只计算中间 1 维厚度方向的温度来确定喷水量，因为只有这个位置有喷嘴。
  如果有幅切，可以多计算两路厚度方向，确定两外两路喷嘴的喷水量。
- $\Delta t$ 确定收敛条件，不用每次都去计算，选择最小值即可。
  收敛条件是指对于一个晶粒来讲，其与四邻域不在发生热交换。
  热交换公式比较复杂，不再研究了，需要知道的是，这和 $\Delta t$ 有关。

跟中重院聊天时，他们不关心实现细节，只需要讲明白，用什么方法，效率提高了多少，代价是多少就可以了。

因为对计算速度有要求，可以考虑使用内存型数据库 Redis 来设计数据库的存储和交互。

甲方提问：网页的渲染速度不知到能不能办到，能不能实时获取信局部信息？

初始温度由中间包确定。可以实时获取。

设计出来的 UI 要能够展示单流、双流、三流的温度场。

需求包括：下发参数后，输入和输出怎么呈现，画面展示一下。
计划做成什么样子，要跟甲方交流一下，方便确认需求是否正确。数据流程要完整，具体实现细节可以省略。

二次开发支持使用 C++ 或 Python 来调用官方的[开放接口](https://www.sentesoftware.co.uk/jmatpro-api)。

在配置环境时，若缺少加密狗，则无法继续完成后续工作，
参考[JMatPro API 安装与开发环境配置指南](https://kdocs.cn/l/cd3ZKiq03jt1)。错误提示如下图所示：

```{image} ../../../_static/images/jmatpro_err_1.png
```

## Thermodynamic Properties

基于该软件进行二次开发，现在又没有加密狗，所以无法调通程序，现在仅根据 UI 界面的输出梳理导出数据的格式。

JMatPro 7.0 通用钢模块共包含 7 个板块：

- Thermodynamic Properties：热力学计算
- Solidification：凝固计算
- Thermo-Physical Properties：热物性能计算
- Mechanical Properties：力学性能计算
- Phase Transformation：相转变动力学计算
- Data Export：数据导出
- Others：其他

热力学计算模块，从{ref}`主界面 <jmatpro_main_page>`上可以看出，有下面这几个功能：

- Step Temperature：设定起始温度、终止温度和步长的情况下，XXX 随温度变化曲线
- Step Concentration： 固定温度下，XXX 随 YYY 浓度变化曲线
- Profile：固定温度下和浓度区间下的 XXX 随铁素体含量变化曲线
- Single：单一温度下各相百分比含量

下面以钢种 `10CrMoV` 为例，仔细分析一下，每个计算模块分别需要输入什么参数，都能得到什么结果。

### Step Temperature

首先我们输入参数：

```{figure} ../../../_static/images/jmatpro_step_temperature_params.png
Step Temperature 输入参数
```

能够得到的所有数据如下：（输出）

```{code-block} text
10CrMoV_%Ph_Wt%_Phase.dat                   各个相的质量百分比随温度变化曲线
10CrMoV_EI_Wt%_C.dat                        各个相的碳元素质量百分比随温度变化曲线
10CrMoV_EI_Wt%_CR.dat                       各个相的铬元素质量百分比随温度变化曲线
10CrMoV_EI_Wt%_FE.dat                       各个相的铁元素质量百分比随温度变化曲线
10CrMoV_EI_Wt%_MN.dat                       各个相的锰元素质量百分比随温度变化曲线
10CrMoV_EI_Wt%_MO.dat                       各个相的钼元素质量百分比随温度变化曲线
10CrMoV_EI_Wt%_NB.dat                       各个相的铌元素质量百分比随温度变化曲线
10CrMoV_EI_Wt%_NI.dat                       各个相的镍元素质量百分比随温度变化曲线
10CrMoV_EI_Wt%_V.dat                        各个相的钒元素质量百分比随温度变化曲线

10CrMoV_Alpha_Activity.dat                  各个钢种成分的激活能随温度变化曲线
10CrMoV_Ph_Wt%_Element_in_AUSTENITE.dat     各个钢种成分的奥氏体质量百分比随温度变化曲线
10CrMoV_Ph_Wt%_Element_in_FERRITE.dat       各个钢种成分的铁素体质量百分比随温度变化曲线
10CrMoV_Ph_Wt%_Element_in_LAVES.dat         各个钢种成分的拉弗斯相质量百分比随温度变化曲线
10CrMoV_Ph_Wt%_Element_in_LIQUID.dat        各个钢种成分的液相质量百分比随温度变化曲线
10CrMoV_Ph_Wt%_Element_in_M(C,N).dat        各个钢种成分的碳氮混合物质量百分比随温度变化曲线
10CrMoV_Ph_Wt%_Element_in_M23C6.dat         各个钢种成分的 M23C6 质量百分比随温度变化曲线

10CrMoV_DeltaG_Partial_Gibbs_Energy.dat     各个相的吉布斯自由能随温度变化曲线
10CrMoV_G_Gibbs_Energy.dat                  钢水的总吉布斯自由能随温度变化曲线

10CrMoV_Cp_Heat_Capacity.dat                钢水的比热容随温度变化曲线
10CrMoV_H_Enthalpy.dat                      钢水的焓随温度变化曲线
10CrMoV_S_Entropy.dat                       钢水的熵随温度变化曲线

10CrMoV_T_Wt%_Phase_SingleTemperatureAnalysis_1166F.dat 在 1166 华氏度下各个相的百分比分布
```

我对这些文件的命名规则是这样的：`钢种名称_UI界面按钮名称_纵轴含义`，它们的横轴都是温度。
如果想打开这些文件，通过直接改文件后缀的方式也可以，把 `dat` 改为 `xls`。

补充知识：`Wt%` 是重量（质量）百分数的单位，表示重量比及一种物质占混合物的比重。

- 上面的 `各个相` 表示的是 `'LIQUID' 'FERRITE' 'M(C,N)' 'AUSTENITE' 'M23C6' 'LAVES'`
- 上面的 `各个钢种成分` 表示的是 `'FE' 'CR' 'MN' 'MO' 'NB' 'NI' 'V' 'C'` 因为 `10CrMoV` 只有这几个成分。
- 上面的 `钢水` 指的是这些总体构成的混合物。

### Step Concentration

```{figure} ../../../_static/images/jmatpro_step_concentration_params.png
Step Concentration 输入参数
```

我们会得到和 `Step Temperature` 一样的文件，区别就是，它的相成分少了 `LAVES`。

### Profile Calculation

```{figure} ../../../_static/images/jmatpro_profile_calculation_params.png
Profile Calculation 输入参数
```

同样我们会得到和 `Step Temperature` 一样的文件，而且，它的相成分更少了，只有 `AUSTENITE` 和 `M(C,N)`。

### Single Calculation

```{figure} ../../../_static/images/jmatpro_single_calculation_params.png
Single Calculation 输入参数
```

这其实是一个很鸡肋的功能，它其实就是 `10CrMoV_T_Wt%_Phase_SingleTemperatureAnalysis_????F.dat`。

## Solidification

### Solidification Properties

输入：

```{figure} ../../../_static/images/jmatpro_solification_calculation_params.png
Solidification Calculation 输入参数
```

通过这个计算模块，我们可以得到下面这些文件：

```{code-block} text
10CrMoV_Average_expansion_coeff.xls
10CrMoV_Bulk_modulus.xls
10CrMoV_Density.xls
10CrMoV_Electrical_conducitivity.xls
10CrMoV_Electrical_resistivity.xls
10CrMoV_Enthalpy.xls
10CrMoV_Hardness.xls
10CrMoV_Latent_heat.xls
10CrMoV_Linear_expression.xls
10CrMoV_Liquid_viscosity.xls
10CrMoV_Molar_volume.xls
10CrMoV_Phase_vol%.xls
10CrMoV_Poisson's_ratio.xls
10CrMoV_Shear_modulus.xls
10CrMoV_Specific_heat.xls
10CrMoV_Tensile_Stress.xls
10CrMoV_Thermal_conductivity.xls
10CrMoV_Total_viscosity.xls
10CrMoV_Yield_Stress.xls
10CrMoV_Young's_modulus.xls
```

但是，当我打开这些文件查看内容的时候，**它们的内容其实都是一样的**。因为我选择的数据全部导出。

这个计算模块支持导出到一些第三方软件，比如 Deform，但是对于数据点数有要求，不支持导出太多数据点。

后面，我又尝试了导出包含各个相的全部数据，没错，果然不出意外，它们的内容也是一样的。

```{code-block} text
10CrMoV_Density_per_phase.xls
10CrMoV_Phase_vol%_per_phase.xls
```

需要了解，JMatPro 在 Solidification 这个计算模块，不是只能导出全部数据，你也可以选择部分导出。

鉴于上面的分析，得出结论，Solidification 这个计算模块只需要分析两张表的表头就可以了。
而且，第一张表是第二张表的子集，因此，直接只对第二张表做分析就可以了。

```{code-block} text
Phases vol%-LIQUID-1.0(C/s)                         液相体积百分比随温度变化曲线
Phases vol%-AUSTENITE-1.0(C/s)                      奥氏体体积百分比随温度变化曲线
Phases vol%-FERRITE-1.0(C/s)                        铁素体体积百分比随温度变化曲线
Phases vol%-MARTENSITE-1.0(C/s)                     马氏体体积百分比随温度变化曲线

Density (g/(cm)^3)-BAINITE_PEARLITE-1.0(C/s)        钢水的珠光体和贝氏体密度随温度变化曲线
Density (g/(cm)^3)-LIQUID-1.0(C/s)                  钢水的液相密度随温度变化曲线
Density (g/(cm)^3)-AUSTENITE-1.0(C/s)               钢水的奥氏体密度随温度变化曲线
Density (g/(cm)^3)-FERRITE-1.0(C/s)                 钢水的铁素体密度随温度变化曲线
Density (g/(cm)^3)-MARTENSITE-1.0(C/s)              钢水的马氏体密度随温度变化曲线
Density (g/(cm)^3)-TOTAL-1.0(C/s)                   钢水的总密度随温度变化曲线

Molar volume (cm^3)-BAINITE_PEARLITE-1.0(C/s)
Molar volume (cm^3)-LIQUID-1.0(C/s)
Molar volume (cm^3)-AUSTENITE-1.0(C/s)
Molar volume (cm^3)-FERRITE-1.0(C/s)
Molar volume (cm^3)-MARTENSITE-1.0(C/s)
Molar volume (cm^3)-TOTAL-1.0(C/s)                  钢水的摩尔体积随温度变化曲线

Linear expansion (%)-  -1.0(C/s)                    钢水的线膨胀系数随温度变化曲线
Average expansion coeff. (10e-6 1/K)-  -1.0(C/s)    钢水的平均膨胀系数随温度变化曲线

Thermal conductivity (W/(m*K))-BAINITE_PEARLITE-1.0(C/s)
Thermal conductivity (W/(m*K))-LIQUID-1.0(C/s)
Thermal conductivity (W/(m*K))-AUSTENITE-1.0(C/s)
Thermal conductivity (W/(m*K))-FERRITE-1.0(C/s)
Thermal conductivity (W/(m*K))-MARTENSITE-1.0(C/s)
Thermal conductivity (W/(m*K))-TOTAL-1.0(C/s)       钢水的热传导率随温度变化曲线

Electrical resistivity (10e-6 Ohm*m)-BAINITE_PEARLITE-1.0(C/s)
Electrical resistivity (10e-6 Ohm*m)-LIQUID-1.0(C/s)
Electrical resistivity (10e-6 Ohm*m)-AUSTENITE-1.0(C/s)
Electrical resistivity (10e-6 Ohm*m)-FERRITE-1.0(C/s)
Electrical resistivity (10e-6 Ohm*m)-MARTENSITE-1.0(C/s)
Electrical resistivity (10e-6 Ohm*m)-TOTAL-1.0(C/s)     钢水的电阻率随温度变化曲线

Electrical conductivity (10e6 1/(Ohm*m))-BAINITE_PEARLITE-1.0(C/s)
Electrical conductivity (10e6 1/(Ohm*m))-LIQUID-1.0(C/s)
Electrical conductivity (10e6 1/(Ohm*m))-AUSTENITE-1.0(C/s)
Electrical conductivity (10e6 1/(Ohm*m))-FERRITE-1.0(C/s)
Electrical conductivity (10e6 1/(Ohm*m))-MARTENSITE-1.0(C/s)
Electrical conductivity (10e6 1/(Ohm*m))-TOTAL-1.0(C/s) 钢水的电导率随温度变化曲线

Young's modulus (GPa)-BAINITE_PEARLITE-1.0(C/s)
Young's modulus (GPa)-LIQUID-1.0(C/s)
Young's modulus (GPa)-AUSTENITE-1.0(C/s)
Young's modulus (GPa)-FERRITE-1.0(C/s)
Young's modulus (GPa)-MARTENSITE-1.0(C/s)
Young's modulus (GPa)-TOTAL-1.0(C/s)                钢水的杨氏模量随温度变化曲线

Bulk modulus (GPa)-BAINITE_PEARLITE-1.0(C/s)
Bulk modulus (GPa)-LIQUID-1.0(C/s)
Bulk modulus (GPa)-AUSTENITE-1.0(C/s)
Bulk modulus (GPa)-FERRITE-1.0(C/s)
Bulk modulus (GPa)-MARTENSITE-1.0(C/s)
Bulk modulus (GPa)-TOTAL-1.0(C/s)                   钢水的体积模量随温度变化曲线

Shear modulus(GPa)-BAINITE_PEARLITE-1.0(C/s)
Shear modulus(GPa)-LIQUID-1.0(C/s)
Shear modulus(GPa)-AUSTENITE-1.0(C/s)
Shear modulus(GPa)-FERRITE-1.0(C/s)
Shear modulus(GPa)-MARTENSITE-1.0(C/s)
Shear modulus(GPa)-TOTAL-1.0(C/s)                   钢水的剪切模量随温度变化曲线

Poisson's ratio-BAINITE_PEARLITE-1.0(C/s)
Poisson's ratio-LIQUID-1.0(C/s)
Poisson's ratio-AUSTENITE-1.0(C/s)
Poisson's ratio-FERRITE-1.0(C/s)
Poisson's ratio-MARTENSITE-1.0(C/s)
Poisson's ratio-TOTAL-1.0(C/s)                      钢水的泊松比随温度变化曲线

Liquid viscosity (mPa s)-  -1.0(C/s)
Total viscosity (mPa s)-  -1.0(C/s)                 钢水的粘度随温度变化曲线

Yield Stress (MPa)-TOTAL-1.0(C/s)                   钢水的屈服强度随温度变化曲线
Yield Stress (MPa)-MARTENSITE-1.0(C/s)
Yield Stress (MPa)-AUSTENITE-1.0(C/s)

Tensile Stress (MPa)-TOTAL-1.0(C/s)                 钢水的拉抗强度随温度变化曲线

Hardness (HRC)-TOTAL-1.0(C/s)                       坯壳硬度随温度变化曲线

Enthalpy (J/g)-TOTAL-1.0(C/s)                       钢水的焓随温度变化曲线
Enthalpy (J/g)-AUSTENITE-1.0(C/s)
Enthalpy (J/g)-FERRITE-1.0(C/s)
Enthalpy (J/g)-BAINITE_PEARLITE-1.0(C/s)
Enthalpy (J/g)-MARTENSITE-1.0(C/s)

Specific heat (J/(g K))-TOTAL-1.0(C/s)              钢水的比热容随温度变化曲线
Specific heat (J/(g K))-AUSTENITE-1.0(C/s)
Specific heat (J/(g K))-FERRITE-1.0(C/s)
Specific heat (J/(g K))-BAINITE_PEARLITE-1.0(C/s)
Specific heat (J/(g K))-MARTENSITE-1.0(C/s)

Latent heat (J/g)-FERRITE-1.0(C/s)                  钢水的潜热随温度变化曲线
Latent heat (J/g)-BAINITE_PEARLITE-1.0(C/s)
Latent heat (J/g)-MARTENSITE-1.0(C/s)
Latent heat (J/g)-SOLID-1.0(C/s)

TIME(s)-Cooling_1.0(C/s)                            已经经过的时间随温度变化曲线
```

## Thermo-Physical Properties

### Extended General

输入：

```{figure} ../../../_static/images/jmatpro_extended_general_params.png
Extended General 输入参数
```

无独有偶，这个模块跟 Solidification 模块的十分相似，因此，只分析总表：

```{code-block} text
Phases wt%-LIQUID           液相质量百分比随温度变化曲线
Phases wt%-FERRITE          
Phases wt%-M(C,N)
Phases wt%-AUSTENITE
Phases wt%-M23C6
Phases wt%-LAVES

Density (g/(cm)^3)-LIQUID
Density (g/(cm)^3)-FERRITE
Density (g/(cm)^3)-M(C,N)
Density (g/(cm)^3)-AUSTENITE
Density (g/(cm)^3)-M23C6
Density (g/(cm)^3)-LAVES
Density (g/(cm)^3)-TOTAL

Molar volume (cm^3)-LIQUID
Molar volume (cm^3)-FERRITE
Molar volume (cm^3)-M(C,N)
Molar volume (cm^3)-AUSTENITE
Molar volume (cm^3)-M23C6
Molar volume (cm^3)-LAVES
Molar volume (cm^3)-TOTAL

Average expansion coeff. (10e-6 1/K)-  
Linear expansion (%)-  

Thermal conductivity (W/(m*K))-LIQUID
Thermal conductivity (W/(m*K))-FERRITE
Thermal conductivity (W/(m*K))-M(C,N)
Thermal conductivity (W/(m*K))-AUSTENITE
Thermal conductivity (W/(m*K))-M23C6
Thermal conductivity (W/(m*K))-LAVES
Thermal conductivity (W/(m*K))-TOTAL

Electrical resistivity (10e-6 Ohm*m)-LIQUID
Electrical resistivity (10e-6 Ohm*m)-FERRITE
Electrical resistivity (10e-6 Ohm*m)-M(C,N)
Electrical resistivity (10e-6 Ohm*m)-AUSTENITE
Electrical resistivity (10e-6 Ohm*m)-M23C6
Electrical resistivity (10e-6 Ohm*m)-LAVES
Electrical resistivity (10e-6 Ohm*m)-TOTAL

Electrical conductivity (10e6 1/(Ohm*m))-LIQUID
Electrical conductivity (10e6 1/(Ohm*m))-FERRITE
Electrical conductivity (10e6 1/(Ohm*m))-M(C,N)
Electrical conductivity (10e6 1/(Ohm*m))-AUSTENITE
Electrical conductivity (10e6 1/(Ohm*m))-M23C6
Electrical conductivity (10e6 1/(Ohm*m))-LAVES
Electrical conductivity (10e6 1/(Ohm*m))-TOTAL

Young's modulus (GPa)-LIQUID
Young's modulus (GPa)-FERRITE
Young's modulus (GPa)-M(C,N)
Young's modulus (GPa)-AUSTENITE
Young's modulus (GPa)-M23C6
Young's modulus (GPa)-LAVES
Young's modulus (GPa)-TOTAL

Bulk modulus (GPa)-LIQUID
Bulk modulus (GPa)-FERRITE
Bulk modulus (GPa)-M(C,N)
Bulk modulus (GPa)-AUSTENITE
Bulk modulus (GPa)-M23C6
Bulk modulus (GPa)-LAVES
Bulk modulus (GPa)-TOTAL

Shear modulus(GPa)-LIQUID
Shear modulus(GPa)-FERRITE
Shear modulus(GPa)-M(C,N)
Shear modulus(GPa)-AUSTENITE
Shear modulus(GPa)-M23C6
Shear modulus(GPa)-LAVES
Shear modulus(GPa)-TOTAL

Poisson's ratio-LIQUID
Poisson's ratio-FERRITE
Poisson's ratio-M(C,N)
Poisson's ratio-AUSTENITE
Poisson's ratio-M23C6
Poisson's ratio-LAVES
Poisson's ratio-TOTAL

Liquid viscosity (mPa s)-  
Total viscosity (mPa s)-  

Liquid diffusivity (10e-9 (m^2)/s)-  
Total diffusivity (10e-9 (m^2)/s)-      钢水的扩散率随温度变化曲线

Surface Tension (mN/m)-                 钢水的表面张力随温度变化曲线

Enthalpy (J/g)-TOTAL

Specific heat (J/(g K))-TOTAL
```

### Dynamic

其实感觉功能是重复了。输入界面长下面的样子：

```{figure} ../../../_static/images/jmatpro_dynamic_params.png
Dynamic 输入参数
```

### Stacking Fault Energy

层错能随温度变化曲线，这个输出很简单，只有一列有效数据，就是层错能。

```{figure} ../../../_static/images/jmatpro_stacking_fault_energy_params.png
Stacking Fault Energy 输入参数
```

### Magentic Permeability

磁导率随温度变化曲线，这个输出很简单，只有一列有效数据，就是磁导率。

```{figure} ../../../_static/images/jmatpro_magnetic_permeability_params.png
Stacking Fault Energy 输入参数
```

## Mechanical Properties

### Jominy Hardenability

拉力随距离的变化曲线、硬度随距离的变化曲线、各相百分比随距离的变化曲线。

这里的各相指的是铁素体、珠光体、贝氏体、马氏体、奥氏体。

```{figure} ../../../_static/images/jmatpro_jominy_hardenability_params.png
Jominy Hardenability 输入参数
```

### High Temperature Strength

高温强度随温度变化曲线，这个输出很简单，只有一列有效数据，就是高温强度。

```{figure} ../../../_static/images/jmatpro_high_temperature_strength_params.png
High Temperature Strength 输入参数
```

### Flow Stress Analysis

不同温度下，流动应力随应变的变化曲线。

```{figure} ../../../_static/images/jmatpro_Flow_Stress_Analysis_params.png
Flow Stress Analysis 输入参数
```

### Fatigue Related

Total Strain - Number of cycles 曲线，应变随？变化曲线

```{figure} ../../../_static/images/jmatpro_fatigue_related_params.png
Fatigue Related 输入参数
```

### Tempered Martensite

该计算模块分别计算了屈服应力随温度变化曲线、拉应力随温度变化曲线、硬度随温度变化曲线。

```{figure} ../../../_static/images/jmatpro_tempering_of_mertensite_structure_params.png
Tempered Martensite 输入参数
```

## Phase transformation

### TTT/CCT Diagram

各相的温度随时间的变化曲线。

```{figure} ../../../_static/images/jmatpro_ttt_cct_params.png
TTT/CCT Diagram 输入参数
```

### Quench Properties

淬火性能计算。

输入：

```{figure} ../../../_static/images/jmatpro_quench_properties_params.png
Quench Properties 输入参数
```

这个计算模块跟 Solidification Properties 模块的结果很像，不再赘述。

### Welding Cycle

焊接热循环计算。

输入：

```{figure} ../../../_static/images/jmatpro_welding_cycles_params.png
Welding Cycle 输入参数
```

这个计算模块跟 Solidification Properties 模块的结果很像，不再赘述。

### Martensite

马氏体转变温度计算，计算马氏体、奥氏体、Md(50/30) 随温度变化曲线

### Energy Changes

计算奥氏体转为其他相态时，吉布斯能随温度变化的曲线 和 焓差随温度变化的曲线。

### Simultaneous Precipitation

计算各相的百分比随时间变化的曲线，以及晶粒大小随时间变化的曲线。

这里的各相指的是 M3C、M2(C,N)、M(C,N)、M23C6、M7C3、M5C、LAVES。

### Reaustenisation

二次奥氏体化计算。

各相或晶粒大小随温度或时间的变化曲线。

这里的各相指的是 Austenite、Ferrite、Pearlite。

### TTA Diagram

温度随时间的变化曲线，以及温度随升温速率的变化曲线

### Transformation Plasticity

输入参数：

```{figure} ../../../_static/images/jmatpro_transformation_plasticity_params.png
Transformation Plasticity 输入参数
```

相变塑性参数计算。

分别计算在 `Factor = Leblond | Greenwood-Johnson | Other` 的情况下：

铁素体、贝氏体和珠光体、马氏体随温度的变化曲线。

### Advanced CCT

输入：

```{figure} ../../../_static/images/jmatpro_advanced_ttt_params.png
Transformation Plasticity 输入参数
```

各相的温度随时间、各相的温度随冷却速率变化曲线。

这里的各相指的是贝氏体、奥氏体、马氏体。

### TTP of M(C,N)

不知道为什么，不能计算。

## Data Export

各相的质量百分比随温度变化曲线，但是不知道为什么，结果都是一样的。

## Others

碳的质量百分比随深度变化曲线。

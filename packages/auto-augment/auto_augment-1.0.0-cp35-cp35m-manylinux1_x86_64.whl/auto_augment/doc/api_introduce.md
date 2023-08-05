

API接口介绍
===



## SDK接口

SDK接口如下， 示例代码运行参考 [qiuic_start](./quick_start.md)

```python
from auto_augment.autoaug.experiment.experiment import AutoAugExperiment
from auto_augment.autoaug.transform.autoaug_transform import AutoAugTransform
from auto_augment.autoaug.utils.yaml_config import get_config
# yaml用户配置参数配置导入， 参数细节参考下一节《参数配置》
config = get_config(config_path, show=True)
# task_config(任务配置)
task_config = config.task_config
# data_config(数据配置)
data_config = config.data_config
# resource_config(资源配置)
resource_config = config.resource_config
# algo_config(算法配置)
algo_config = config.algo_config
# search_space(搜索空间配置
search_space = config.get("search_space", None)

# 数据增强策略搜索任务调用接口如下:
# 算法，任务，资源，数据，搜索空间(optional)配置导入，
exper = AutoAugExperiment.create(
    algo_config=algo_config,
    task_config=task_config,
    resource_config=resource_config,
    data_config=data_config,
    search_space=search_space
) 
# 开始搜索任务
result = exper.search()  
# 最佳策略获取， policy格式见搜索结果应用格式  
policy = result.get_best_policy()  
# policy保存本地
result.dump_best_policy(path=path) 

# 数据增强策略用户自定义调用接口
transform = AutoAugTransform.create(policy)  # 可应用于用户数据增强的transform接口
# PaddleClas接入示例工程 auto-augment/auto_augment/examples/PaddleClas
# PaddleClas接入示例算子CustomAutoAugTransform [auto-augment/auto_augment/examples/PaddleClas/code/ppcls_utils/operators.py] 

# PaddleDetection接入示例工程 auto-augment/auto_augment/examples/PaddleDetection
# PaddleDetection接入示例算子CustomAutoAugTransform [auto-augment/auto_augment/examples/PaddleDetection/code/ppdet_utils/transform_utils.py]


# todo 数据增强策略应用于自有训练任务调用接口如下, 未开发，优先级较低
exper = AutoAugExperiment.create(
algo_config=algo_config,
task_config=task_config,
resource_config=resource_config,
data_config=data_config
)
result = exper.train(policy=policy_file) 


```



## 参数配置

参数配置支持yaml格式描述及json格式描述，项目中仅提供yaml格式配置模板。模板统一于configs/路径下

用户可配置参数分为task_config(任务配置)，data_config(数据配置), resource_config(资源配置)，algo_config(算法配置)， search_space(搜索空间配置)。

### task_config(任务配置)

​	任务配置细节，包括任务类型及模型细节

​	具体字段如下:

​	run_mode: ["ray", "automl_service"],  #表示后端采用服务，目前支持单机ray框架, automl_service分布式暂未支持。

​	task_type： ["classifier", "detector"] #任务类型，目前支持图像分类单标签，物体检测单标签

​	classifier or detector: 具体任务类型的配置细节,

#### classifier任务配置细节

classifier任务采用开源paddleclas框架

- model_name: 模型名称
- model_yaml： 采用的paddleclas配置文件路径， 相关模型参数请在paddleclas配置文件中直接配置
- classifier_type：str, ["single_label"] 分类任务的类型，目前仅支持单标签
- epochs: int, 任务搜索轮数， **必填** , 该参数需要特殊指定
- early_stopper:  dict or None, early stop机制，

#### detector任务配置细节

detector任务采用开源paddledetection框架

与上述classifier任务配置细节一致的参数不再描述，新增参数额外补充。



### data_config(数据配置)

数据配置支持多种格式输入, 包括图像分类txt标注格式， 物体检测voc标注格式， 物体检测coco标注格式.

- train_img_prefix：str. 训练集数据路径前缀
- train_ann_file：str, 训练集数据描述文件， 
- val_img_prefix：str, 验证集数据路径前缀
- val_ann_file：str,验证集数据描述文件
- label_list：str, 标签文件
- delimiter： ","  数据描述文件采用的分隔符
- sample: 采样策略，详见下面采样策略说明
- anno_type: ["txt", "voc", "coco"] 支持图像分类txt标注格式， 物体检测voc标注格式， 物体检测coco标注格式

#### 采样策略说明
- type: ["stratify_sample", "random_sample"] 支持stratify_sample分层采样，random_sample随机采样
- sample_ratio：float, 采样比例
- mode: ["static", "dynamic"],  "static"表示固定采样，即采样数据在搜索过程中固定。"dynamic"表示动态采样，即采样数据在搜索过程中动态变化。 "dynamic"模式暂不支持

  
### resource_config(资源配置)
- gpu：float, 表示每个搜索进程的gpu分配资源，run_mode=="ray"模式下支持小数分配

- cpu:  float, 表示每个搜索进程的cpu分配资源，run_mode=="ray"模式下支持小数分配

  

### algo_config(算法配置)
算法配置目前仅支持PBA，后续会进一步拓展。
#### PBA配置
- algo_name: str, ["PBA"], 搜索算法
- algo_param:
   - perturbation_interval: 搜索扰动周期
   - num_samples：搜索进程数
   - 

### search_space(搜索空间配置)

搜索空间定义， 策略搜索阶段必填， 策略应用训练会忽略。

- operators_repeat： int，默认1， 表示搜索算子的重复次数。

- operator_space： 搜索的算子空间

   1. 自定义算子模式：

      htype: str, ["choice"] 超参类型，目前支持choice枚举

      value: list, [0,0.5,1] 枚举数据

      ![image-20200707162627074](/Users/lvhaijun01/Library/Application Support/typora-user-images/image-20200707162627074.png)

   2. 缩略版算子模式:

      用户只需要指定需要搜索的算子，prob, magtitue搜索空间为系统默认配置，为0-1之间。

      ![image-20200707162709253](/Users/lvhaijun01/Library/Application Support/typora-user-images/image-20200707162709253.png)

   支持1，2模式混合定议

      
#### 图像分类算子
["Sharpness", "Rotate", "Invert", "Brightness", "Cutout", "Equalize","TranslateY", "AutoContrast", "Color","TranslateX", "Solarize", "ShearX","Contrast", "Posterize", "ShearY", "FlipLR"]

#### 物体检测算子
["AutoContrast", "Equalize", "Posterize", "Solarize", "Solarize_add", "Color","Contrast", "Brightness", "Sharpness","Cutout", "BBox_Cutout", "Rotate_BBox", "TranslateX_BBox", "TranslateY_BBox", "ShearX_Only_BBoxes", "ShearY_Only_BBoxes", "TranslateX_Only_BBoxes", "TranslateY_Only_BBoxes", "Flip_Only_BBoxes", "Solarize_Only_BBoxes", "Equalize_Only_BBoxes", "Cutout_Only_BBoxes", "ShearX_BBox", "ShearY_BBox", "Rotate_Only_BBoxes"]



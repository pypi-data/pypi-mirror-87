

# 入门使用

## 目录
- [安装](#安装)
- [应用简述](#应用简述)
- [图像分类任务](#图像分类任务)
- [物体检测任务](#物体检测任务)
- [效果评测](#效果评测)

## 安装

安装文档参考 [安装文档](install.md)



## 应用简述

auto-augment组件目前支持图像分类任务和物体检测任务。

组件应用时分成搜索(search)和训练(train)两个阶段

**搜索阶段在预置模型上对不同算子的组合进行策略搜索，输出最优数据增强调度策略组合**

**训练阶段在特定模型上应用最优调度数据增强策略组合 **

下面分不同任务简述应用流程



## 图像分类任务

图像分类目前支持PaddleClas框架，使用开源代码在auto_augment/third_party/PaddleClas中

该框架的commit id 请参考git记录。

以MobileNetV3_small_x1_0模型，imagenet任务为例

其他模型请参考examples/PaddleClas/MobileNetV3_small_x1_0

### paddle版本依赖

```
依赖 paddlepaddle-gpu==1.7.1
```



### 数据配置

请参考PaddleClas的[数据说明](../third_party/PaddleClas/docs/zh_CN/tutorials/data.md)

提供imagenet上的启动脚本。

imagenet数据可以通过软连方式将数据准备格式如下

```bash
auto_augment/dataset/imagenet/
|_ train/
|  |_ n01440764
|  |  |_ n01440764_10026.JPEG
|  |  |_ ...
|  |_ ...
|  |
|  |_ n15075141
|     |_ ...
|     |_ n15075141_9993.JPEG
|_ val/
|  |_ ILSVRC2012_val_00000001.JPEG
|  |_ ...
|  |_ ILSVRC2012_val_00050000.JPEG
|_ train_list.txt
|_ val_list.txt
```

### 搜索阶段

搜索配置请参考[SDK介绍](./api_introduce.md)

提供imagent上的采样数据集 dataset/imagenet/reduce_train_cls240_num_100.txt

```bash
cd auto_augment
bash examples/PaddleClas/MobileNetV3_small_x1_0/search/search_autoaug_classify_imagenet.sh
```

### 训练阶段

用户在训练阶段利用搜索产生的最优调度策略进行模型，理论上最优调度策略具有一定的可迁移性，可应用于不同模型的训练使用，但具体迁移的效果提升需要实测，建议是搜索模型与训练模型尽量一致，效果可以得到最大程度保证。

具体训练配置请参考[训练示例](./train_examples_docs.md)

```bash
cd auto_augment
bash examples/PaddleClas/MobileNetV3_small_x1_0/train/train_autoaug_classify_imagenet.sh
```



## 物体检测任务

### paddle版本依赖

```
依赖 paddlepaddle-gpu==1.7.1
```



物体检测目前支持PaddleDetection框架，使用开源代码在auto_augment/third_party/PaddleDetection中

该框架的commit id 请参考git记录。

以faster_rcnn_r50_vd_fpn_3x模型，coco任务为例

其他模型请参考examples/PaddleDetection/faster_rcnn_r50_vd_fpn_3x

### 数据配置

请参考PaddleDetection的[安装说明中的数据集](../third_party/PaddleDetection/docs/tutorials/INSTALL_cn.md)

提供coco上的启动脚本。

提供coco上的采样数据集 dataset/coco/instance_coco_sample_train.json

```bash
auto_augment/dataset/coco/
├── annotations
│   ├── instances_train2014.json
│   ├── instances_train2017.json
│   ├── instances_val2014.json
│   ├── instances_val2017.json
│   |   ...
├── train2017
│   ├── 000000000009.jpg
│   ├── 000000580008.jpg
│   |   ...
├── val2017
│   ├── 000000000139.jpg
│   ├── 000000000285.jpg
│   |   ...
|   ...
```

### 搜索阶段

搜索配置请参考[SDK介绍](./api_introduce.md)

```bash
cd auto_augment
bash examples/PaddleDetection/faster_rcnn_r50_vd_fpn_3x/search/search_autoaug_detector_coco.sh
```

### 训练阶段

用户在训练阶段利用搜索产生的最优调度策略进行模型，理论上最优调度策略具有一定的可迁移性，可应用于不同模型的训练使用，但具体迁移的效果提升需要实测，建议是搜索模型与训练模型尽量一致，效果可以得到最大程度保证。

具体训练配置请参考[训练示例](./train_examples_docs.md)

```bash
cd auto_augment
bash examples/PaddleDetection/faster_rcnn_r50_vd_fpn_3x/train/train_autoaug_detector_coco.sh
```



# 效果评测

查看[效果评测](./benchmark.md)



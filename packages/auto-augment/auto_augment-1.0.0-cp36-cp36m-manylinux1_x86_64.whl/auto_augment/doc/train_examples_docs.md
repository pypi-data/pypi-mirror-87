数据增强策略应用实例
===

## 图像分类paddleclas

基于paddleclas的训练代码修改参考auto_augment/examples/PaddleClas/code

训练代码的启动与paddleclas保持一致，以MobileNetV3_small_x1_0为例:

需要定制auto_augment/examples/PaddleClas/MobileNetV3_small_x1_0/train/MobileNetV3_small_x1_0_imagenet.yml

在MobileNetV3_small_x1_0_imagenet.yml中插入CustomAutoAugTransform算子。





## 物体检测paddledetection

基于paddledetection的训练代码修改参考auto_augment/examples/PaddleDetection/code

训练代码的启动与paddledetection保持一致，以faster_rcnn_r50_vd_fpn_3x为例:

需要定制auto_augment/examples/PaddleDetection/faster_rcnn_r50_vd_fpn_3x/train/faster_rcnn_r50_vd_fpn_3x_coco.yml

在faster_rcnn_r50_vd_fpn_3x_coco.yml中插入CustomAutoAugTransform算子

注意paddledetection默认支持iters的迭代模式，但auto-augment只支持epoch的迭代模式。

**因此需要用户自行转换epochs与max_iters。epochs = max_iters * train_batch_size * gpu_nums / train_images **

在auto_augment/examples/PaddleDetection/faster_rcnn_r50_vd_fpn_3x/search/faster_rcnn_r50_vd_fpn_3x.yml 中 填入epochs

在auto_augment/examples/PaddleDetection/faster_rcnn_r50_vd_fpn_3x/train/faster_rcnn_r50_vd_fpn_3x_coco.yml 中填入max_iter



### 
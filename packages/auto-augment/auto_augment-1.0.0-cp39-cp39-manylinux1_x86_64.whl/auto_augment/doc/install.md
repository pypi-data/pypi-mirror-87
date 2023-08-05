# 安装说明

todo 提供whl本地包 或 运行环境镜像

## docker镜像构建

### dockerfile构建

```
cd auto_augment/dockerfile/py3.7
docker build -t auto-augment:1.0.0-dev .
```

#### 镜像下载: 

从下述百度云组件资源下载auto-augment_1.0.0.tar

docker load -i auto-augment_1.0.0.tar 导入即可

镜像名为yq01-aip-m12-tianzhi14.yq01.baidu.com/dragonboat/auto-augment:1.0.0-dev
hub.baidubce.com/rudder/auto-augment:1.0.0-dev



## 代码获取



从下述百度云组件资源下载whl包，例如auto_augment-1.0.0-cp37-cp37m-linux_x86_64.whl

```
pip install auto_augment-1.0.0-cp37-cp37m-linux_x86_64.whl #会自动安装相关依赖
pip -V #获取site-packages地址
mv xxxx/lib/python3.7/site-packages/auto_augment <user_path>/
使用 <user_path>/auto_augment即可。
```





## 百度云组件资源下载

链接:https://pan.baidu.com/s/1w-2TTyz26b5F-a7vMbTOIA  密码:1625




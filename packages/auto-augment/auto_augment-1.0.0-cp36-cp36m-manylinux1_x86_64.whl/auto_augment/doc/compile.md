# 编译说明

## cython编译说明

组件库以cython编译进行加密
代码编译列表在auto-augment/auto_augment/doc/online_list.json
在根目录下运行 bash setup.sh 即完成代码编译加密和发布
发布产生在ouput/dist/中

todo 支持不同python版本的编译发布

其他有用命令
1.python setup.py install 
2.python setup.py install --user



## 更改成manylinux版本

https://opensource.com/article/19/2/manylinux-python-wheels

https://github.com/pypa/manylinux

镜像 hub.baidubce.com/rudder/autoaugment/manylinux1_x86_64_cython:1.0

```
docker pull quay.io/pypa/manylinux1_x86_64
docker run --name=haijun_autoaug_build_v3 -v /data:/home -it hub.baidubce.com/rudder/autoaugment/manylinux1_x86_64_cython:1.0 bash
cd xxxx
auditwheel repair auto_augment-1.0.0-cp37-cp37m-linux_x86_64.whl -w ./output/


```



## 编译镜像

```
deploy_param_image_name=hub.baidubce.com/rudder/autoaugment/manylinux1_x86_64_cython:1.0
cd auto_augment/dockerfile/compile/Dockerfile
docker build -f ./Dockerfile -t ${deploy_param_image_name} .
```

## 编译集成脚本

一键生成支持python3.x、manylinux架构的软件包

```
hub.baidubce.com/rudder/autoaugment/manylinux1_x86_64_cython:1.0
bash auto_augment/scripts/complie.sh
```

# 发布到pypi

## test-pypi发布

```
https://test.pypi.org/manage/projects/
https://packaging.python.org/tutorials/packaging-projects/
python3 -m pip install --user --upgrade twine
# 上传
python3 -m twine upload --repository https://upload.pypi.org/legacy --skip-existing dist/*
# 下载
pip install -i https://test.pypi.org/simple/ auto-augment

```




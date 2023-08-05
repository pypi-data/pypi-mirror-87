FROM nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04

LABEL maintainer="lvhaijun01@baidu.com"


ARG UBUNTU_MIRROR="http://mirrors.tuna.tsinghua.edu.cn/ubuntu"
RUN bash -c 'if [[ -n ${UBUNTU_MIRROR} ]]; then \
        sed -i "s#http://archive.ubuntu.com/ubuntu#${UBUNTU_MIRROR}#g" /etc/apt/sources.list && \
        sed -i "s#http://security.ubuntu.com/ubuntu#${UBUNTU_MIRROR}#g" /etc/apt/sources.list ; \
    fi'

# Configure time zone
RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libopencv-dev \
    libssl-dev \
    dnsutils \
    unzip \
    vim \
    rsync \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
#ADD Miniconda3-latest-Linux-x86_64.sh /tmp/

#py3
RUN bash -c 'cd /tmp && \
    wget --no-check-certificate https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.2-Linux-x86_64.sh && \
    bash Miniconda3-py37_4.8.2-Linux-x86_64.sh -b -p ~/miniconda3 && \
    echo "source ~/miniconda3/bin/activate" >> ~/.bashrc && \
    echo "export PATH="~/miniconda3/bin:${PATH}"" >> ~/.bashrc && \
    source ~/.bashrc  && \
    rm -rf Miniconda3-py37_4.8.2-Linux-x86_64.sh' && \
    /root/miniconda3/bin/python -m pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/ && \
    /root/miniconda3/bin/python -m pip install --upgrade pip && \
    /root/miniconda3/bin/python -m pip install --upgrade setuptools && \
    /root/miniconda3/bin/python -m pip install albumentations==0.4.3 && \
    /root/miniconda3/bin/python -m pip install Cython==0.29.16 && \
    /root/miniconda3/bin/python -m pip install pycocotools==2.0.0 && \
    /root/miniconda3/bin/python -m pip install numpy==1.17.4 && \
    /root/miniconda3/bin/python -m pip install ray[tune]==0.8.4 && \
    /root/miniconda3/bin/python -m pip install scikit-learn==0.21.3 && \
    /root/miniconda3/bin/python -m pip install addict==2.2.1 && \
    /root/miniconda3/bin/python -m pip install xmltodict==0.12.0 && \
    /root/miniconda3/bin/python -m pip install pandas==0.25.2  && \
    /root/miniconda3/bin/python -m pip install ujson==3.0.0 && \

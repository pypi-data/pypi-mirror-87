#!/usr/bin/env bash
# @Project      : tql-cloudml
# @Time         : 2019-06-10 19:19
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

docker rmi # 删除镜像
docker image prune # 清空镜像

docker container ls -a
docker rm # 删除容器
docker container prune -f # 清空容器

docker pull cr.d.xiaomi.net/cloud-ml/tensorflow-gpu:1.13.1-xm1.0.0-zjyprc-hadoop-py3


docker run -it --rm --name container 2f08cdcac492 bash

docker commit  -a 'yuanjie' -m 'ml tools' --change='CMD /prepare_dev.py && /run_jupyter.sh' tql-ml cr.d.xiaomi.net/yuanjie/tql-ml:v1

# milvus-admin
# docker image inspect milvusdb/milvus-admin:latest | grep -i version
docker run -p 3000:80 milvusdb/milvus-em
docker container list

ContainerID=8ca24d3ff686
ImageName=milvus-admin:latest
docker commit  -a 'yuanjie' -m 'ann' $ContainerID cr.d.xiaomi.net/yuanjie/$ImageName
docker push cr.d.xiaomi.net/yuanjie/$ImageName

# app
ContainerID=45ad4e63c9dc
ImageName=app:latest
docker commit  -a 'yuanjie' -m 'ann' $ContainerID cr.d.xiaomi.net/yuanjie/$ImageName
docker push cr.d.xiaomi.net/yuanjie/$ImageName


# milvus
docker run -it --rm --name ann milvusdb/milvus:cpu-latest bash
docker container list

ContainerID=8313f4e7e2b8
ImageName=milvus:cpu-latest
docker commit  -a 'yuanjie' -m 'ann' $ContainerID cr.d.xiaomi.net/yuanjie/$ImageName
docker push cr.d.xiaomi.net/yuanjie/$ImageName


ContainerID=3b0fea9464f6
ImageName=neo4j:0.0.1
docker commit  -a 'yuanjie' -m 'neo4j' $ContainerID cr.d.xiaomi.net/yuanjie/$ImageName
docker push cr.d.xiaomi.net/yuanjie/$ImageName


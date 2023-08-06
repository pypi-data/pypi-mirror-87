#!/usr/bin/env bash
if [ -n "$1" ]
then name=$1
else name=gpu2
fi;

# 镜像列表：http://docs.api.xiaomi.net/cloud-ml/usage/image_list.html
password=xiaomi
cloudml dev create -n $name -p $password \
--priority_class guaranteed \
-d cr.d.xiaomi.net/cloud-ml/horovod:0.19.3-tf2.1.0-torch-mxnet1.6.0-xm1.0.0-py3 \
-cm rw \
-c 32 -M 32G \
-g 1 # [u\'v100-32g\', u\'t4-16g\', u\'p4-8g\', u\'v100-16g\']
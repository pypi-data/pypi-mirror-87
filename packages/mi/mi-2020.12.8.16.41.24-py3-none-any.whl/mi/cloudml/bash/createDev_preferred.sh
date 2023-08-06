#!/usr/bin/env bash
if [ -n "$1" ]
then name=$1
else name=gpu2
fi;

password=xiaomi
cloudml dev create -n $name -p $password \
--priority_class preferred \
-d cr.d.xiaomi.net/cloud-ml/tensorflow-gpu:33103tql2dev  \
-cm rw \
-c 16 -M 32G \
#-g 1
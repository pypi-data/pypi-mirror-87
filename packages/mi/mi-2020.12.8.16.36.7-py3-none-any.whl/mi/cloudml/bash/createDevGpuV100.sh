#!/usr/bin/env bash
if [ -n "$1" ]
then name=$1
else name=v100
fi;

password=Betterme8
cloudml dev create -n $name -p $password \
--priority_class guaranteed \
-d cr.d.xiaomi.net/cloud-ml/tensorflow-gpu:2.2.0-xm1.0.0-py3 \
-cm rw \
-rs v100 \
-c 31 -M 32G \
-g 1 -gt v100 -gm 32g \




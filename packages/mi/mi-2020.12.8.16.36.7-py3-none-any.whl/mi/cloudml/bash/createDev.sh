# http://docs.api.xiaomi.net/cloud-ml/usage/request_quota_v2.html

#!/usr/bin/env bash
if [ -n "$1" ]
then name=$1
else name=tql2dev
fi;

password=xiaomi
cloudml dev create -n $name -p $password \
-d cr.d.xiaomi.net/cloud-ml/tensorflow-gpu:33103tql2dev \
--priority_class guaranteed \
-c 32 -M 32G \
-g 1 \
-cv aaa \
-cm rw


#https://cloud.d.xiaomi.net/product/docs/cloudml/devenv/02_use_dev_cli
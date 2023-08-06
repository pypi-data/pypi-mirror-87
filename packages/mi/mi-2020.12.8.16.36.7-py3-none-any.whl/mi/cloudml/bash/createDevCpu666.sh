# http://docs.api.xiaomi.net/cloud-ml/usage/request_quota_v2.html

#!/usr/bin/env bash
if [ -n "$1" ]
then name=$1
else name=cpu666
fi;

password=Betterme8

#cloudml ceph create -n $name -c 100G
#sleep 10

cloudml dev create -n $name -p $password \
-d cr.d.xiaomi.net/cloud-ml/devsave:33103-v100 \
--priority_class preferred \
-c 4 -M 8G \
-cm rw \
-rs $name

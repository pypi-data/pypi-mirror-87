# http://docs.api.xiaomi.net/cloud-ml/usage/request_quota_v2.html

#!/usr/bin/env bash
if [ -n "$1" ]
then name=$1
else name=mastercpu
fi;

cloudml ceph create -n $name -c 100G
sleep 10

password=Betterme8
cloudml dev create -n $name -p $password \
-d cr.d.xiaomi.net/cloud-ml/devsave:33103-cpu666 \
--priority_class preferred \
-c 32 -M 64G \
-cm rw \
-rs $name

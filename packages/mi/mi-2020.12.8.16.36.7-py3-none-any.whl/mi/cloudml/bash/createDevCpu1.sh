# http://docs.api.xiaomi.net/cloud-ml/usage/request_quota_v2.html

#!/usr/bin/env bash
if [ -n "$1" ]
then name=$1
else name=cpu1
fi;

password=yuanjie
cloudml dev create -n $name -p $password \
-d cr.d.xiaomi.net/cloud-ml/devsave:33103-mydev \
--priority_class preferred \
-c 32 -M 88G \
-cm rw \
-cv aaa \
-cm rw


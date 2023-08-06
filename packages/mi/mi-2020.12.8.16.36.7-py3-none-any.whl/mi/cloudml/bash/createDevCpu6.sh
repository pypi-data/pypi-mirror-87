# http://docs.api.xiaomi.net/cloud-ml/usage/request_quota_v2.html

#!/usr/bin/env bash
if [ -n "$1" ]
then name=$1
else name=cpu6
fi;

password=Betterme8
cloudml dev create -n $name -p $password \
-d cr.d.xiaomi.net/cloud-ml/devsave:33103-mydev \
--priority_class preferred \
-hka h_browser@XIAOMI.HADOOP -hkt tql -he hdfs://zjyprc-hadoop \
-c 16 -M 32G \
-cm rw

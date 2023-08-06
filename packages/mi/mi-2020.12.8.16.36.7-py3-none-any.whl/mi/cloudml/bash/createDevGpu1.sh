#!/usr/bin/env bash
if [ -n "$1" ]
then name=$1
else name=master
fi;

password=Betterme8
cloudml dev create -n $name -p $password \
--priority_class guaranteed \
-d cr.d.xiaomi.net/cloud-ml/devsave:33103-dev_ \
-hka h_browser@XIAOMI.HADOOP -hkt tql -he hdfs://zjyprc-hadoop \
-cm rw \
-c 32 -M 32G \
-g 1 # [u\'v100-32g\', u\'t4-16g\', u\'p4-8g\', u\'v100-16g\']
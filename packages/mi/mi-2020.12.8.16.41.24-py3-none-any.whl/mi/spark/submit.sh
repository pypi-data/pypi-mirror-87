#!/usr/bin/env bash
# @Project      : mi
# @Time         : 2020-03-06 13:40
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

CLASS="com.xiaomi.algo.push.biz.label.LabelTrick"

function spark_calculate(){
spark-submit --cluster 'zjyprc-hadoop-spark2.1' \
--master yarn-cluster \
--conf spark.speculation=false \
--name $CLASS \
--conf spark.yarn.job.owners=yuanjie \
--conf spark.yarn.alert.phone.number=18550288233 \
--queue 'production.miui_group.browser.miui_browser_zjy_1' \
--num-executors 256 \
--executor-cores 2 \
--executor-memory 8g \
--driver-memory 8g \
--class ${CLASS} \
hdfs://zjyprc-hadoop/user/h_browser/algo/yuanjie/jars/MIPush-1.0-SNAPSHOT.jar \
-delta=$1

# var=$(date -d $1day +%Y%m%d)
# curl -d "id=64349&pt=date=$var" http://dp.pt.xiaomi.com/add_partition
}

for i in $(seq -8 1 -2)
do
spark_calculate $i
done

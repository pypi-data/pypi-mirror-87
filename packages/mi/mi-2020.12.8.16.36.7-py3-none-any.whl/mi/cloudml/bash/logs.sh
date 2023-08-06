#!/usr/bin/env bash
# @Project      : tql-cloudml
# @Time         : 2019-06-21 00:09
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

model="$1"
if [ -n "$2" ];
then n="$2"
else n=10
fi;

cloudml jobs logs $model -n $n



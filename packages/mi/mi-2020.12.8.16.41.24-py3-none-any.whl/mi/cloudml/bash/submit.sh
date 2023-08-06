#!/usr/bin/env bash
if [ -n "$1" ];
then model=$1
else model="model"
fi;

if cloudml jobs delete $model | grep "Successfully";
then echo "删除 ..." && sleep 18s;
fi;
cloudml jobs submit -f ./model.yaml -n $model;
rm -rf ./build/ ./*.egg-info/ ./dist/;
sleep 8s && cloudml jobs metrics $model;
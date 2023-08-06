#!/usr/bin/env bash
project_name=$1
if cloudml jobs delete $project_name | grep error;
then echo "11111"
fi
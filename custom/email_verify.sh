#!/bin/bash

# curl --user restadmin:restpass -X POST http://10.89.0.53:8001/3.1/addresses/$1/verify #| python3 -m json.tool

# curl --user restadmin:restpass -X POST http://10.89.0.53:8001/3.1/addresses/$1/unverify #| python3 -m json.tool


while getopts ":vu:" option; do
  case $option in
    v)
      podman exec -it mailman-core curl --user restadmin:restpass -X POST http://10.89.0.53:8001/3.1/addresses/$1/verify #| python3 -m json.tool
      exit;;
    u)
      podman exec -it mailman-core curl --user restadmin:restpass -X POST http://10.89.0.53:8001/3.1/addresses/$1/unverify #| python3 -m json.tool
      exit;;
    *)
      echo "invalid option"
      exit;;
  esac
done

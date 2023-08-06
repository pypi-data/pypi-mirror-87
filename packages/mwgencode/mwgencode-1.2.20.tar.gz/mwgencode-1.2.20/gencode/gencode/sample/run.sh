#!/usr/bin/env bash
# consul的host 格式 ip:port
export CONSUL_HTTP_ADDR=192.168.101.88:8500
# docker host的port
export WEB_PORT=8899
# true自動註冊到kong，true，false不做，注意字母全小寫
export KONG_AUTO_REGISTER=true
# true自動註冊成 consul服務，false不做，注意字母全小寫
export CONSUL_AUTO_REGISTER=true
# 资料库名，默认为 maxbus
export DATABASE_NAME=maxbus
# 权限用的系统名称
export SYSTEM_NAME=misweb
export LOG_LEVEL=20
#export SWAGGER_HOST=192.168.101.88:8081
export UPLOAD_FOLDER="/var/文件共享目录"
# 认证方式 jwt，session，默认为jwt（不需要该设定，因auth已同时支持session和jwt）
# export AUTH_TYPE=jwt
# 開發環境的docker，代碼valume方式
docker-compose -f docker-compose-dev.yaml up -d
# 部署的docker-compose 文件
#docker-compose up -d


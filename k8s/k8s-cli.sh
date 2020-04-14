#!/usr/bin/env sh
set -eu
set -x

SERVICE_NAME=config-registry-service
_path=$(dirname $(realpath "${0}"))

do_build_image() {
  eval $(minikube docker-env)
  docker build --pull --tag=config-registry "$(dirname ${_path})"
  eval $(minikube docker-env -u)
}

do_show_url() {
  minikube service "${SERVICE_NAME}" ${1:---url}
}

do_start_service() {
  kubectl apply -f ${_path}/deployment.yml
  kubectl apply -f ${_path}/service.yml
  echo "Service available at: $(do_show_url)/configs"
}

do_stop_service() {
  kubectl delete -f ${_path}/deployment.yml || true
  kubectl delete -f ${_path}/service.yml || true
}

case "${1}" in
build)
  do_build_image
  ;;
url)
  do_show_url
  ;;
start)
  do_start_service
  ;;
stop)
  do_stop_service
  ;;
esac

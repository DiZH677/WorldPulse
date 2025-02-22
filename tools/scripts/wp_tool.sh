
#!/bin/sh

current_dir=$(pwd)
service_path=$(echo "$current_dir" | grep -o '.*/services/[^/]*')

if [ -z "$service_path" ]; then
  echo "Ошибка: Вы не находитесь в каталоге сервиса (services/<название сервиса>)."
  exit 1
fi

service_name=$(basename "$service_path")

if [ "$1" = "test" ]; then
  ln -s "$service_path/src/endpoints" "$service_path/tests/endpoints"
  pytest "$service_path/tests"
  rm "$service_path/tests/endpoints"
  exit 0
fi

if [ "$1" = "gen" ]; then
  openapi-generator-cli generate \
  -i "$service_path/docs/api.yaml"\
  -g python-fastapi\
  -o .  --additional-properties=packageName=endpoints --additional-properties=fastapiImplementationPackage=endpoints
  exit 0
fi

if [ "$1" = "run" ]; then
  cd "$service_path" && sudo docker compose up
  exit 0
fi


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
  --minimal-update\
  -o "$service_path" --additional-properties=packageName=endpoints --additional-properties=fastapiImplementationPackage=endpoints

  codegen_dir=$(realpath "$service_path/../../.codegen")
  services_dir=$(realpath "$service_path/../")

  if [ ! -d "$codegen_dir" ]; then
    mkdir -p "$codegen_dir"
  fi

  for item in "$services_dir"/*; do
    # Проверка, является ли элемент директорией
    if [ -d "$item" ]; then
      item_name=$(basename "$item")
      if [ "$item_name" != "$service_name" ]; then
        item_name_norm=$(echo "$item_name" | sed 's/-/_/g')

        echo "Генерация клиента для: $item_name_norm"
        arg_1="$item/docs/api.yaml"
        arg_2="$codegen_dir/client_$item_name_norm"
        openapi-generator-cli generate -i "$arg_1" -g python -o "$arg_2"_tmp --package-name "$item_name_norm"_client
        rm -r "$service_path"/src/"$item_name_norm"_client
        mv "$arg_2"_tmp/"$item_name_norm"_client "$service_path"/src/"$item_name_norm"_client
        mv "$arg_2"_tmp/requirements.txt "$service_path"/src/"$item_name_norm"_client/requirements.txt
      fi
    fi
  done

  rm -r "$codegen_dir"
  exit 0
fi

if [ "$1" = "run" ]; then
  cd "$service_path" && sudo docker compose up
  exit 0
fi

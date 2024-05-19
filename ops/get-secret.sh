#!/bin/bash

# Fly.IO secrets getter since they don't want to make one available in the CLI
# Args: app name, secret key

vars=($(flyctl secrets list --app $1 | grep -v DIGEST | awk '{print $1}'))
output=$(flyctl ssh console --app $1 -C 'env' 2>/dev/null)

for line in $output; do
  varname=${line%%=*}
  for var in "${vars[@]}"; do
    if [ "$var" = "$varname" ]; then
      echo "${line#*=}"
      break
    fi
  done
done

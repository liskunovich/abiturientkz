#!/bin/bash

cleanup() {
    echo "...Остановка контейнеров..."
    docker-compose -f docker-compose-dbs.yml -f docker-compose.yml stop
}

trap cleanup EXIT

docker-compose -f docker-compose-dbs.yml -f docker-compose.yml up -d

docker-compose -f docker-compose-dbs.yml -f docker-compose.yml logs -f

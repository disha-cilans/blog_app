#!/bin/sh     
docker-compose down
docker image prune -f
docker-compose up -d
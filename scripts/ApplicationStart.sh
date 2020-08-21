#!/bin/bash

# Upgrade DB
docker-compose run --rm backend alembic upgrade head
docker-compose -f /srv/scdao-api/docker-compose.yml up --env-file=/srv/scdao-api/.env -d > /dev/null 2> /dev/null < /dev/null &
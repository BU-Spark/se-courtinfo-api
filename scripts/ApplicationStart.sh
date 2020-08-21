#!/bin/bash

# Upgrade DB
docker-compose run --rm backend alembic upgrade head
docker-compose -f /srv/scdao-api/docker-compose.yml up -d > /dev/null 2> /dev/null < /dev/null &
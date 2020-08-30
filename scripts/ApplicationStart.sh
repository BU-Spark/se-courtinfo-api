#!/bin/bash

# Upgrade DB
if [ "$DEPLOYMENT_GROUP_NAME" == "SCDAO-API-PROD" ]
then
  # Just start app, don't want to automatically upgrade DB in production
  docker-compose -f /srv/scdao-api/docker-compose.yml -f /srv/scdao-api/docker-compose.prod.yml up --env-file=/srv/scdao-api/.env -d > /dev/null 2> /dev/null < /dev/null &
fi

if [ "$DEPLOYMENT_GROUP_NAME" == "SCDAO-API-DEV" ]
then
  # Run DB upgrade and start app
  docker-compose run --rm backend alembic upgrade head
  docker-compose -f /srv/scdao-api/docker-compose.yml -f /srv/scdao-api/docker-compose.dev.yml up --env-file=/srv/scdao-api/.env -d > /dev/null 2> /dev/null < /dev/null &
fi

#!/bin/bash -e

set -e

if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
  docker login --username="$DOCKER_USERNAME" --password="$DOCKER_PASSWORD" https://reg.fluxdock.io:5000

  if [ "$TRAVIS_BRANCH" == "master" ]; then
    echo "Deploying image to docker hub for master (latest)"
    docker tag fluxdock_odoo odoo/odoo:latest
    docker push "odoo/odoo:latest"
  elif [ ! -z "$TRAVIS_TAG" ]; then
    echo "Deploying image to docker hub for tag ${TRAVIS_TAG}"
    docker tag fluxdock_odoo odoo/odoo:${TRAVIS_TAG}
    docker push "odoo/odoo:${TRAVIS_TAG}"
  elif [ ! -z "$TRAVIS_BRANCH" ]; then
    echo "Deploying image to docker hub for branch ${TRAVIS_BRANCH}"
    docker tag fluxdock_odoo odoo/odoo:${TRAVIS_BRANCH}
    docker push "odoo/odoo:${TRAVIS_BRANCH}"
  else
    echo "Not deploying image"
  fi
fi

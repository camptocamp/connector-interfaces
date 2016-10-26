#!/bin/bash -e

set -e

if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
  docker login --username="$DOCKER_USERNAME" --password="$DOCKER_PASSWORD"

  if [ "$TRAVIS_BRANCH" == "master" ]; then
    echo "Deploying image to docker hub for master (latest)"
    docker tag fluxdock_odoo camptocamp/fluxdock_odoo:latest
    docker push "camptocamp/fluxdock_odoo:latest"
  elif [ ! -z "$TRAVIS_TAG" ]; then
    echo "Deploying image to docker hub for tag ${TRAVIS_TAG}"
    docker tag fluxdock_odoo camptocamp/fluxdock_odoo:${TRAVIS_TAG}
    docker push "camptocamp/fluxdock_odoo:${TRAVIS_TAG}"
  elif [ ! -z "$TRAVIS_BRANCH" ]; then
    echo "Deploying image to docker hub for branch ${TRAVIS_BRANCH}"
    docker tag fluxdock_odoo camptocamp/fluxdock_odoo:${TRAVIS_BRANCH}
    docker push "camptocamp/fluxdock_odoo:${TRAVIS_BRANCH}"
  else
    echo "Not deploying image"
  fi

  echo "This is a PR"

fi

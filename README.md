[![Build Status](https://travis-ci.com/camptocamp/fluxdock_odoo.svg?token=Lpp9PcS5on9AGbp76WKB&branch=master)](https://travis-ci.com/camptocamp/fluxdock_odoo)

# Fluxdock Odoo Project (Coaching)

This project uses Docker.
Travis builds a new image for each change on the branches and for each new tag.

The images built on the master branch are built as `odoo/odoo:latest`.
The images built on other branches are built as `odoo/odoo:<branch-name>`.
The ones built from tags are built as `odoo/odoo:<tag-name>`.

Images are pushed on the fluxdock registry `reg.fluxdock.io:5000` only when Travis has a green build.

The database is automatically created and the migration scripts
automatically run.

You'll find a [Docker guide for the development](./docs/docker-dev.md) and on for the [testers](./docs/docker-test.md).

## Guides

* [Docker pre-requisite](./docs/prerequisites.md)
* [Docker developer guide](./docs/docker-dev.md)
* [Docker tester guide](./docs/docker-test.md)
* [Deployment](./docs/deployment.md)
* [Structure](./docs/structure.md)
* [Releases and versioning](./docs/releases.md)
* [Pull Requests](./docs/pull-requests.md)
* [Upgrade scripts](./docs/upgrade-scripts.md)

## How-to

* [How to add a new addons repository](./docs/how-to-add-repo.md)
* [How to add a Python or Debian dependency](./docs/how-to-add-dependency.md)
* [How to integrate an open pull request of an external repository](./docs/how-to-integrate-pull-request.md)
* [How to connect to psql in Docker](./docs/how-to-connect-to-docker-psql.md)
* [How to change Odoo configuration values](./docs/how-to-set-odoo-configuration-values.md)
* [How to backup and restore volumes](./docs/how-to-backup-and-restore-volumes.md)

The changelog is in [HISTORY.rst](HISTORY.rst).


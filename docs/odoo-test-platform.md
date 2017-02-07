# Odoo Test Platform

This platform builds test instances for our projects.  The tests instances are
mainly intended to be used by Camptocamp developers and project managers, but
occasionally it may be useful for showing a feature to a customer. The goal is
to quickly test a merged pull request on master.

The test instances are **automatically recreated from scratch** after every
commit on master.

For this reason:
* We will not put the test database on the postgres cluster but in a standalone
  container in the test stack.
* This instance should be populated with a small set of data in order to be
  quickly created.
* Assume this instance **can be deleted at any moment** with all the data you
  have created or modified.

The platform is on
[https://caas-dev.camptocamp.com/env/1a100359/apps/stacks](https://caas-dev.camptocamp.com/env/1a100359/apps/stacks).

The test instances are accessed using domains in the *.odoo-test.camptocamp.ch
subdomain, such as fluxdock.odoo-test.camptocamp.ch.


#### Test stack configuration

See [rancher.md](rancher.md#rancher-environment-setup) for more details and encrypt / decrypt command.

For the test stack, the composition file is [rancher/fluxdock-odoo-test/docker-compose.yml](../rancher/fluxdock-odoo-test/docker-compose.yml).

If you used [Odoo template](https://github.com/camptocamp/odoo-template) to
create your project you should already have it.

Otherwise, you can download it and replace all the cookiecutter's values.

Then, be sure to check the configuration of the instance (download the files
from the odoo-template repository if needed) in
[rancher/fluxdock-odoo-test/rancher.public.env](../rancher/fluxdock-odoo-test/rancher.public.env) and
[rancher/fluxdock-odoo-test/rancher.env](../rancher/fluxdock-odoo-test/rancher.env).  The second file
contains the private values and [needs to be
encrypted](rancher.md#rancher-environment-setup) to `rancher.env.gpg`
(`rancher.env` is never committed and must be in `.gitignore`).

In `rancher.env` you have to fill:
* RANCHER_ACCESS_KEY and RANCHER_SECRET_KEY, the keys are in
  Lastpass' "[odoo-test] Rancher API Keys for rancher.env"
* LETSENCRYPT_AWS_ACCESS_KEY and LETSENCRYPT_AWS_SECRET_KEY the keys are in
  Lastpass' "[odoo-test] Let's Encrypt AWS Keys for rancher.env"
* DB_PASSWORD and ADMIN_PASSWD with freshly generated passwords. To generate
  passwords, you can use this command in your terminal `pwgen -n1 -s 20`

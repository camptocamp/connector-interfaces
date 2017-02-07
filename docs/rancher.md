# Automated Rancher build

## Travis deployment

When committing on master branch, if tests pass, Travis will:

1. Build a docker image
2. Push it on DockerHub with the tag: `latest`
3. Upgrade the stack on rancher with image `latest`

Thus, the test server will be continuously upgraded.

## Rancher templates

### Test instance

The Rancher template for the test instance is defined in [rancher folder](../rancher/fluxdock-odoo-test/).
This templates defines the rancher stack automatically upgraded by Travis.

### Integration and production instances

The Rancher templates for the integration and production instances are grouped in a project
for the platform:

* https://github.com/camptocamp/odoo-cloud-platform-ch-rancher-templates


## Rancher environment setup

In order to configure the variables for the container built on Rancher by
Travis, the file [rancher.env.gpg](../rancher/fluxdock-odoo-test/rancher.env.gpg) is used

For every operation below, a password will be asked. The password is stored in Lastpass in the following site in the folder of the project:

* Rancher: fluxdock-odoo-test/rancher.env.gpg

If you've just created the rancher.env files, you should create the corresponding Lastpass entry.
You should also add rancher.env in project .gitignore file, only rancher.env.gpg should be commited.

To decrypt a file, run:

```
$ gpg rancher.env.gpg
```

You can also source the content of a file (which is only composed of environment variables used by `rancher-compose`) if you need to use `rancher-compose`:

```
$ source <(gpg2 -d rancher.env.gpg)
```

When you have to modify the file, you have to re-encrypt the file, which is done with:

```
$ gpg2 --symmetric --cipher-algo AES256 rancher.env
```

## Travis

Each succeeded build on the master branch triggers:

* push of a new `latest` image on the Docker Hub
* deploy of the `latest` image on the test environment

The password to decrypt the gpg environment file (Rancher:
fluxdock-odoo-test/rancher.env.gpg) is needed by Travis, so we store it in a `secure`
environment.

To get this secure variable:
 * Install, if needed, the travis command line client

 ```bash
 sudo gem install travis
 ```

 * Authenticate yourself on travis server with your github account.

 ```bash
 travis login
 ```

 * Then ask Travis to encrypt your gpg password (stored on Lastpass)

 ```bash
 travis encrypt -r camptocamp/<repository_name> rancher_env_password=xxxxxxx
 ```

The output of this command (should be like `secure=encrypted key`should be added in the `global` section in `env` of
`travis.yml`.


## Docker images

Docker images for Odoo are generated and pushed to [Docker Hub](https://hub.docker.com) by Travis when builds are successful.
This push is done in [travis/publish.sh](../travis/publish.sh) which is called by [travis.yml](../.travis.yml) in `after_success` section.

You can see that this script will tag docker image with:
 * latest: When the build was triggered by a commit on master
 * `git tag name`: When the build was triggered after a new tag is pushed.

So Travis must have access to your project on Docker Hub. If it's not the case, ask someone with access to:
 * Create if needed the [project on Docker Hub](https://hub.docker.com/r/camptocamp/fluxdock_odoo/)
 * Create access for Travis in this new project and put auth informations in Lastpass
  * user: c2cbusinessfluxdocktravis
  * password: Generated password
  * email: business-deploy+fluxdock-travis@camptocamp.com (which is aliased on camptocamp@camptocamp.com)

On Travis, in [settings page](https://travis-ci.com/camptocamp/fluxdock_odoo/settings) , add following environnement variables:
 * DOCKER_USERNAME : c2cbusinessfluxdocktravis
 * DOCKER_PASSWORD : The generated password in previous step, so you can find it in Lastpass

**From there, each travis successful build on master or on tags will build a docker image and push it to Docker Hub**

**And even better, if you followed all the previous steps, the next successfull build on master will automatically create the test stack (fluxdock-odoo-test) on Rancher**

#### Test deployment

In [travis/publish.sh](../travis/publish.sh), you can see that the deploy function is called when the latest image is generated
(so after a successful travis build on master)

This deploy function do the following steps:
 * Download a rancher-compose client
 * Decrypt fluxdock-odoo-test/rancher.env.gpg and source it to read all needed configurations for accessing rancher and configuring the stack.
 * Remove, if exists, the test stack db container on rancher.
 * Create or upgrade the full stack (with the new builded odoo docker image)
 * This upgrade will recreate a database and container and run the installation process.

But Travis need the gpg password in order to decrypt rancher.env.gpg file.

Look at [rancher.md in travis section](rancher.md#travis) to know how to configure travis for that.

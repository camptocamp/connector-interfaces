FROM camptocamp/odoo-project:9.0-2.0.0
MAINTAINER Camptocamp

# Install additional python packages if needed
COPY ./requirements.txt /opt/odoo
RUN cd /opt/odoo && pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl bzip2

RUN set -x; \
    curl -SL https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 | \
    tar xj --strip-components=2 -C /usr/local/bin/ phantomjs-2.1.1-linux-x86_64/bin/phantomjs

ENV ADDONS_PATH="/opt/odoo/local-src, \
/opt/odoo/external-src/server-tools, \
/opt/odoo/src/addons, \
/opt/odoo/external-src/vertical-association, \
/opt/odoo/external-src/website-cms, \
/opt/odoo/external-src/social, \
/opt/odoo/external-src/odoo-cloud-platform, \
"

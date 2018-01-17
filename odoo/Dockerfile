FROM camptocamp/odoo-project:11.0-2.5.1
MAINTAINER Camptocamp

COPY ./*requirements.txt /opt/odoo/

# Install additional debian and python packages if needed
RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
        libmagic1 \
        && cd /opt/odoo \
        && find . -maxdepth 1 -name "*requirements.txt" ! -name src_requirements.txt ! -name base_requirements.txt -exec pip install -r {} \; \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

COPY ./before-migrate-entrypoint.d/* odoo/before-migrate-entrypoint.d/
COPY ./start-entrypoint.d/* odoo/start-entrypoint.d/
RUN chmod +x odoo/before-migrate-entrypoint.d/* \
    && chmod +x odoo/start-entrypoint.d/*

ENV ADDONS_PATH="/opt/odoo/local-src, \
/opt/odoo/external-src/server-tools, \
/opt/odoo/external-src/server-env, \
/opt/odoo/src/addons, \
/opt/odoo/external-src/website-cms, \
/opt/odoo/external-src/social, \
/opt/odoo/external-src/odoo-cloud-platform, \
"

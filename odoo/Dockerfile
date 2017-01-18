FROM camptocamp/odoo-project:9.0-2.0.0
MAINTAINER Camptocamp

# Install additional python packages if needed
COPY ./requirements.txt /opt/odoo
RUN cd /opt/odoo && pip install -r requirements.txt

ENV ADDONS_PATH="/opt/odoo/local-src, \
/opt/odoo/external-src/server-tools, \
/opt/odoo/src/addons, \
/opt/odoo/external-src/vertical-association, \
/opt/odoo/external-src/website-cms, \
/opt/odoo/external-src/odoo-cloud-platform, \
"

FROM camptocamp/odoo-project:9.0-1.7.1
MAINTAINER Camptocamp

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY oerpscenario /opt/odoo/oerpscenario
COPY bin/oerpscenario /opt/odoo/bin/oerpscenario

ENV ADDONS_PATH=/opt/odoo/local-src,/opt/odoo/external-src/server-tools,/opt/odoo/src/addons,/opt/odoo/external-src/vertical-association

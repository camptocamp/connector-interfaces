# force deploy on test
# WARNING: removes db and odoo container as travis deploy does

RANCHER_STACK_NAME=fluxdock-odoo-test
TEMPLATE_DIR="${PWD}/rancher/latest"

source $TEMPLATE_DIR/rancher.env
source $TEMPLATE_DIR/rancher.public.env

(cd "${TEMPLATE_DIR}" && \
 rancher-compose -p "${RANCHER_STACK_NAME}" rm odoo db --force && \
 sleep 30 && \
 rancher-compose -p "${RANCHER_STACK_NAME}" up --pull --recreate --force-recreate --confirm-upgrade -d)

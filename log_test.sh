# follow odoo test logs

RANCHER_STACK_NAME=fluxdock-odoo-test
TEMPLATE_DIR="${PWD}/rancher/latest"

source $TEMPLATE_DIR/rancher.env
source $TEMPLATE_DIR/rancher.public.env

(cd "${TEMPLATE_DIR}" && \
 rancher-compose -p "${RANCHER_STACK_NAME}" logs --follow odoo)

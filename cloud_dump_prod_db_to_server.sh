# bash script to restore pre-cloud production database locally
# and fix db name a and filestore path to match our cloud settings
export PROJECT_NAME="fluxdock"
export HOST_BACKUPS=$PWD/bkp_to_prod  # Where you want to save the backups

[ -d $HOST_BACKUPS ] || mkdir $HOST_BACKUPS

docker run --rm --net=${PROJECT_NAME}_default --link ${PROJECT_NAME}_db_1:db -e PGPASSWORD=odoo -v $HOST_BACKUPS:/backup postgres:9.5 pg_dump -O -Uodoo --file /backup/fluxdock.pg --format=c odoodb -h db

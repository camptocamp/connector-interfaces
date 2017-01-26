# bash script to restore pre-cloud production database locally
# and fix db name a and filestore path to match our cloud settings
export PROJECT_NAME="fluxdock"
export HOST_BACKUPS=$PWD/bkp_prod  # Where you want to save the backups
export DATAODOO_VOLUME="${PROJECT_NAME}_data-odoo"  # Exact name to find with 'docker volume ls'
export DATADB_VOLUME="${PROJECT_NAME}_data-db"  # Exact name to find with 'docker volume ls'

# restore db
docker stop ${PROJECT_NAME}_db_1
docker run --rm -v "$DATAODOO_VOLUME:/data/odoo" -v $HOST_BACKUPS:/backup debian bash -c "tar xvzf /backup/backup-dataodoo.tar.gz"
docker run --rm -v "$DATADB_VOLUME:/var/lib/postgresql/data" -v $HOST_BACKUPS:/backup debian bash -c "tar xvzf /backup/backup-datadb.tar.gz"

# fix db name and filestore path
docker start ${PROJECT_NAME}_db_1
sleep 4
# docker exec -ti fluxdock_db_1 bash -c "createdb -U odoo 'odoodb_latest_$(date +"%Y%m%d")' -T odoodb" && \
# docker exec -ti fluxdock_db_1 bash -c "dropdb -U odoo odoodb --if-exists" && \
docker exec -ti ${PROJECT_NAME}_db_1 bash -c "createdb -U odoo  odoodb -T 'fluxdock-deutsch'" && \
docker exec -ti ${PROJECT_NAME}_db_1 bash -c "dropdb -U odoo 'fluxdock-deutsch'" && \
docker run --rm -v "$DATAODOO_VOLUME:/data/odoo" debian bash -c "[ -d /data/odoo/filestore/fluxdock-deutsch ] && rm -rf /data/odoo/filestore/odoodb && mv /data/odoo/filestore/fluxdock-deutsch /data/odoo/filestore/odoodb"

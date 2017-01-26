# scp files to server if HOST_BACKUPS
# ssh into odoo-platform-db
# restore db

# STOP ODOO!
# ./rancher fluxdock-odoo-prod stop odoo
sudo docker exec -it r-postgres-cluster_postgres_2 dropdb polished_morning_3582 -U postgres
sudo docker exec -it r-postgres-cluster_postgres_2 createdb polished_morning_3582 -U postgres -O polished_morning_3582
pg_restore -O -h lb.postgres-cluster -U polished_morning_3582 -d polished_morning_3582 fluxdock.pg
# START ODOO!
# ./rancher fluxdock-odoo-prod start odoo

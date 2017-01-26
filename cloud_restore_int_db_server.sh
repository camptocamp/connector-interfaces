# scp files to server if HOST_BACKUPS
# ssh into odoo-platform-int-db
# restore db

# STOP ODOO!
# ./rancher fluxdock-odoo-integration stop odoo
sudo docker exec -it r-postgres-integration_postgres_1 dropdb polished_morning_3582_integration -U postgres
sudo docker exec -it r-postgres-integration_postgres_1 createdb polished_morning_3582_integration -U postgres -O polished_morning_3582_integration
pg_restore -O -h postgres.postgres-integration -U polished_morning_3582_integration -d polished_morning_3582_integration fluxdock.pg
# START ODOO!
# ./rancher fluxdock-odoo-integration start odoo

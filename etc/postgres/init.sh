#!/bin/bash

#
# Copyright © 2013 by its contributors. See AUTHORS for details.
#

POSTGRES_VERSION=9.1

sudo cp -a /etc/postgresql/${POSTGRES_VERSION}/main/postgresql.conf .
sudo cp -a /etc/postgresql/${POSTGRES_VERSION}/main/pg_hba.conf .
sudo -u postgres pg_dropcluster --stop ${POSTGRES_VERSION} main
sudo -u postgres pg_createcluster -E 'UTF-8' --lc-collate='en_US.UTF-8' --lc-ctype='en_US.UTF-8' --locale='en_US.UTF-8' ${POSTGRES_VERSION} main
sudo sed -e "s:listen_addresses = 'localhost':listen_addresses = '*':g" -i postgresql.conf
sudo sed -e 's:127.0.0.1/32:0.0.0.0/0:g' -i pg_hba.conf
sudo cp -a ./postgresql.conf /etc/postgresql/${POSTGRES_VERSION}/main
sudo cp -a ./pg_hba.conf /etc/postgresql/${POSTGRES_VERSION}/main
sudo /etc/init.d/postgresql restart
sudo -u postgres psql -c "CREATE USER django_login WITH PASSWORD 'password';"
sudo -u postgres psql -c "ALTER ROLE django_login WITH CREATEDB"
sudo -u postgres psql -c "CREATE DATABASE django_db;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE django_db TO django_login;"

#
# End of File
#

#!/bin/bash
set -e
mysql -uroot -p"$MYSQL_ROOT_PASSWORD" ctf05 -e \
  "INSERT INTO products (id, name, description, price) VALUES (999, 'Vault', '${FLAG}', 0);"

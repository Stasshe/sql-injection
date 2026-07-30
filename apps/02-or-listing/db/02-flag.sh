#!/bin/bash
set -e
mysql -uroot -p"$MYSQL_ROOT_PASSWORD" ctf02 -e \
  "INSERT INTO products (id, name, description, price) VALUES (999, 'Internal Backup', '${FLAG}', 0);"

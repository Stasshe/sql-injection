#!/bin/bash
set -e
CODE=$((RANDOM % 10))
mysql -uroot -p"$MYSQL_ROOT_PASSWORD" ctf06 -e \
  "INSERT INTO flags (flag, code) VALUES ('${FLAG}', ${CODE});"

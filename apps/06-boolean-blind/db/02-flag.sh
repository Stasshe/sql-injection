#!/bin/bash
set -e
mysql -uroot -p"$MYSQL_ROOT_PASSWORD" ctf06 -e "INSERT INTO flags (flag) VALUES ('${FLAG}');"

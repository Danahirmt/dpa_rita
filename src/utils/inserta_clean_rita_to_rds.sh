#!/bin/bash
# Progama que hace la insersion de datos desde semantic.csv hacia semantic.rita
# Nota: necesita que el archio credentials_psql.txt este presente, el cual
# contiene los datos que permite la conexion a psql con el RDS
# user = MY_USER
# password = MY_PASS
# db_name = MY_DB
# host = MY_HOST

. credentials_psql.txt

# Correcion para evitar errores de importacion con psql
cd clean
cat part-*.csv| sed 's/\"\"/AAAAAAAAAAA/g' > clean.csv

# importa datos hacia psq
PGPASSWORD=$password psql -U $user -h $host -d $db_name -c "\copy clean.rita FROM 'clean.csv' with null as E'AAAAAAAAAAA' CSV;"
rm -r ../semantic
echo "Data insertion on semantic.rita completed"

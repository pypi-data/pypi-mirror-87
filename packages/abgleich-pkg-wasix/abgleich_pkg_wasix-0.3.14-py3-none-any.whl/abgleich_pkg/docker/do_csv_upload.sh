#!/bin/bash

mkdir -p db-up

export PGPASSWORD='1qa2ws'
export TABLENAME='ABGLEICH'
export networkmode=host
export dbupdir="`pwd`/db-up"
export fn='../data/ABGLEICH.csv'

rm -f ${dbupdir}/${fn}
rm -f ${dbupdir}/create_table_abacusvgl.csv
cp  ./${fn} ${dbupdir}/${fn}

# Sample CSV data
head ${dbupdir}/${fn} |csvsql --no-constraints -d ',' -q '"'   --tables ${TABLENAME}  | sed 's/DECIMAL/NUMERIC/' | sed 's/VARCHAR/TEXT/' > ${dbupdir}/create_table_abacusvgl.csv


echo -e "\ndrop table..."
docker run -e POSTGRES_PASSWORD=1qa2ws -e PGPASSWORD="$PGPASSWORD" --rm --network=${networkmode}                    postgres  \
  psql -h localhost -p 15432 -U postgres -d mydb -c \
  "DROP TABLE IF EXISTS \"${TABLENAME}\";"


# Create table for loading 
# Uses host network to access database published on port 5432 of the host
echo -e "\ncreate table..."
docker run -e POSTGRES_PASSWORD="$PGPASSWORD" -e PGPASSWORD="$PGPASSWORD" --rm --network=${networkmode}   -v "${dbupdir}:/data"  postgres  \
  psql -h localhost -p 15432 -U postgres -d mydb -c "`cat ${dbupdir}/create_table_abacusvgl.csv`"

# \copy data from file (mounted by volume)
echo -e "\nupload csv..."
docker run -e POSTGRES_PASSWORD=1qa2ws -e PGPASSWORD="$PGPASSWORD" --rm --network=${networkmode}   -v "${dbupdir}:/data" postgres \
  psql -h localhost -p 15432 -U postgres -d mydb  -c \
    "\\copy \"${TABLENAME}\" FROM '/data/${fn}' WITH DELIMITER ',' CSV HEADER"


# Show content
echo -e "\nShow content..."
docker run -e POSTGRES_PASSWORD=1qa2ws -e PGPASSWORD="$PGPASSWORD" --rm --network=${networkmode}                     postgres  \
  psql -h localhost -p 15432 -U postgres  -d mydb -c \
  "SELECT count(*) FROM \"${TABLENAME}\";"


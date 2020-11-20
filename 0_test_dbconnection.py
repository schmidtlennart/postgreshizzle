import psycopg2
import sys

### Test reach db:

con = None

try:

    con =  psycopg2.connect("dbname='isewer' user='isewer_rw' host='postgres' port='5432' password='abwasser2020_rw'")

    cur = con.cursor()
    cur.execute('SELECT version()')

    version = cur.fetchone()[0]
    print(version)

except psycopg2.DatabaseError as e:

    print(f'Error {e}')
    sys.exit(1)

finally:

    if con:
        con.close()

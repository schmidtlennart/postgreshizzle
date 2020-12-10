import psycopg2
import sys
# get db log-in credentials
exec(open('100_config_passwords.py').read())
### Test reach db:
con = None

try:

    con =  psycopg2.connect(config_string_rw)

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

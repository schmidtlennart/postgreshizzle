exec(open('100_config_passwords.py').read())
#if local
#engine_string_rw = engine_string_local
# if admin on ufz postgres
eng_str = engine_string_adm

from sqlalchemy import create_engine
engine = create_engine(eng_str,executemany_mode='values',executemany_values_page_size=10000, executemany_batch_page_size=5000)
# check if connections works - will throw error if connection cannot be established
engine.connect()
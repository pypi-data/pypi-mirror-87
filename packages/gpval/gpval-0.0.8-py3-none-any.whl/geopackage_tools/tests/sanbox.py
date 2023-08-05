import os
from geopackage_tools.infra import db_conn
geo_file = '/home/ronenk1/dev/geopackage_tools/shlomiko9.GPKG'

db = db_conn.init(geo_file)

tables = db_conn.get_tables(db)
indices = db_conn.get_indices(db)
triggers = db_conn.get_triggers(db)

table_name = os.path.basename(geo_file).split('.')[0]
main_data = db_conn.list_table_columns(db, table_name)
db_conn.get_all_rows_tables(db, 'gpkg_tile_matrix')
print(tables)
print(indices)
print(triggers)
print(main_data)
print(os.path.abspath('.'))
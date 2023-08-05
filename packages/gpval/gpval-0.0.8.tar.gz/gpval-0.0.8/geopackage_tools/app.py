

import sqlite3
import os

geo_file = '//shlomiko9.GPKG'


def init(geo_file):
    """ initialize instance of sql cursor object to the package"""
    conn = sqlite3.connect(geo_file)
    return conn.cursor()


def list_tabels(cursor):
    """ query that scan all tables included on given geopackage"""
    cursor.execute("SELECT name FROM sqlite_master where type = 'table'")
    return [table[0] for table in cursor]


def list_indeces(cursor):
    """ query that scan all indices included on given geopackage"""
    cursor.execute("SELECT name FROM sqlite_master where type = 'index'")
    return [table[0] for table in cursor]

def list_triggers(cursor):
    """ query that scan all indices included on given geopackage"""
    cursor.execute("SELECT name FROM sqlite_master where type = 'trigger'")
    return [table[0] for table in cursor]

def list_table_columns(table_name):
    """ query that return all columns name in main table of content in geopackage"""
    cursor.execute("SELECT * FROM "+table_name)
    return list(map(lambda x: x[0], cursor.description))

cursor = init(geo_file)
gpkg_tabels_list = list_tabels(cursor)
gpkg_indices_list = list_indeces(cursor)
gpkg_triggers_list = list_triggers(cursor)

print("\nGeoPackage include %d tabels" % len(gpkg_tabels_list))
for i in gpkg_tabels_list:
    print(i)

print("\nGeoPackage include %d indices" % len(gpkg_indices_list))
for i in gpkg_indices_list:
    print(i)

print("\nGeoPackage include %d triggers" % len(gpkg_triggers_list))
for i in gpkg_triggers_list:
    print(i)

table_name = os.path.basename(geo_file).split('.')[0]
main_table_columns = list_table_columns(table_name)
print(main_table_columns)
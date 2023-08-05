import sqlite3


def init(geo_file) -> object:
    """
    initialize instance of sql cursor object to the package
    """
    conn = sqlite3.connect(geo_file)
    return conn.cursor()


def get_tables(cursor) -> list:
    """ query that scan all tables included on given geopackage"""
    cursor.execute("SELECT name FROM sqlite_master where type = 'table'")
    return [table[0] for table in cursor]


def get_indices(cursor) -> list:
    """ query that scan all indices included on given geopackage"""
    cursor.execute("SELECT name FROM sqlite_master where type = 'index'")
    return [table[0] for table in cursor]


def get_triggers(cursor):
    """ query that scan all triggers included on given geopackage"""
    cursor.execute("SELECT name FROM sqlite_master where type = 'trigger'")
    return [table[0] for table in cursor]


def list_table_columns(cursor, table_name):
    """ query that return all columns name in main table of content in geopackage"""
    cursor.execute("SELECT * FROM " + table_name)
    return list(map(lambda x: x[0], cursor.description))


def get_all_rows_tables(cursor, table_name):
    """ query that return all rows data included on given table name"""
    cursor.execute("SELECT * FROM "+table_name)
    return cursor.fetchall()


def get_index_query(cursor, table_name):
    """
    This method return data on index by table name
    """
    cursor.execute("SELECT * FROM sqlite_master WHERE type = 'index' AND tbl_name='"+table_name+"' ")
    return cursor.fetchall()


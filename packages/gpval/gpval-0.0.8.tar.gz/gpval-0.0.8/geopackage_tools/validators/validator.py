import os
import logging
from geopackage_tools.infra import db_conn as db
from geopackage_tools.config import *

_logger = logging.getLogger('gp_validator.validator')


def validate_tables(file_name, cursor):
    tables_names = db.get_tables(cursor)
    expected_tables = TABLES_LIST
    expected_tables.append(file_name)
    expected_tables = set(expected_tables)
    tables_names = set(tables_names)

    if expected_tables.issubset(tables_names):
        return True, tables_names
    else:
        return False, tables_names


def validate_index(cursor):
    indices_names = db.get_indices(cursor)

    if TILES_INDEX in indices_names:
        return True, indices_names
    else:
        return False, indices_names


#todo fix pixel size float precision error with numpy.isclose() after validating with sharon about standart
def validate_tile_matrix(cursor,table_name):
    """
    validate if all tile matrix table contain all relevant fields and data according standard
    """
    state = False
    VAL_START_ZOOM_LEVEL
    max_level = VAL_MAX_ZOOM_LEVEL

    res = db.get_all_rows_tables(cursor,table_name)
    expected_row_dict = {
        'zoom_level': VAL_START_ZOOM_LEVEL,
        'matrix_width': VAL_MAT_W,
        'matrix_height': VAL_MAT_H,
        'tile_width': VAL_TILE_W,
        'tile_height': VAL_TILE_H,
        'pixel_x_size': VAL_PIXEL_X_SIZE,
        'pixel_y_size': VAL_PIXEL_Y_SIZE
    }
    try:
        while expected_row_dict['zoom_level'] <= max_level:
            mat = res[expected_row_dict['zoom_level']]

            try:
                actual_row_dict = {
                    'zoom_level': mat[1],
                    'matrix_width': mat[2],
                    'matrix_height': mat[3],
                    'tile_width': mat[4],
                    'tile_height': mat[5],
                    'pixel_x_size': mat[6],
                    'pixel_y_size': mat[7]
                }
            except Exception as e:
                _logger.error('Error of some missed fields on tile matrix row, current raw are %s with message' % mat, str(e))
                return state, res

            if expected_row_dict == actual_row_dict:
                _update_dicts(expected_row_dict)
            else:
                _logger.error('wrong values of matrix, should be %s but actual %s' % (expected_row_dict, actual_row_dict))
                return state, res



    except Exception as e:
        _logger.error("Not valid gpkg_tile_matrix data, failed on iteration")
        return state, res
    return state, res


def _update_dicts(expected_row_dict):
    expected_row_dict['zoom_level'] += 1
    expected_row_dict['matrix_width'] *= 2
    expected_row_dict['matrix_height'] *= 2
    expected_row_dict['pixel_x_size'] /= 2
    expected_row_dict['pixel_y_size'] /= 2


def validate_crs(cursor, table_name):
    res = db.get_all_rows_tables(cursor, table_name)
    return res


def validate_tiles_index(cursor, table_name):
    """
    Validate the geopackage include tiles matrix indexing according x,y,z

    """
    res = db.get_index_query(cursor, table_name)
    indexes_names = [name[1] for name in res]
    if 'tiles_index' not in indexes_names:
        raise Exception('Index of tiles_matrix not exists')
    try:
        t_index = [idx for idx in res if idx[1] == 'tiles_index'][0][4]
    except Exception:
        raise Exception('Can not locate the tiles_index')
    res = 'zoom_level' in t_index and 'tile_column' in t_index and 'tile_row' in t_index
    return res, t_index

def aseert_package(url):
    """
    This method except package url and scan geopackage if valid
    :param url: geopackage location path
    :return: bool - True if package is ok, False if invalid package
    """

    cur = db.init(url)
    file_name = os.path.basename(url)

    # validate all tables consist + the  unique table related to file name
    state1, table_list = validate_tables(file_name.split('.')[0], cur)
    _logger.info('Checked if package consist all required tables: [%s]', state1)
    _logger.debug("Tables name that package [%s] contain: [%s]", file_name, " | ".join(table_list))

    # validate tile_matrix table consist all important rows
    cols_list = db.list_table_columns(cur, file_name.split('.')[0])
    state2 = all(elem in cols_list for elem in TILE_MATRIX_COLUMNS)
    _logger.info('Checked if table [tile_matrix] consist all required columns: [%s]', state2)
    _logger.debug("Columns name that tile_matrix table contain: [%s]", " | ".join(cols_list))

    # validate index
    state3, index_list = validate_index(cur)
    _logger.info('Checked if package consist required "%s" index: [%s]', TILES_INDEX, state3)
    _logger.debug("Indices name that package [%s] contain: [%s]", file_name, " | ".join(index_list))

    # validate crs
    crs_list = validate_crs(cur, GPKG_SPATIAL_REF_SYS)
    crs_type = [c[0] for c in crs_list]
    if CRS_WGS_84 in crs_type:
        idx = crs_type.index(CRS_WGS_84)
        crs = crs_list[idx]
        state4 = ORGANIZATION in crs and SRS_ID in crs
        _logger.info('Checked if package CRS data include the required system [WGS84] : [%s] ', state4)
        _logger.debug("CRS name that package [%s] contain: [%s]", file_name, " | ".join(crs_type))
        _logger.debug("CRS [%s] include current data [%s] ", CRS_WGS_84, " | ".join([str(c) for c in crs]))

    # validate tile_matrix indexing
    state5, index = validate_tiles_index(cur, file_name.split('.')[0])
    _logger.info('Checked if package include tiles_matrix indexing to table [%s]: %s', file_name.split('.')[0], state5)
    _logger.debug("tiles_matrix index: [%s]", index)
    ok = all([state1, state2, state3, state4, state5])
    return ok

import os
import logging
import math
from geopackage_tools.config import *
from geopackage_tools.infra import db_conn as db
from geopackage_tools.validators import validator as validator
_logger = logging.getLogger("gp_validator")
logging.getLogger().setLevel(logging.DEBUG)
geo_file = '/home/ronenk1/dev/geopackage_tools/shlomiko9.GPKG'
RES = validator.aseert_package(geo_file)
cur = db.init(geo_file)
file_name = os.path.basename(geo_file).split('.')[0]
validator.validate_tiles_index(cur, file_name)
res_tables, tables_names = validator.validate_tables(file_name, cur)
res_indices, indices_names = validator.validate_index(cur)

# validator.validate_tile_matrix(cur,"gpkg_tile_matrix")
validator.validate_crs(cur, GPKG_SPATIAL_REF_SYS)
_logger.info("tables created correct: %s, with names: %s" % (res_tables, "|".join(tables_names)))
_logger.info("indices created correct: %s, with names: %s" % (res_indices, "|".join(indices_names)))



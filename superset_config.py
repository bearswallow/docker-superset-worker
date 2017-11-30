import os

# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# superset metadata (slices, connections, tables, dashboards, ...).
# Note that the connection information to connect to the datasources
# you want to explore are managed directly in the web UI
SQLALCHEMY_DATABASE_URI = os.getenv('SUPERSET_METADATA_CONNECTION')

resultBackend = os.getenv('CELERY_RESULT_BACKEND')

# Celery work config, supporting async query
class CeleryConfig(object):
    BROKER_URL = os.getenv('BROKER_URL')
    CELERY_IMPORTS = 'superset.sql_lab'
    CELERY_RESULT_BACKEND = resultBackend
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
CELERY_CONFIG = CeleryConfig

# config results backend
import re
m = re.match(r'redis://([^:/]+):([0-9]+)/([0-9]+)', resultBackend)
backendHost = m.group(1)
backendPort = int(m.group(2))
backDb = int(m.group(3))
from werkzeug.contrib.cache import RedisCache
RESULTS_BACKEND = RedisCache(
    host=backendHost, port=backendPort, db=backDb,
    key_prefix= os.getenv('APPLICATION_PREFIX') + "_results:")

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("workerConfig")
logger.info("metadata storage: " + SQLALCHEMY_DATABASE_URI)
logger.info("broker url: " + CeleryConfig.BROKER_URL)
logger.info("Result backend url:" + CeleryConfig.CELERY_RESULT_BACKEND)
logger.info("RedisCache: { host: %s, port: %s, db: %s, key_prefix: %s }" % tuple([backendHost, backendPort, backDb, RESULTS_BACKEND.key_prefix]))
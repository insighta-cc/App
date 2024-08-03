"""
System config
"""

import os
class Config:
    """
    db config
    """
    host = os.getenv('MYSQL_HOST')
    username = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    port = os.getenv('MYSQL_PORT')
    dbname = os.getenv('MYSQL_DB')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_API_ENABLED = True


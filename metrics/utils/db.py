import os
import psycopg2
import logging

logger = logging.getLogger(__name__)


def connect_to_db() -> psycopg2.connect():
    connection = psycopg2.connect(user=os.environ['DB_USER'],
                                  password=os.environ['DB_PASSWORD'],
                                  host=os.environ['DB_HOST'],
                                  port="5432",
                                  database="postgres")
    return connection

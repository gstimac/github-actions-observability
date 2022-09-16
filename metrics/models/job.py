import datetime as dt
import json
import logging
import psycopg2
import metrics.utils.db as db

logger = logging.getLogger(__name__)


class Job:
    def __init__(self, job_id: int, run_id: int, runner_id: int, name: str, status: str,
                 conclusion: str, start_time: dt.datetime, end_time: dt.datetime, data: json) -> None:
        self.data = data
        self.end_time = end_time
        self.start_time = start_time
        self.conclusion = conclusion
        self.status = status
        self.name = name
        self.runner_id = runner_id
        self.run_id = run_id
        self.job_id = job_id

    def insert_job(self) -> int:
        try:
            connection = db.connect_to_db()
            cursor = connection.cursor()

            insert_query = """INSERT INTO jobs (id, run_id, runner_id, name, status, conclusion, start_time, end_time, data) 
                              VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            record_to_insert = (self.id, self.run_id, self.runner_id, self.name, self.status,
                                self.conclusion, self.start_time, self.end_time, self.data)
            cursor.execute(insert_query, record_to_insert)

            connection.commit()
            count = cursor.rowcount
            logger.info("Record inserted successfully into mobile table %", count)

        except (Exception, psycopg2.Error) as error:
            logger.error("Failed to insert record into jobs table: %s", error, stack_info=True)

        finally:
            if connection:
                cursor.close()
                connection.close()
            return count

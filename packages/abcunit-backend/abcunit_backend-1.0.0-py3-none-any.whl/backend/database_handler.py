import psycopg2
import os
from .base_handler import BaseHandler


class DataBaseHandler(BaseHandler):

    def __init__(self, error_types, table_name='results'):
        """
        :param error_types: (str list) List of the string names of the
        different types of errors that you want to log
        :param table_name: (str) Optional string name of the table logs
        will be insert into (default is 'results')
        """

        self.error_types = error_types
        connection_info = os.environ.get("ABCUNIT_DB_SETTINGS")
        if not connection_info:
            raise KeyError('Please create environment variable ABCUNIT_DB_SETTINGS'
                           'in for format of "dbname=<db_name> user=<user_name>'
                           'host=<host_name> password=<password>"')
        try:
            self.conn = psycopg2.connect(connection_info)
        except psycopg2.Error as err:
            print(err)
            raise ValueError('ABCUNIT_DB_SETTINGS string is incorrect. Should be'
                             'in for format of "dbname=<db_name> user=<user_name>'
                             'host=<host_name> password=<password>"')
        self.cur = self.conn.cursor()
        self.table_name = table_name
        self._create_table()

    def _create_table(self):
        """
        Creates a table called <self.table_name> with primary key id varchar(255)
        and result varchar(255), if one does not already exist
         """

        self.cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name}'
                         '(id varchar(255) PRIMARY KEY, result varchar(255) NOT NULL);')
        self.conn.commit()

    def _delete_table(self):
        """
        Drops the database table
        """

        self.cur.execute(f"DROP TABLE {self.table_name};")
        self.conn.commit()

    def get_result(self, identifier):
        """
        Selects the result of the job with the identifier parsed
        and returns it

        :param identifier: (str) Identifier of the job result
        :return: (str) Result of job
        """

        query = f"SELECT result FROM {self.table_name} " \
                f"WHERE id='{identifier}';"
        self.cur.execute(query)
        if self.cur.rowcount > 0:
            return self.cur.fetchone()[0]
        return None

    def get_all_results(self):
        """
        :return: (dict) Dictionary of all job identifiers mapped to
        their respective results
        """

        query = f"SELECT * FROM {self.table_name}"
        self.cur.execute(query)
        result_dict = {}
        for (name, result) in self.cur:
            result_dict[name] = result
        return result_dict

    def get_successful_runs(self):
        """
        :return: (str list) Returns a list of the identifiers of all
        successful runs
        """

        query = f"SELECT id FROM {self.table_name} " \
                "WHERE result='success';"
        self.cur.execute(query)
        return [name[0] for name in self.cur]

    def get_failed_runs(self):
        """
        :return: (dict) Dictionary of error types mapped to
        lists of job identifiers which result in them
        """

        query = f"SELECT id, result FROM {self.table_name} " \
                "WHERE result<>'success';"
        self.cur.execute(query)
        failures = dict([(key, []) for key in self.error_types])
        for (name, result) in self.cur:
            failures[result].append(name)
        return failures

    def delete_result(self, identifier):
        """
        Deletes entry specified by the given identifier
        from the database

        :param identifier: (str) Identifier of the job
        """

        query = f"DELETE FROM {self.table_name} " \
                f"WHERE id='{identifier}';"
        self.cur.execute(query)
        self.conn.commit()

    def delete_all_results(self):
        """
        Deletes all entries from the table
        """

        self.cur.execute(f"DELETE FROM {self.table_name};")
        self.conn.commit()

    def ran_successfully(self, identifier):
        """
        Returns true / false on whether the result with this
        identifier is successful

        :param identifier: (str) Identifier of the job result
        :return: (bool) Boolean on if job ran successfully
        """

        query = f"SELECT result FROM {self.table_name} " \
                f"WHERE id='{identifier}';"
        self.cur.execute(query)
        result = self.cur.fetchone()
        if result is not None:
            return result[0] == 'success'
        return False

    def count_results(self):
        """
        :return: (int) Number of results in the table
        """

        self.cur.execute(f"SELECT COUNT(*) FROM {self.table_name};")
        return self.cur.fetchone()[0]

    def count_successes(self):
        """
        :return: (int) Number of successfull results in the table
        """

        query = f"SELECT COUNT(*) FROM {self.table_name} " \
                "WHERE result='success';"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def count_failures(self):
        """
        :return: (int) Number of failed results in the table
        """

        query = f"SELECT COUNT(*) FROM {self.table_name} " \
                "WHERE result<>'success';"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def insert_success(self, identifier):
        """
        Inserts an entry into the table with a given identifier
        and the result 'success'

        :param identifier: (str) Identifier of the job
        """

        query = f"INSERT INTO {self.table_name} " \
                f"VALUES ('{identifier}', 'success');"
        self.cur.execute(query)
        self.conn.commit()

    def insert_failure(self, identifier, error_type):
        """
        Inserts an entry into the table with a given identifier
        and result from error_types

        :param identifier: (str) Identifier of the job
        :param error_type: (str) Result of the job, from the
        error_types list
        """

        query = f"INSERT INTO {self.table_name} " \
                f"VALUES ('{identifier}', '{error_type}');"
        self.cur.execute(query)
        self.conn.commit()

    def close(self):
        """
        Close connection with the database
        """

        self.cur.close()
        self.conn.close()

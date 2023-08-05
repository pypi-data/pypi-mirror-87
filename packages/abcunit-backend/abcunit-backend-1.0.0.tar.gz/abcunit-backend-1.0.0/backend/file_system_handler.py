import glob
import os
import functools
from .base_handler import BaseHandler


class FileSystemHandler(BaseHandler):

    def __init__(self, base_log_dir, n_facets, sep, error_types):
        """
        :param base_log_dir: (str) Path to top level directory for logs
        :param n_facets: (int) Number of facets used to describe each unit result
        :param sep: (str) Separator used for a result identifier
        :param error_types: (str list) List of the string names of the different
        types of errors that you want to log
        """

        self.error_types = error_types
        self.n_facets = n_facets
        self.sep = sep

        self.success_dir = os.path.join(base_log_dir, 'success')
        self.failure_dir = os.path.join(base_log_dir, 'failure')

    def validate(func):
        """
        Decorator to check if an identifier is of the correct format
        """

        @functools.wraps(func)
        def validate_identifier(*args, **kwargs):
            identifier = args[1]  # Assumes identifier is second argument
            if os.sep in identifier:
                raise ValueError
            return func(*args, **kwargs)
        return validate_identifier

    def _path_to_identifier(self, path):
        """
        Given a full path to a result returns its identifier

        :param path: (str) Path to result file
        :return: (str) Job identifier
        """

        # Getting the last n_facets number of items in the path and joining
        # them to create the relative identifier
        path_arr = path.split(os.sep)
        identifier = self.sep.join(path_arr[-self.n_facets:])
        return identifier

    def _identifier_to_path(self, identifier, result):
        """
        Given an identifier and a result, return a full path to its result file

        :param identifier: (str) Identifier of the job result
        :param result: (str) Result of the job
        :return: (str) Path to result file
        """

        id_path = identifier.replace(self.sep, os.sep)
        if result == 'success':
            return os.path.join(self.success_dir, id_path)
        else:
            return os.path.join(self.failure_dir, result, id_path)

    @validate
    def get_result(self, identifier):
        """
        Returns the value of a result given its identifier

        :param identifier: (str) Identifier of the job
        :return: (str) Result of job
        """

        path = self._identifier_to_path(identifier, 'success')
        if os.path.exists(path):
            return 'success'

        for error in self.error_types:
            path = self._identifier_to_path(identifier, error)
            if os.path.exists(path):
                return error

        return None

    def get_all_results(self):
        """
        :return: (dict) Dictionary of all job identifiers mapped to
        their respective results
        """

        results = {}
        for identifier in self.get_successful_runs():
            results[identifier] = 'success'

        error_dict = self.get_failed_runs()
        for (error_type, identifiers) in error_dict.items():
            for identifier in identifiers:
                results[identifier] = error_type

        return results

    def get_successful_runs(self):
        """
        :return: (str list) Returns a list of the identifiers of all
        successful runs
        """

        glob_pattern = os.path.join(self.success_dir, os.sep.join(['*' for _ in range(self.n_facets)]))
        files = glob.glob(glob_pattern)
        return [self._path_to_identifier(fname) for fname in files]

    def get_failed_runs(self):
        """
        :return: (dict) Dictionary of error types mapped to
        lists of job identifiers which result in them
        """

        failures = {}
        for error_type in self.error_types:
            glob_pattern = os.path.join(self.failure_dir, error_type, os.sep.join(['*' for _ in range(self.n_facets)]))
            files = glob.glob(glob_pattern)
            failures[error_type] = [self._path_to_identifier(fname) for fname in files]

        return failures

    @validate
    def delete_result(self, identifier):
        """
        Deletes result file from the file system given its identifier

        :param identifier: (str) Identifier of the job
        """

        path = self._identifier_to_path(identifier, 'success')
        if os.path.exists(path):
            os.unlink(path)

        for error in self.error_types:
            path = self._identifier_to_path(identifier, error)
            if os.path.exists(path):
                os.unlink(path)

    def delete_all_results(self):
        """
        Deletes all result files in the file system under the
        base_log_dir
        """

        success_pattern = os.path.join(self.success_dir, os.sep.join(['*' for _ in range(self.n_facets)]))
        # failure pattern +1 * to account for failure type dir
        failure_pattern = os.path.join(self.failure_dir, os.sep.join(['*' for _ in range(self.n_facets + 1)]))
        success_files = glob.glob(success_pattern)
        failure_files = glob.glob(failure_pattern)

        for success_file in success_files:
            os.unlink(success_file)

        for failure_file in failure_files:
            os.unlink(failure_file)

    @validate
    def ran_successfully(self, identifier):
        """
        Returns true / false on whether the result with this
        identifier is successful

        :param identifier: (str) Identifier of the job result
        :return: (bool) Boolean on if job ran successfully
        """

        path = self._identifier_to_path(identifier, 'success')
        return os.path.exists(path)

    def count_results(self):
        """
        :return: (int) Number of results in the table
        """

        return len(self.get_all_results())

    def count_successes(self):
        """
        :return: (int) Number of successful result files
        """

        return len(self.get_successful_runs())

    def count_failures(self):
        """
        :return: (int) Number of failure result files
        """

        size = 0
        error_dict = self.get_failed_runs()
        for error in error_dict.keys():
            size += len(error_dict[error])
        return size

    @validate
    def insert_success(self, identifier):
        """
        Creates a successful result file with the identifier passed

        :param identifier: (str) Identifier of the job
        """

        path = self._identifier_to_path(identifier, 'success')
        dr = os.path.dirname(path)

        if not os.path.isdir(dr):
            os.makedirs(dr)
        open(path, 'w')  # empty success file

    @validate
    def insert_failure(self, identifier, error_type):
        """
        Creates a failure result file using the identifier
        and error type parsed

        :param identifier: (str) Identifier of the job
        :param error_type: (str) Result of the job, from the
        error_types list
        """

        path = self._identifier_to_path(identifier, error_type)
        dr = os.path.dirname(path)

        if not os.path.isdir(dr):
            os.makedirs(dr)
        with open(path, 'w') as writer:
            writer.write(f'{error_type} has occurred!')

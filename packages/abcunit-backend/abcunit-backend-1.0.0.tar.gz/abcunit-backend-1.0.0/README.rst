
abcunit-backend
===============

Storage backends for an ABCUnit Framework, logging success and failures of process units.


Database Backend
----------------

To use this backend you will need to contact the JASMIN help desk (support@jasmin.ac.uk) and ask them to setup a postgresql database for you. Specify a name for the database and a username to login with. JASMIN support will get back to you with the user password and host name. 


After you have got your database, you'll need to export an environment variable called  ``$ABCUNIT_DB_SETTINGS`` and set it to a connection string for ``psycopg2``\ :

.. code-block::

   ABCUNIT_DB_SETTINGS="dbname=<name> user=<user> host=<host> password=<pwd>"

``DatabaseHandler`` class construction looks like this:

.. code-block::

   DatabaseHandler(error_types, table_name="results")

Where;


* ``error_types`` is a list of the string names of the different types of errors that you want to log
* ``table_name`` is the name of the table logs will be insert into

Connects to an existing database and creates a table to store results:

.. code-block::

   <table_name> (id varchar(255) PRIMARY KEY, result varchar(255) NOT NULL)

.. list-table::
   :header-rows: 1

   * - id
     - result
   * - facet1.facet2.facet3
     - success
   * - facet1.facet2.facet3
     - bad_file
   * - &#8942;
     - &#8942;



File System Backend
-------------------

``FileSystemHandler`` class construction looks like this:

.. code-block::

   FileSytemHandler(base_log_dir, n_facets, sep, error_types)

Where;


* ``base_log_dir`` is the string path to top level directory for logs
* ``n_facets`` is the number of facets used to describe each unit result
* ``sep`` is the separator used for a result identifier
* ``error_types`` is a list of the string names of the different types of errors that you want to log

Uses the file system to create log files marking success and failures, categorised by directory structure:

.. code-block::

   <log_base_dir>/success/facet1/facet2/facet3

   <log_base_dir>/failure/error_type/facet1/facet2/facet3

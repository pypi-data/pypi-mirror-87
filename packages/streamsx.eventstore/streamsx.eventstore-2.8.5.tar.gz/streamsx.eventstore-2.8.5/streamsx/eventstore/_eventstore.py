# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2018

import streamsx.spl.op
import streamsx.spl.types
from streamsx.topology.schema import CommonSchema, StreamSchema
from streamsx.spl.types import rstring
import os
import getpass
import wget
from tempfile import gettempdir
import shutil
import tarfile
import requests
import string
import random
import re
import urllib.parse as up
import json
import streamsx.database as db
from streamsx.toolkits import download_toolkit

_TOOLKIT_NAME = 'com.ibm.streamsx.eventstore'

def _add_toolkit_dependency(topo):
    # IMPORTANT: Dependency of this python wrapper to a specific toolkit version
    # This is important when toolkit is not set with streamsx.spl.toolkit.add_toolkit (selecting toolkit from remote build service)
    streamsx.spl.toolkit.add_toolkit_dependency(topo, 'com.ibm.streamsx.eventstore', '[2.0.0,3.0.0)')

def _add_store_file(topology, path):
    filename = os.path.basename(path)
    topology.add_file_dependency(path, 'opt')
    return 'opt/'+filename

def download_toolkit(url=None, target_dir=None):
    r"""Downloads the latest Eventstore toolkit from GitHub.

    Example for updating the Eventstore toolkit for your topology with the latest toolkit from GitHub::

        import streamsx.eventstore as es
        # download Eventstore toolkit from GitHub
        eventstore_toolkit_location = es.download_toolkit()
        # add the toolkit to topology
        streamsx.spl.toolkit.add_toolkit(topology, eventstore_toolkit_location)

    Example for updating the topology with a specific version of the Eventstore toolkit using a URL::

        import streamsx.eventstore as es
        url220 = 'https://github.com/IBMStreams/streamsx.eventstore/releases/download/v2.2.0/streamsx.eventstore.toolkits-2.2.0-20190731-0640.tgz'
        eventstore_toolkit_location = es.download_toolkit(url=url220)
        streamsx.spl.toolkit.add_toolkit(topology, eventstore_toolkit_location)

    Args:
        url(str): Link to toolkit archive (\*.tgz) to be downloaded. Use this parameter to 
            download a specific version of the toolkit.
        target_dir(str): the directory where the toolkit is unpacked to. If a relative path is given,
            the path is appended to the system temporary directory, for example to /tmp on Unix/Linux systems.
            If target_dir is ``None`` a location relative to the system temporary directory is chosen.

    Returns:
        str: the location of the downloaded Eventstore toolkit

    .. note:: This function requires an outgoing Internet connection
    .. versionadded:: 2.5
    """
    _toolkit_location = streamsx.toolkits.download_toolkit (toolkit_name=_TOOLKIT_NAME, url=url, target_dir=target_dir)
    return _toolkit_location


def configure_connection(instance, name='eventstore', database=None, connection=None, user=None, password=None, keystore_password=None, truststore_password=None, plugin_name=None, plugin_flag=None, ssl_connection=None):
    """Configures IBM Streams for a connection to IBM Db2 Event Store database.

    Creates an application configuration object containing the required properties with connection information.

    Example for creating a configuration for a Streams instance with connection details::

        from icpd_core import icpd_util
        from streamsx.rest_primitives import Instance
        import streamsx.eventstore as es
        
        cfg=icpd_util.get_service_instance_details(name='your-streams-instance')
        cfg[streamsx.topology.context.ConfigParams.SSL_VERIFY] = False
        instance = Instance.of_service(cfg)
        app_cfg = es.configure_connection(instance, database='TESTDB', connection='HostIP:Port1;HostIP:Port2', user='db2-user', password='db2-password')


    Args:
        instance(streamsx.rest_primitives.Instance): IBM Streams instance object.
        name(str): Name of the application configuration
        database(str): The name of the database, as defined in IBM Db2 Event Store.
        connection(str): The set of IP addresses and port numbers needed to connect to IBM Db2 Event Store, format: <HostIP:Port from JDBC URL>;<SCALA connection URL>
        user(str): Name of the IBM Db2 Event Store User in order to connect.
        password(str): Password for the IBM Db2 Event Store User in order to connect.
        keystore_password(str): Password for key store file.
        truststore_password(str): Password for trust store file.
        plugin_name(str): The plug-in name for the SSL connection.
        plugin_flag(str): Set "false" to disable SSL plugin. If not specified the default is plugin is used.
        ssl_connection(str): Set "false" to disable SSL connection. If not specified the default is SSL enabled.

    Returns:
        Name of the application configuration.
    """

    # Prepare operator (toolkit) specific properties for application configuration
    description = 'Config for Db2 Event Store connection ' + name
    properties = {}
    if database is not None:
        properties['databaseName']=database
    if connection is not None:
        properties['connectionString']=connection
    if user is not None:
        properties['eventStoreUser']=user
    if password is not None:
        properties['eventStorePassword']=password
    if keystore_password is not None:
        properties['keyStorePassword']=keystore_password
    if truststore_password is not None:
        properties['trustStorePassword']=truststore_password
    if plugin_name is not None:
        properties['pluginName']=plugin_name
    if plugin_flag is not None:
        properties['pluginFlag']=plugin_flag
    if ssl_connection is not None:
        properties['sslConnection']=ssl_connection

    # prepare app config credentials for jdbc toolkit
    if database is not None and connection is not None and user is not None and password is not None:
        if ';' in connection:
            credentials = {}
            conn = connection.split(";", 1)
            credentials['username']=user
            credentials['password']=password
            if ',' in conn[0]:
                jdbc_conn = conn[0].split(",", 1)
                jdbcurl = 'jdbc:db2://' + jdbc_conn[0] + '/' + database
            else:
                jdbcurl = 'jdbc:db2://' + conn[0] + '/' + database
            credentials['jdbcurl']=jdbcurl
            # add for app config
            properties ['credentials'] = json.dumps (credentials)
    
    # check if application configuration exists
    app_config = instance.get_application_configurations(name=name)
    if app_config:
        print ('update application configuration: '+name)
        app_config[0].update(properties)
    else:
        print ('create application configuration: '+name)
        instance.create_application_configuration(name, properties, description)
    return name


def _download_driver_file_from_url(url, tmpfile):
    r = requests.get(url)
    with open(tmpfile, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    return tmpfile

def _get_jdbc_driver():
    tmpfile = gettempdir() + '/ibm-event_2.11-1.0.jar'
    if os.path.isfile(tmpfile):
        return tmpfile
    else:
        _download_driver_file_from_url("https://github.com/IBMStreams/streamsx.eventstore/raw/develop/com.ibm.streamsx.eventstore/opt/ibm-event_2.11-1.0.jar", tmpfile)
        if os.path.isfile(tmpfile):
            return tmpfile
        else:
            raise ValueError("Invalid JDBC driver")


class SQLStatement(db.JDBCStatement):
    """Runs a SQL statement using Db2 Event Store client driver and JDBC database interface.

    The statement is called once for each input tuple received. Result sets that are produced by the statement are emitted as output stream tuples.
    
    This class bases :py:class:`db_ref:streamsx.database.JDBCStatement`, includes the JDBC driver ('ibm-event_2.11-1.0.jar') and sets defaults for Db2 Event Store database:

    * jdbc_driver_class = 'COM.ibm.db2os390.sqlj.jdbc.DB2SQLJDriver'
    * ssl_connection = True
    * keystore_type = 'PKCS12'
    * truststore_type = 'PKCS12'
    * plugin_name = 'IBMIAMauth'
    * security_mechanism = 15

    Example with "select count" statement and defined output schema with attribute ``TOTAL`` having the result of the query::

        import streamsx.eventstore as es

        sample_schema = StreamSchema('tuple<int32 TOTAL, rstring string>')
        sql_query = 'SELECT COUNT(*) AS TOTAL FROM SAMPLE.TAB1'
        query = topo.source([sql_query]).as_string()
        res = s.map(es.SQLStatement(credentials='eventstore'), schema=sample_schema)
        res.print()

    Args:
        credentials(dict|str): The credentials of the IBM cloud Db2 warehouse service in JSON or the name of the application configuration.
        options (kwargs): The additional optional parameters as variable keyword arguments.

    Returns:
        :py:class:`topology_ref:streamsx.topology.topology.Stream`: Result stream.

    .. note:: This function requires an outgoing Internet connection to download the driver if jdbc_driver_lib is not specified
    .. versionadded:: 2.7
    """
    def __init__(self, credentials, **options):
        jdbc_driver_lib = _get_jdbc_driver()  
        print ('jdbc_driver_lib: '+jdbc_driver_lib)

        super(SQLStatement, self).__init__(credentials, **options)
        self.jdbc_driver_lib = jdbc_driver_lib
        self.jdbc_driver_class='COM.ibm.db2os390.sqlj.jdbc.DB2SQLJDriver'
        self.ssl_connection=True
        self.keystore_type='PKCS12'
        self.truststore_type='PKCS12'
        self.plugin_name='IBMIAMauth'
        self.security_mechanism=15


def run_statement(stream, credentials, truststore, keystore, truststore_password=None, keystore_password=None, schema=None, sql=None, sql_attribute=None, sql_params=None, transaction_size=1, jdbc_driver_class='COM.ibm.db2os390.sqlj.jdbc.DB2SQLJDriver', jdbc_driver_lib=None, ssl_connection=True, keystore_type='PKCS12', truststore_type='PKCS12', plugin_name='IBMIAMauth', security_mechanism=15, vm_arg=None, name=None):
    """Runs a SQL statement using Db2 Event Store client driver and JDBC database interface.

    The statement is called once for each input tuple received. Result sets that are produced by the statement are emitted as output stream tuples.
    
    This function includes the JDBC driver ('ibm-event_2.11-1.0.jar') for Db2 Event Store database ('COM.ibm.db2os390.sqlj.jdbc.DB2SQLJDriver') in the application bundle per default.

    Supports two ways to specify the statement:

    * Statement is part of the input stream. You can specify which input stream attribute contains the statement with the ``sql_attribute`` argument. If input stream is of type ``CommonSchema.String``, then you don't need to specify the ``sql_attribute`` argument.
    * Statement is given with the ``sql`` argument. The statement can contain parameter markers that are set with input stream attributes specified by ``sql_params`` argument.

    Example with "select count" statement and defined output schema with attribute ``TOTAL`` having the result of the query::

        import streamsx.eventstore as es

        sample_schema = StreamSchema('tuple<int32 TOTAL, rstring string>')
        sql_query = 'SELECT COUNT(*) AS TOTAL FROM SAMPLE.TAB1'
        query = topo.source([sql_query]).as_string()
        res = es.run_statement(query, credentials=credentials, schema=sample_schema)
    

    Args:
        stream(streamsx.topology.topology.Stream): Stream of tuples containing the SQL statements or SQL statement parameter values. Supports :py:class:`topology_ref:streamsx.topology.schema.StreamSchema` (schema for a structured stream) or ``CommonSchema.String`` as input.
        credentials(dict|str): The credentials of the IBM cloud Db2 warehouse service in JSON or the name of the application configuration.
        truststore(str): Path to the trust store file for the SSL connection.
        keystore(str): Path to the key store file for the SSL connection.
        truststore_password(str): Password for the trust store file given by the truststore parameter.
        keystore_password(str): Password for the key store file given by the keystore parameter.
        schema(StreamSchema): Schema for returned stream. Defaults to input stream schema if not set.             
        sql(str): String containing the SQL statement. Use this as alternative option to ``sql_attribute`` parameter.
        sql_attribute(str): Name of the input stream attribute containing the SQL statement. Use this as alternative option to ``sql`` parameter.
        sql_params(str): The values of SQL statement parameters. These values and SQL statement parameter markers are associated in lexicographic order. For example, the first parameter marker in the SQL statement is associated with the first sql_params value.
        transaction_size(int): The number of tuples to commit per transaction. The default value is 1.
        jdbc_driver_class(str): The default driver is for Db2 Event Store database 'COM.ibm.db2os390.sqlj.jdbc.DB2SQLJDriver'.
        jdbc_driver_lib(str): Path to the JDBC driver library file. Specify the jar filename with absolute path, containing the class given with ``jdbc_driver_class`` parameter. Per default the 'ibm-event_2.11-1.0.jar' is added to the 'opt' directory in the application bundle.
        ssl_connection(bool): Use SSL connection, default is ``True``
        keystore_type(str): Type of the key store file, default is ``PKCS12``.
        truststore_type(str): Type of the key store file, default is ``PKCS12``.
        plugin_name(str): Name of the security plugin, default is 'IBMIAMauth'.
        security_mechanism(int): Value of the security mechanism, default is 15 (com.ibm.db2.jcc.DB2BaseDataSource.PLUGIN_SECURITY).
        vm_arg(str): Arbitrary JVM arguments can be passed to the Streams operator.
        name(str): Sink name in the Streams context, defaults to a generated name.

    Returns:
        :py:class:`topology_ref:streamsx.topology.topology.Stream`: Result stream.

    .. note:: This function requires an outgoing Internet connection to download the driver if jdbc_driver_lib is not specified
    .. versionadded:: 2.4
    .. deprecated:: 2.7.0
        Use the :py:class:`~SQLStatement`.
    """
    
    jdbc_driver_lib = _get_jdbc_driver()  
    print ('jdbc_driver_lib: '+jdbc_driver_lib)

    return db.run_statement(stream,
                            credentials,
                            schema=schema,
                            sql=sql,
                            sql_attribute=sql_attribute,
                            sql_params=sql_params,
                            transaction_size=transaction_size,
                            jdbc_driver_class=jdbc_driver_class,
                            jdbc_driver_lib=jdbc_driver_lib,
                            ssl_connection=ssl_connection,
                            truststore=truststore,
                            truststore_password=truststore_password,
                            keystore=keystore,
                            keystore_password=keystore_password,
                            keystore_type=keystore_type,
                            truststore_type=truststore_type,
                            plugin_name=plugin_name,
                            security_mechanism=security_mechanism,
                            vm_arg=vm_arg,
                            name=name)


class Insert(streamsx.topology.composite.ForEach):
    """Inserts tuple into a table using Db2 Event Store Scala API.

    Important: The tuple field types and positions in the IBM Streams schema must match the field names in your IBM Db2 Event Store table schema exactly.

    Creates the table if the table does not exist. Set the ``primary_key`` and ``partitioning_key`` in case the table needs to be created.

    Example of a Streams application inserting rows to a table in a Db2 Event Store database::

        import streamsx.eventstore as es

        # generate sample tuples with the schema of the target table
        s = topo.source([1,2,3,4,5,6,7,8,9])
        schema=StreamSchema('tuple<int32 id, rstring name>').as_tuple()
        s = s.map(lambda x : (x,'X'+str(x*2)), schema=schema)

        # insert tuple data into table as rows
        s.for_each(es.Insert(config='eventstore', table='SampleTable', schema_name='sample', primary_key='id', partitioning_key='id'))

    Args:
        table(str): The name of the table into which you want to insert rows.
        schema_name(str): The name of the table schema name of the table into which to insert data.
        database(str): The name of the database, as defined in IBM Db2 Event Store. Alternative this parameter can be set with function :py:meth:`~streamsx.eventstore.configure_connection`.
        connection(str): The set of IP addresses and port numbers needed to connect to IBM Db2 Event Store. Alternative this parameter can be set with function :py:meth:`~streamsx.eventstore.configure_connection`.
        user(str): Name of the IBM Db2 Event Store User in order to connect. Alternative this parameter can be set with function :py:meth:`~streamsx.eventstore.configure_connection`.
        password(str): Password for the IBM Db2 Event Store User in order to connect. Alternative this parameter can be set with function :py:meth:`~streamsx.eventstore.configure_connection`.
        config(str): The name of the application configuration. Value returned by the function :py:meth:`~streamsx.eventstore.configure_connection`.
        batch_size(int): The number of rows that will be batched in the operator before the batch is inserted into IBM Db2 Event Store by using the batchInsertAsync method. If you do not specify this parameter, the batchSize defaults to the estimated number of rows that could fit into an 8K memory page.
        front_end_connection_flag(bool): Set to ``True`` to connect through a Secure Gateway (for Event Store Enterprise Edition version >= 1.1.2 and Developer Edition version > 1.1.4)
        max_num_active_batches(int): The number of batches that can be filled and inserted asynchronously. The default is 1.        
        partitioning_key(str): Partitioning key for the table. A string of attribute names separated by commas. The partitioning_key parameter is used only, if the table does not yet exist in the IBM Db2 Event Store database.
        primary_key(str): Primary key for the table.  A string of attribute names separated by commas. The order of the attribute names defines the order of entries in the primary key for the IBM Db2 Event Store table. The primary_key parameter is used only, if the table does not yet exist in the IBM Db2 Event Store database.
        truststore(str): Path to the trust store file for the SSL connection.
        truststore_password(str): Password for the trust store file given by the truststore parameter. Alternative this parameter can be set with function :py:meth:`~streamsx.eventstore.configure_connection`.
        keystore(str): Path to the key store file for the SSL connection.
        keystore_password(str): Password for the key store file given by the keystore parameter. Alternative this parameter can be set with function :py:meth:`~streamsx.eventstore.configure_connection`.
        plugin_name(str): The plug-in name for the SSL connection. The default value is IBMIAMauth.      
        plugin_flag(str|bool): Set "false" or ``False`` to disable SSL plugin. If not specified, the default is use plugin.
        ssl_connection(str|bool): Set "false" or ``False`` to disable SSL connection. If not specified the default is SSL enabled.

    Returns:
        streamsx.topology.topology.Sink: Stream termination

    .. versionadded:: 2.8
    """

    def __init__(self, table, schema_name=None, database=None, connection=None, user=None, password=None, config=None, batch_size=None, front_end_connection_flag=None, max_num_active_batches=None, partitioning_key=None, primary_key=None, truststore=None, truststore_password=None, keystore=None, keystore_password=None, plugin_name=None, plugin_flag=None, ssl_connection=None):
        self.table = table
        self.schema_name = schema_name
        self.database = database
        self.connection = connection
        self.user = user
        self.password = password
        self.config = config
        self.batch_size = batch_size
        self.front_end_connection_flag = front_end_connection_flag
        self.max_num_active_batches = max_num_active_batches
        self.partitioning_key = partitioning_key
        self.primary_key = primary_key
        self.truststore = truststore
        self.truststore_password = truststore_password
        self.keystore = keystore
        self.keystore_password = keystore_password
        self.plugin_name = plugin_name
        self.plugin_flag = plugin_flag
        self.ssl_connection = ssl_connection

    def populate(self, topology, stream, name, **options) -> streamsx.topology.topology.Sink:

        if self.config is None and self.connection is None:
            raise ValueError("Either config parameter or connection must be set.")
        if self.config is None and self.database is None:
            raise ValueError("Either config parameter or database must be set.")

        # python wrapper eventstore toolkit dependency
        _add_toolkit_dependency(topology)

        _op = _EventStoreSink(stream, schema=None, connectionString=self.connection, databaseName=self.database, tableName=self.table, schemaName=self.schema_name, partitioningKey=self.partitioning_key, primaryKey=self.primary_key, name=name)
        if self.front_end_connection_flag is not None:
            if self.front_end_connection_flag is True:
                _op.params['frontEndConnectionFlag'] = _op.expression('true')
        if self.batch_size is not None:
            _op.params['batchSize'] = streamsx.spl.types.int32(self.batch_size)
        if self.max_num_active_batches is not None:
            _op.params['maxNumActiveBatches'] = streamsx.spl.types.int32(self.max_num_active_batches)
          
        if self.keystore is not None:
            _op.params['keyStore'] = _add_store_file(topology, self.keystore)
        if self.keystore_password is not None:
            _op.params['keyStorePassword'] = self.keystore_password
        if self.plugin_name is not None:
            _op.params['pluginName'] = self.plugin_name
        else:
            _op.params['pluginName'] = 'IBMIAMauth'
        if self.plugin_flag is not None:
            if isinstance(self.plugin_flag, (bool)):
                if self.plugin_flag:
                    _op.params['pluginFlag'] = _op.expression('true')
                else:
                    _op.params['pluginFlag'] = _op.expression('false')
            else:
                if 'true' in self.plugin_flag.lower():
                    _op.params['pluginFlag'] = _op.expression('true')
                else:
                    _op.params['pluginFlag'] = _op.expression('false')
        if self.ssl_connection is not None:
            if isinstance(self.ssl_connection, (bool)):
                if self.ssl_connection:
                    _op.params['sslConnection'] = _op.expression('true')
                else:
                    _op.params['sslConnection'] = _op.expression('false')
            else:
                if 'true' in self.ssl_connection.lower():
                    _op.params['sslConnection'] = _op.expression('true')
                else:
                    _op.params['sslConnection'] = _op.expression('false')
        if self.truststore is not None:
            _op.params['trustStore'] = _add_store_file(topology, self.truststore)
        if self.truststore_password is not None:
            _op.params['trustStorePassword'] = self.truststore_password

        if self.config is not None:
            _op.params['configObject'] = self.config
        else:
            if self.user is not None:
                _op.params['eventStoreUser'] = self.user
            if self.password is not None:
                _op.params['eventStorePassword'] = self.password

        return streamsx.topology.topology.Sink(_op)


def insert(stream, table, schema_name=None, database=None, connection=None, user=None, password=None, config=None, batch_size=None, front_end_connection_flag=None, max_num_active_batches=None, partitioning_key=None, primary_key=None, truststore=None, truststore_password=None, keystore=None, keystore_password=None, plugin_name=None, plugin_flag=None, ssl_connection=None, schema=None, name=None):
    """Inserts tuple into a table using Db2 Event Store Scala API.

    Important: The tuple field types and positions in the IBM Streams schema must match the field names in your IBM Db2 Event Store table schema exactly.

    Creates the table if the table does not exist. Set the ``primary_key`` and ``partitioning_key`` in case the table needs to be created.

    Example of a Streams application inserting rows to a table in a Db2 Event Store database::

        # provide connection endpoint information in format <HostIP:Port from JDBC URL>;<SCALA connection URL>
        es_connection = 'HostIP:Port1;HostIP:Port2'
        # generate sample tuples with the schema of the target table
        s = topo.source([1,2,3,4,5,6,7,8,9])
        schema=StreamSchema('tuple<int32 id, rstring name>').as_tuple()
        s = s.map(lambda x : (x,'X'+str(x*2)), schema=schema)
        # insert tuple data into table as rows
        res = es.insert(s, connection=es_connection, database='TESTDB', table='SampleTable', schema_name='sample', primary_key='id', partitioning_key='id')

    Args:
        stream(streamsx.topology.topology.Stream): Stream of tuples containing the fields to be inserted as a row. Supports :py:class:`topology_ref:streamsx.topology.schema.StreamSchema` (schema for a structured stream) as input. The tuple attribute types and positions in the IBM Streams schema must match the field names in your IBM Db2 Event Store table schema exactly.
        table(str): The name of the table into which you want to insert rows.
        schema_name(str): The name of the table schema name of the table into which to insert data.
        database(str): The name of the database, as defined in IBM Db2 Event Store. Alternative this parameter can be set with function :py:meth:`~streamsx.eventstore.configure_connection`.
        connection(str): The set of IP addresses and port numbers needed to connect to IBM Db2 Event Store. Alternative this parameter can be set with function :py:meth:`~streamsx.eventstore.configure_connection`.
        user(str): Name of the IBM Db2 Event Store User in order to connect. Alternative this parameter can be set with function :py:meth:`~streamsx.eventstore.configure_connection`.
        password(str): Password for the IBM Db2 Event Store User in order to connect. Alternative this parameter can be set with function :py:meth:`~streamsx.eventstore.configure_connection`.
        config(str): The name of the application configuration. Value returned by the function :py:meth:`~streamsx.eventstore.configure_connection`.
        batch_size(int): The number of rows that will be batched in the operator before the batch is inserted into IBM Db2 Event Store by using the batchInsertAsync method. If you do not specify this parameter, the batchSize defaults to the estimated number of rows that could fit into an 8K memory page.
        front_end_connection_flag(bool): Set to ``True`` to connect through a Secure Gateway (for Event Store Enterprise Edition version >= 1.1.2 and Developer Edition version > 1.1.4)
        max_num_active_batches(int): The number of batches that can be filled and inserted asynchronously. The default is 1.        
        partitioning_key(str): Partitioning key for the table. A string of attribute names separated by commas. The partitioning_key parameter is used only, if the table does not yet exist in the IBM Db2 Event Store database.
        primary_key(str): Primary key for the table.  A string of attribute names separated by commas. The order of the attribute names defines the order of entries in the primary key for the IBM Db2 Event Store table. The primary_key parameter is used only, if the table does not yet exist in the IBM Db2 Event Store database.
        truststore(str): Path to the trust store file for the SSL connection.
        truststore_password(str): Password for the trust store file given by the truststore parameter. Alternative this parameter can be set with function :py:meth:`~streamsx.eventstore.configure_connection`.
        keystore(str): Path to the key store file for the SSL connection.
        keystore_password(str): Password for the key store file given by the keystore parameter. Alternative this parameter can be set with function :py:meth:`~streamsx.eventstore.configure_connection`.
        plugin_name(str): The plug-in name for the SSL connection. The default value is IBMIAMauth.      
        plugin_flag(str|bool): Set "false" or ``False`` to disable SSL plugin. If not specified, the default is use plugin.
        ssl_connection(str|bool): Set "false" or ``False`` to disable SSL connection. If not specified the default is SSL enabled.
        schema(streamsx.topology.schema.StreamSchema): Schema for returned stream. Expects a Boolean attribute called ``_Inserted_`` in the output stream. This attribute is set to true if the data was successfully inserted and false if the insert failed. Input stream attributes are forwarded to the output stream if present in schema.            
        name(str): Sink name in the Streams context, defaults to a generated name.

    Returns:
        streamsx.topology.topology.Sink: Stream termination
        or
        Output Stream if ``schema`` parameter is specified. This output port is intended to output the information on whether a tuple was successful or not when it was inserted into the database.

    .. deprecated:: 2.8.0
        Use the :py:class:`~Insert`.
    """

    if config is None and connection is None:
         raise ValueError("Either config parameter or connection must be set.")
    if config is None and database is None:
         raise ValueError("Either config parameter or database must be set.")

    # python wrapper eventstore toolkit dependency
    _add_toolkit_dependency(stream.topology)

    _op = _EventStoreSink(stream, schema, connectionString=connection, databaseName=database, tableName=table, schemaName=schema_name, partitioningKey=partitioning_key, primaryKey=primary_key, name=name)
    if front_end_connection_flag is not None:
        if front_end_connection_flag is True:
            _op.params['frontEndConnectionFlag'] = _op.expression('true')
    if batch_size is not None:
        _op.params['batchSize'] = streamsx.spl.types.int32(batch_size)
    if max_num_active_batches is not None:
        _op.params['maxNumActiveBatches'] = streamsx.spl.types.int32(max_num_active_batches)
          
    if keystore is not None:
        _op.params['keyStore'] = _add_store_file(stream.topology, keystore)
    if keystore_password is not None:
        _op.params['keyStorePassword'] = keystore_password
    if plugin_name is not None:
        _op.params['pluginName'] = plugin_name
    else:
        _op.params['pluginName'] = 'IBMIAMauth'
    if plugin_flag is not None:
        if isinstance(plugin_flag, (bool)):
            if plugin_flag:
                _op.params['pluginFlag'] = _op.expression('true')
            else:
                _op.params['pluginFlag'] = _op.expression('false')
        else:
            if 'true' in plugin_flag.lower():
                _op.params['pluginFlag'] = _op.expression('true')
            else:
                _op.params['pluginFlag'] = _op.expression('false')
    if ssl_connection is not None:
        if isinstance(ssl_connection, (bool)):
            if ssl_connection:
                _op.params['sslConnection'] = _op.expression('true')
            else:
                _op.params['sslConnection'] = _op.expression('false')
        else:
            if 'true' in ssl_connection.lower():
                _op.params['sslConnection'] = _op.expression('true')
            else:
                _op.params['sslConnection'] = _op.expression('false')
    if truststore is not None:
        _op.params['trustStore'] = _add_store_file(stream.topology, truststore)
    if truststore_password is not None:
        _op.params['trustStorePassword'] = truststore_password

    if config is not None:
        _op.params['configObject'] = config
    else:
        if user is not None:
            _op.params['eventStoreUser'] = user
        if password is not None:
            _op.params['eventStorePassword'] = password

    if schema is not None:
        return _op.outputs[0]
    else:
        return streamsx.topology.topology.Sink(_op)


class _EventStoreSink(streamsx.spl.op.Invoke):
    def __init__(self, stream, schema, tableName, connectionString=None, databaseName=None, schemaName=None, batchSize=None, configObject=None, eventStorePassword=None, eventStoreUser=None, frontEndConnectionFlag=None, maxNumActiveBatches=None, partitioningKey=None, preserveOrder=None, primaryKey=None, keyStore=None, keyStorePassword=None, pluginFlag=None, pluginName=None, sslConnection=None, trustStore=None, trustStorePassword=None, vmArg=None, name=None):
        topology = stream.topology
        kind="com.ibm.streamsx.eventstore::EventStoreSink"
        inputs=stream
        schemas=schema
        params = dict()
        if vmArg is not None:
            params['vmArg'] = vmArg
        if connectionString is not None:
            params['connectionString'] = connectionString
        if databaseName is not None:
            params['databaseName'] = databaseName
        if tableName is not None:
            params['tableName'] = tableName
        if schemaName is not None:
            params['schemaName'] = schemaName
        if batchSize is not None:
            params['batchSize'] = batchSize
        if configObject is not None:
            params['configObject'] = configObject
        if eventStorePassword is not None:
            params['eventStorePassword'] = eventStorePassword
        if eventStoreUser is not None:
            params['eventStoreUser'] = eventStoreUser
        if frontEndConnectionFlag is not None:
            params['frontEndConnectionFlag'] = frontEndConnectionFlag
        if maxNumActiveBatches is not None:
            params['maxNumActiveBatches'] = maxNumActiveBatches
        if partitioningKey is not None:
            params['partitioningKey'] = partitioningKey
        if preserveOrder is not None:
            params['preserveOrder'] = preserveOrder
        if primaryKey is not None:
            params['primaryKey'] = primaryKey
        if keyStore is not None:
            params['keyStore'] = keyStore
        if keyStorePassword is not None:
            params['keyStorePassword'] = keyStorePassword
        if pluginFlag is not None:
            params['pluginFlag'] = pluginFlag
        if pluginName is not None:
            params['pluginName'] = pluginName
        if sslConnection is not None:
            params['sslConnection'] = sslConnection
        if trustStore is not None:
            params['trustStore'] = trustStore
        if trustStorePassword is not None:
            params['trustStorePassword'] = trustStorePassword

        super(_EventStoreSink, self).__init__(topology,kind,inputs,schema,params,name)




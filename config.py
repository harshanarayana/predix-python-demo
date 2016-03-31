#!/usr/bin/python
"""
    This file acts as the basic configuration generation utility that lets
    the end user setup the basic setup required to run this demo app.

    This applications requires the following resources to be there or the
    settings will be defaulted to match the requirements to run this app
    on the local machine instead of the Predix.io Cloud ENV.
"""

# Import Library Requirements.
import os
import json

# Lets define some global variable for safety.
CONFIG_FILE = "./config/config.json"
CONFIG_DICT = dict()


def __check_file(file_name):
    """
        This function acts as a fail-safe to make sure that the a file
        exists. This can come in handy when trying to read data from
        the configuration files.

        @:parameter
            file_name   -   File to Check

        @:return
            True        -   Exists
            False       -   Doesn't Exist
    """
    if os.path.isfile(file_name):
        return True
    else:
        return False


def __parse_config_file(file_name):
    """
        This function is used to Read and parse the configuration file if
        for some reason, I fail to obtain some required parameters from
        the OS' environment variable.

        @:parameter
            file_name   -   Input JSON file to Reas

        @:return
            json_data   -   Dictionary of JSON data from Python
    """
    with open(file_name) as data:
        json_data = json.load(data)

    return json_data


def get_rest_information(instance_type="prod"):
    """
        This function is used to return the RestFul service information
        back to the Flask App initiator so that the Flask Server can be
        started on the Port and the Host specified by the User.

        We make use of the ENV File and the Configuration file in order
        to perform this operation.

        @:parameter:
            instance_type   -   Parameter used to Identify the Run Mode.
                                Defaults to Prod.
        @:returns:
            host_name   -   Host Name that needs to be used to run Flask
            port_number -   Port on which the Flask Application must run
            debug       -   Enable or Disable Debug Mode based on ENV
    """
    port_number = 9099
    host_name = "0.0.0.0"
    debug = False
    global CONFIG_DICT
    global CONFIG_FILE

    if __check_file(CONFIG_FILE):
        CONFIG_DICT = __parse_config_file(CONFIG_FILE)

    if instance_type == "prod":
        if os.getenv("PORT") is not None:
            port_number = int(os.getenv("PORT"))
        elif CONFIG_DICT.get("port") is not None:
            port_number = int(CONFIG_DICT.get("port"))
        else:
            port_number = 9099

        if os.getenv("HOST_NAME") is not None:
            host_name = os.getenv("HOST_NAME")

        if os.getenv("DEBUG") is not None:
            if os.getenv("DEBUG"):
                debug = True

        if CONFIG_DICT.get("debug") is not None:
            if CONFIG_DICT.get("debug"):
                debug = True
    else:
        if __check_file(CONFIG_FILE):
            CONFIG_DICT = __parse_config_file(CONFIG_FILE)
            if CONFIG_DICT.get("port") is not None:
                port_number = int(CONFIG_DICT.get("port"))
            else:
                port_number = 9099
        else:
            port_number = 9099

        if os.getenv("DEBUG") is not None:
            if os.getenv("DEBUG"):
                debug = True

        if CONFIG_DICT.get("debug") is not None:
            if CONFIG_DICT.get("debug"):
                debug = True

    return host_name, port_number, debug


def get_rabbit_mq_config():
    """
        This function serves up the RabbitMQ Message Queue related settings
        on a platter to the end user.

        These settings are essential in establishing a connection to the MQs
        in the Predix.io machine for making use of them in the code base.

        @:returns
            host_name           -   RabbitMQ Host Name Identifier.
            message_queue_name  -   Name of the message Queue to to be used.
                                    This needs to Pre-exist in RabbitMQ.
    """
    host_name = "localhost"
    message_queue_name = "pq"
    global CONFIG_DICT

    if CONFIG_DICT.get("rabbitmq") is not None:
        host_name = CONFIG_DICT.get("rabbitmq").get("hostname")
        message_queue_name = CONFIG_DICT.get(
            "rabbitmq").get("message_queue_name")

    if 'VCAP_SERVICES' in os.environ:
        if os.environ.get('VCAP_SERVICES') is not None \
                and json.loads(os.environ.get(
                    "VCAP_SERVICES")).get("p-rabbitmq-35") is not None:
            VCAP_SERVICES = json.loads(os.environ.get("VCAP_SERVICES"))
            rabbit_mq = VCAP_SERVICES.get("p-rabbitmq-35")
            if rabbit_mq[0].get("credentials") is not None \
                    and rabbit_mq[0].get(
                        "credentials").get("amqp") is not None:
                ampq = rabbit_mq[0].get("credentials").get("amqp")
                if ampp.get("host") is not None:
                    host_name = ampq.get("host")
    return host_name, message_queue_name


def get_redis_config():
    """
        This function is used to serve-up the Redis Settings to the enduser.
        This is required to setup an in Memory Cache system that can be used
        in conjunction with Postgresql for faster in memory processing and
        quick turn around read time for data processing.

        This is never to be used as a data storage system since this is only
        an In-memory system.

        @:returns
            hostname    -   Redis machine host name to be used for connecting
            port        -   Redis Port to use for Connection
            password    -   Password Field to be used for connection.
    """
    hostname = "localhost"
    port = 6379
    password = ''
    global CONFIG_DICT

    if CONFIG_DICT.get("redis") is not None:
        hostname = CONFIG_DICT.get("redis").get("hostname")
        port = CONFIG_DICT.get("redis").get("port")
        password = CONFIG_DICT.get("redis").get("password")

    if 'VCAP_SERVICES' in os.environ:
        VCAP_SERVICES = json.loads(os.environ.get("VCAP_SERVICES"))
        if VCAP_SERVICES is not None \
                and VCAP_SERVICES.get("redis-3") is not None:
            redis = VCAP_SERVICES.get("redis-3")[0]
            if redis.get("credentials") is not None:
                hostname = redis.get("credentials").get("host", "localhost")
                port = redis.get("credentials").get("port", 6379)
                password = redis.get("credentials").get("password", '')

    return hostname, port, password


def get_postgresql_config():
    """
        This function checks through each items in the ENV Variable, Config
        file as well as the Custom Default items in order to return the
        parameters required to set up a PostgreSQL connection.

        @:returns
            database    -   Database to Use as Default.
            user        -   User name for invoking connection.
            password    -   Password to Establish PostgreSQL connection
            host        -   Host Name to use
            port        -   Connection port for PostgreSQL.
    """
    database = "test"
    user = "postgres"
    password = "password"
    host = "127.0.0.1"
    port = "4532"
    global CONFIG_DICT

    if CONFIG_DICT.get("postgres") is not None:
        database = CONFIG_DICT.get("postgres").get("database")
        user = CONFIG_DICT.get("postgres").get("user")
        password = CONFIG_DICT.get("postgres").get("password")
        host = CONFIG_DICT.get("postgres").get("host")
        port = CONFIG_DICT.get("postgres").get("port")

    if "VCAP_SERVICES" in os.environ:
        VCAP_SERVICES = json.loads(os.environ.get("VCAP_SERVICES"))
        if VCAP_SERVICES is not None \
                and VCAP_SERVICES.get("postgres") is not None:
            postgres = VCAP_SERVICES.get("postgres")[0]
            if postgres.get("credentials") is not None:
                database = postgres.get("credentials").get("database")
                user = postgres.get("credentials").get("username")
                password = postgres.get("credentials").get("password")
                host = postgres.get("credentials").get("host")
                port = postgres.get("credentials").get("port")

    return database, user, password, host, port

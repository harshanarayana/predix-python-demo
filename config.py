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


def get_rest_information(instance_type = "prod"):
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
    """
    port_number = 9099
    host_name = "0.0.0.0"
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
    else:
        if __check_file(CONFIG_FILE):
            CONFIG_DICT = __parse_config_file(CONFIG_FILE)
            if CONFIG_DICT.get("port") is not None:
                port_number = int(CONFIG_DICT.get("port"))
            else:
                port_number = 9099
        else:
            port_number = 9099

    return host_name, port_number


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

    global  CONFIG_DICT

    if CONFIG_DICT.get("rabbitmq_host") is not None:
        host_name = CONFIG_DICT.get("rabbitmq_host")

    if CONFIG_DICT.get("rabbitmq_queue") is not None:
        message_queue_name = CONFIG_DICT.get("rabbitmq_queue")

    if 'VCAP_SERVICES' in os.environ:
        if os.environ.get('VCAP_SERVICES') is not None \
                and os.environ.get("VCAP_SERVICES").get("p-rabbitmq-35") is not None:
            rabbit_mq = os.environ.get("VCAP_SERVICES").get("p-rabbitmq-35")
            if rabbit_mq[0].get("credentials") is not None \
                    and rabbit_mq[0].get("credentials").get("amqp") is not None:
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
    if 'VCAP_SERVICES' is os.environ:
        if os.environ.get("VCAP_SERVICES") is not None \
                and os.environ.get("VCAP_SERVICES").get("redis-3") is not None:
            redis = os.environ.get("VCAP_SERVICES").get("redis-3")[0]
            if redis.get("credentials") is not None:
                hostname = redis.get("credentials").get("host", "localhost")
                port = redis.get("credentials").get("port", 6379)
                password = redis.get("credentials").get("password", '')

    return hostname, port, password


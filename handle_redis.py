#!/usr/bin/python
"""
    This file acts as a platform on which all your Redis actions are
    performed. All Necessary seetings and configurations are build and
    handled in this file.

    An object of this can be created and used as per the user convenience.
"""
import redis
import json


class RedisHandler(object):
    """
        This is the class that user needs to make use of, for handling
        all REDIS related activities.

        This provides a simple interface which the users can make use
        of and handle the Redis Changes. The contents of this file,
        for this demo application is very primitive and can be extended.
    """
    def __init__(self, host="localhost", port=6379, password=""):
        """
            Constructor Function.

            @:parameter
                host        -   Redis Host
                port        -   Redis Connection Port
                password    -   Redis Connection Password
        """
        self.host = host
        self.port = port
        self.password = password
        self.redis = None
        self.error_found = False
        self.__initialize()
        self.info = None
        self.error = ""

    def __initialize(self):
        """
            This is the base initializer function that is invoked from
            the __init__ function. This sets-up all your REDIS required
            constraints.
        """
        try:
            self.redis = redis.StrictRedis(
                host=self.host,
                port=self.port,
                password=self.password)
            self.info = self.redis.info()
        except redis.ConnectionError:
            """
                For the purpose of this function, lets set a variable saying
                we faced an error setting up REDIS.
            """
            self.error = "Connection Error trying to Access REDIS."
            self.error_found = True

    def add_to_redis(self, key, value=None):
        """
            This function acts as an interface that the user can make use of
            for creating an item in the REDIS Cache for Processing/any other
            req.

            @:parameter
                key     -   Key to use for Setting Redis Item.
                value   -   Value to be set for the key.
        """
        try:
            self.redis.set(key, value)
        except:
            self.error_found = True
            self.error = "Failed to Set Value " + value + " to Key " + key

    def get_from_redis(self, key):
        """
            This function acts as an interface while the user tries to obtain
            a value from the REDIS cache.

            @:parameter
                key     -   Key to Check in Redis

            @:return
                value   -   Value for the Key mentioned above that's in REDIS.
        """
        try:
            if key is None:
                self.error_found = True
                self.error = "Can't have a None/Null value for Key while " + \
                             "trying read data from REDIS"
                return ""
            else:
                return self.redis.get(key)
        except:
            self.error_found = True
            self.error = "Failed to get value for Key " + key
            return self.error

    def add_to_redis_list(self, key, value=None):
        """
            This function acts as an interface to let the user add an item to
            an array in REDIS.

            @:parameter
                key     -   Key to use for Setting Redis Item.
                value   -   Value to Append to the Redis List.
        """
        try:
            self.redis.rpush(key, value)
        except:
            self.error_found = True
            self.error = "Failed to Append Value " + value + \
                         " to list with Key " + key

    def check_error(self):
        """
            This function acts as an error check mechanism to safely handle
            all the breakage scenario.

            @:return
                error   -   Error Message
        """
        if self.error_found:
            return self.error

    def get_all_keys(self):
        """
            This function acts as an interface that can be used to obtain a
            list of all the Key value pairs in the Redis Cache.
            This returns a list of Lists with 2 values in each of the internal
            lists.

            @:return
                redis_data  -   List of Redis Items stored.
        """
        redis_data = list()
        try:
            redis_keys = self.redis.keys()
            for key in redis_keys:
                value = self.redis.get(key)
                if type(value) is list:
                    temp = ""
                    for v in value:
                        temp += str(v)
                    value = temp
                item = dict()
                item['key'] = key
                item['value'] = value
                redis_data.append(item)
            return redis_data
        except:
            self.error_found = True
            self.error = "Failed to Obtain Redis Key value Info."
            return ["Error", self.error]

    def reset_error(self):
        """
            Reset Error Message.
        """
        self.error_found = False
        self.error = ""

    def get_redis_info(self):
        """
            This acts as a wrapper to be used for obtaining the Redis
            connection related information.

            @:return
                info    -   A Dictionary containing Redis Info.
        """
        try:
            return json.dumps(
                self.redis.info(),
                sort_keys=True,
                indent=8,
                separators=(',', ': '))
        except:
            self.error_found = True
            self.error = "Error Trying to Read Redis Infomration"
            return self.error

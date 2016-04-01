#!/usr/bin/python
"""
    This file acts as the Entry Point to the Rest Services that will be
    deployed on the Predix.io page for Demo Purpose.

    @Authour : Harsha Narayana
"""

# Import Basic Library requirements.
from flask import Flask, render_template, request, \
    jsonify, make_response, Response
from config import get_rest_information, get_redis_config, \
    get_postgresql_config
from handle_redis import RedisHandler
from handle_postgres import PostgreSQL
from flask.ext.httpauth import HTTPBasicAuth
import md5
from functools import wraps

# Some Global Variable to handle REDIS, POSTGRES and RABBITMQ.
REDIS = None
POSTGRES = None
COUNTER = 1
AUTHENTICATION = {
    "username": "5cc0ad025dd42c5b70e193e77fcc5e96",
    "password": "5f4dcc3b5aa765d61d8327deb882cf99"
}

# This line initializes a Flask Application for the Current __name__.
app = Flask(__name__)
app.config['SECRET_KEY'] = "Luke I am Your Father !"
auth = HTTPBasicAuth()


"""
    The Routing Functions are listed in the Below Code Section. Please be
    careful while making changes to the Routing. They can break our app
    if not done in the right way.
"""


# Basic Error Handler Mode. This will come in handly in case your application
# runs into an error. This can return a JSON response string.
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Write a Custom authentication mode function that gets invoked each time you
# try to validate an incoming request with the help of HTTPAuth.
def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        authentication = request.authorization
        if authentication.get("username") is None or authentication.get("password") is None:
            return Response('Failed Login! Missing Credentials',
                            401,
                            {'WWW-Authenticate': 'Basic realm="Auth!"'})
        if not validate_credentials(
                authentication.get("username"), authentication.get("password")):
            return Response('Failed Login! Invalid Credentials.',
                            401,
                            {'WWW-Authenticate': 'Invalid Credentials'})
        return f(*args, **kwargs)
    return wrapper


# This is the base URL Routing Function. Let's put a Sample Demo HTML page in
# here.
@app.route('/')
def home():
    """
        This Page Renders a basic HTML page with a Message displayed in h3.
    """
    return render_template("index.html")


# A Sample Routing path to show how the Routing for Different URL works.
@app.route("/sample/")
def sample():
    """
        This Page Renders the Same Message as Basic HTML Home page. Along with
        that, it adds an extra line to differentiate the content.
    """
    return render_template("sample.html")


# Following Section Shows an HTML form for the User and Prompts him to enter
# an input message which gets pushed to a Secondary Page for Rendering.
@app.route("/signup/")
def signup():
    """
        This Page Prompts the User with an HTML page that expects him to enter
        Name and Email information and Submit it.
    """
    return render_template("signup.html")


# The Following Section of the Code acts as a Post Submit Action Handler that
# processes the incoming POST request from the Browser to Flask and processes
# it accordingly.
@app.route("/submit/", methods=["POST"])
def submit():
    """
        The Following page handles the Incoming Form that is submitted by
        the User and Sends a response back in HTML format.

        This behavior can be reproduced on any rest services.
    """
    username = request.form['username']
    email = request.form['useremail']
    return render_template("submit.html", name=username, email=email)


# The following Function is used to Test the REDIS connection using the
# Rest Mode. This show the usage of Redis as an in-memory cache before
# it can be persisted onto any of the Databases.
@app.route("/redis-signup/")
def redis_signup():
    return render_template("signup.html", redis=1)


# The following section of the code acts as a POST RESTful service API that
# adds the data to Redis Key-Value store and Persists to DB if specified in
# the payload. otherwise, it simply ignores the data and sends a JSON
# response back in succsss mode.
@app.route("/redis-rest-submit", methods=["POST"])
def create_redis_item():
    """
        This function takes an incoming payload from a RESTful POST request
        and processes it to look for the following keys.

        1. redis
        2. persist

        Based on the value of the keys mentioned above it performs one of the
        tasks below as applicable
    """
    global REDIS
    global POSTGRES
    global COUNTER
    has_redis = False
    persist = False
    message = dict()

    if not request.json or 'payload' not in request.json:
        message = {
            "state": "failure",
            "error": "payload key not found. Invalid Payload Data"
        }
        return jsonify({'message': message}), 400

    if 'username' not in request.json.get('payload') or \
            'email' not in request.json.get('payload'):
        message = {
            "state": "failure",
            "error": "username & email are mandatory. Invalid Payload Data."
        }
        return jsonify({'message': message}), 400
    payload = request.json.get('payload')

    if payload.get('username') is None or payload.get('email') is None:
        message = {
            "state": "failure",
            "error": "Username & email can't be empty. Invalid payload data."
        }
        return jsonify({'message': message}), 400

    if 'redis' in request.json:
        if request.json.get('redis'):
            has_redis = True

    if 'persist' in request.json:
        if request.json.get('persist'):
            persist = True

    message = {
        "state": "successful",
        "info": "Hello, young padawan " + payload.get("username") + "," +
        " the FORCE is strong with you. \n" +
        "You have a long way to go before you become a Jedi. " +
        "I will drop you a tutorial at " + payload.get("email")
    }

    if has_redis:
        message['info'] = ""
        REDIS.add_to_redis(payload.get("username"), payload.get("email"))
        REDIS.add_to_redis("inserts", COUNTER)
        COUNTER += 1
        message['info'] = "Hello, master " + payload.get("username") + \
            ", the ONE RING has been waiting for you all this time. \n" + \
            "Looks like we finally found each other. " + \
            "To claim the ONE RING, please check your email " + \
            payload.get("email")
        message['redis_status'] = "stored"

    if persist:
        query = "INSERT INTO DEMO (USERNAME, EMAIL) VALUES(%s, %s)"
        POSTGRES.run_query_store(
            query_string=query,
            binding=(
                payload.get("username"),
                payload.get("email")
            )
        )
        message['persist'] = "successful"

    return jsonify({'message': message}), 200


# The Following Section of the Code acts as a Post Submit Action Handler that
# processes the incoming POST request from the Browser to Flask and processes
# it accordingly.
@app.route("/redis-submit/", methods=["POST"])
@authenticate
def redis_submit():
    """
        The Following page handles the Incoming Form that is submitted by
        the User and Sends a response back in HTML format.

        This behavior can be reproduced on any rest services.
    """
    global REDIS
    global COUNTER
    global POSTGRES
    username = request.form['username']
    email = request.form['useremail']
    persist = request.form.get('persist')
    if persist is not None:
        persist = 1
    else:
        persist = 0

    if REDIS is None or REDIS.check_error():
        if REDIS is not None:
            message = REDIS.check_error()
        else:
            message = "No REDIS Object Handler Found."
        return render_template(
            "error.html",
            name=username,
            email=email,
            message=message)
    REDIS.reset_error()
    REDIS.add_to_redis(username, email)
    REDIS.add_to_redis("inserts", COUNTER)
    COUNTER += 1

    if persist:
        query = "INSERT INTO DEMO (USERNAME, EMAIL) VALUES(%s, %s)"
        POSTGRES.run_query_store(query_string=query, binding=(username, email))

    if REDIS.check_error():
        return render_template(
            "error.html",
            name=username,
            email=email,
            message=REDIS.check_error())
    else:
        return render_template(
            "submit.html",
            name=username,
            email=email,
            redis=1)


# The following Code is for Displaying the Entities in the Redis Cache.
@app.route("/get-redis")
def get_redis():
    """
        This Function obtains the data in Redis KEY Value pair and returns them
        in an array so that it can be rendered into a neat table in the HTML.
    """
    global REDIS
    redis_data = REDIS.get_all_keys()
    return render_template("redis.html", redis_data=redis_data)


# This route is provided for you to check if the REDIS connection is setup
# or not before going ahead.
@app.route("/redis-status")
def redis_status():
    global REDIS
    return render_template(
        "redis_status.html",
        json_data=REDIS.get_redis_info())


# This Route acts as a way to check the Status for PostgreSQL.
@app.route("/postgres-status")
def postgres_status():
    global POSTGRES
    (status, message) = POSTGRES.check_status()
    if status:
        status = 1
    else:
        status = 0
    if len(message) < 1:
        message = "PostgreSQL Connection Successfully established."
    return render_template(
        "postgres_status.html",
        status=status,
        message=message)


# This function Routes the request made by the End user into a function that
# handles the process of getting the data from PostgreSQL machine and
# displaying it to the end user in HTML table format.
@app.route("/get-postgres")
def get_postgres():
    global POSTGRES
    postgres_data = POSTGRES.run_query("SELECT * FROM DEMO")
    postgres_info = list()
    for row in postgres_data:
        item = dict()
        item['id'] = row[0]
        item['key'] = row[1]
        item['value'] = row[2]
        postgres_info.append(item)
    return render_template("postgres.html", postgres_data=postgres_info)


"""
    Authentication Based RESTful Services Example.
"""


# Write an authentication mechanism that can be used to validate incoming
# requests from the user. This is a basic authentication with static data.
def validate_credentials(username, password):
    """
        Performs a basic MD5 based Authentication for both user and pass.
    """
    global AUTHENTICATION
    md5user = md5.new(username)
    md5pass = md5.new(password)
    return AUTHENTICATION.get("username") == md5user.hexdigest() and AUTHENTICATION.get("password") == md5pass.hexdigest()


# Basic Function that Takes a Set of Authentication values in BASIC Auth mode
# to validate the incoming RESTful requests.
@app.route("/authenticate/")
@authenticate
def authenticate_rest():
    """
        This is a sample function that lets you use the basic auth mode for
        performing user authentication as part of the RESTful requests.
    """
    message = {
        "state": "success",
        "message": "Oh Captain, My Captain."
    }
    return jsonify({'message': message}), 200


# This section of the Code Starts-up your Flask Application.
if __name__ == "__main__":
    (flask_hostname, flask_port, flask_debug) = get_rest_information()
    (redis_hostname, redis_port, redis_password) = get_redis_config()
    (postgres_database, postgres_user, postgres_password,
     postgres_host, postgres_port) = get_postgresql_config()
    if REDIS is None:
        REDIS = RedisHandler(
            host=redis_hostname,
            port=redis_port,
            password=redis_password)

    if POSTGRES is None:
        POSTGRES = PostgreSQL(database=postgres_database,
                              user=postgres_user,
                              password=postgres_password,
                              host=postgres_host,
                              port=postgres_port)
    app.run(
        host=flask_hostname,
        port=flask_port,
        debug=flask_debug)

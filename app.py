#!/usr/bin/python
"""
    This file acts as the Entry Point to the Rest Services that will be
    deployed on the Predix.io page for Demo Purpose.

    @Authour : Harsha Narayana
"""

# Import Basic Library requirements.
from flask import Flask, render_template, request, url_for
from config import get_rest_information, get_rabbit_mq_config, get_redis_config
from handle_redis import RedisHandler

# Some Global Variable to handle REDIS, POSTGRES and RABBITMQ.
REDIS = None
COUNTER = 1

# This line initializes a Flask Application for the Current __name__.
app = Flask(__name__)


"""
    The Routing Functions are listed in the Below Code Section. Please be
    careful while making changes to the Routing. They can break our app
    if not done in the right way.
"""


# This is the base URL Routing Function. Let's put a Sample Demo HTML page in here.
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


# The Following Section of the Code acts as a Post Submit Action Handler that
# processes the incoming POST request from the Browser to Flask and processes
# it accordingly.
@app.route("/redis-submit/", methods=["POST"])
def redis_submit():
    """
        The Following page handles the Incoming Form that is submitted by
        the User and Sends a response back in HTML format.

        This behavior can be reproduced on any rest services.
    """
    global REDIS
    global  COUNTER
    username = request.form['username']
    email = request.form['useremail']
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
    REDIS.add_to_redis(username, email)
    REDIS.add_to_redis("inserts", COUNTER)
    COUNTER += 1
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


# This section of the Code Starts-up your Flask Application.
if __name__ == "__main__":
    (flask_hostname, flask_port, flask_debug) = get_rest_information()
    (redis_hostname, redis_port, redis_password) = get_redis_config()
    if REDIS is None:
        REDIS = RedisHandler(
            host=redis_hostname,
            port=redis_port,
            password=redis_password)

    app.run(
        host=flask_hostname,
        port=flask_port,
        debug=flask_debug
    )
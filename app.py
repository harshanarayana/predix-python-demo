#!/usr/bin/python
"""
    This file acts as the Entry Point to the Rest Services that will be
    deployed on the Predix.io page for Demo Purpose.

    @Authour : Harsha Narayana
"""

# Import Basic Library requirements.
from flask import Flask, render_template, request, url_for
from config import get_rest_information, get_rabbit_mq_config, get_redis_config

# This line initializes a Flask Application for the Current __name__.
app = Flask(__name__)

"""
    The Routing Functions are listed in the Below Code Section. Please be
    careful while making changes to the Routings. They can break our app
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


# This section of the Code Starts-up your Flask Application.
if __name__ == "__main__":
    (flask_hostname, flask_port) = get_rest_information()
    app.run(
        host=flask_hostname,
        port=flask_port
    )
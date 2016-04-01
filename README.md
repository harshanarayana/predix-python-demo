<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Introduction](#introduction)
- [Tech-Stack Requirements](#tech-stack-requirements)
- [Setup](#setup)
- [Usage](#usage)
  - [Usage - Run - Local Machines](#usage---run---local-machines)
  - [Usage - Push to Predix.io](#usage---push-to-predixio)
    - [Setting Up Predix.io](#setting-up-predixio)
    - [Pushing to Predix.io Cloud](#pushing-to-predixio-cloud)
    - [Customizing and Using](#customizing-and-using)
  - [Application Routing - Help](#application-routing---help)
  - [Application Structure](#application-structure)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Introduction #

This is a Python based application that was created for the purpose of DEMO. This application does not specific operation that has any business value. 

This application can be used as a reference application while you are trying to build your own custom application that you want to deploy on the [Predix.io](https://www.predix.io) Cloud.

This application can be run and tested both on the local machine as well as the Predix Cloud. The Following section of the document contain a detailed list of all the Tech-Stack required to run this application on local machines for testing and development purpose before it is deployed onto the Predix Cloud.

# Tech-Stack Requirements #

The following section details the tech-stack requirement that needs to be met for you to be able to test and run this application locally. Any other versions not mentioned in the section below haven't been tested and can be used at your own discretion.

1. [Python 2.7.6](http://www.activestate.com/activepython)
2. [Redis >= 3.0](http://redis.io/download)
3. [PostgreSQL >= 9.3.X](http://www.postgresql.org/download/)
4. [Python pip = 8.1.1](https://pypi.python.org/pypi/pip)
5. Any Code editor of your choice.

# Setup #

This section of the document contains details on how to setup the local environment for you to be able to run/test and develop this application locally.

> All commands mentioned in the following section refer to a Linux System. You will have to replace them with their equivalent Windows commands if required.

1. Setup the Tech-Stack Details mentioned in the section above. Install the versions and softwares as applicable to your machines.
2. Install Python Library dependencies.
```sudo pip install requirements.txt```
3. Start the Following Services if they are not already running.
```sudo service postgresql start && sudo service redis_6379 status```
4. Reset PostgreSQL password for the user ```postgres``` to ```password```
  * [Reference Link 1](http://scratching.psybermonkey.net/2009/06/postgresql-how-to-reset-user-name.html)
  * [Reference Link 2](http://www.postgresql.org/docs/9.1/static/auth-pg-hba-conf.html)
5. Restart the Services for PostgreSQL. ```sudo services postgresql restart```
6. Clone this Repository.

# Usage #
## Usage - Run - Local Machines ##
Running this application on local machine is just a single command away. 
```bash
    python app.py
```

After you run the above command, point the URL to the address mentioned in the Command line using your favorite browser and voila. 

## Usage - Push to Predix.io ##
Before you can push this application into the Predix.io machine, there are a few pre-requisites that are to be done from your side. Following section of the document contains a detailed information on what needs to be done.

### Setting Up Predix.io ###

Follow the setps described below to setup the Predix 

1. Create an account on [Predix.io](https://www.predix.io) Cloud.
2. Create a Space
3. Follow the Instructions and tutorials in the [Predix.io](https://www.predix.io) Cloud. to setup Cloud Foundry items on your machine.
4. Access the [Catalog](https://www.predix.io/catalog/) Section to Setup Some basic services.
  1. [Key-Value Store : Redis](https://www.predix.io/services/service.html?id=1215) Name this service as ```dev```
  2. [SQL Database : PostgreSQL](https://www.predix.io/services/service.html?id=1178) Name this service as ```testpsql```
5. Setup CF login in your machine. 

### Pushing to Predix.io Cloud ###

This application is a generic application build for the purpose of Demo and can easily be published onto the Predix.io Cloud with very minimal changes. The following set of changes are essential.

1. Modify the ```manifest.yml``` file to change the application name.
  ```yml

    ---
    applications:
    - name: predix-demo-raildocs-python #Modify this Application name to a Unique name.
      memory: 1G
      build_pack: python_buildpack
      command: python app.py
      stack: cflinuxfs2
      services: # If you have named your services differently, update them.
      - dev  # Redis Service
      - testpsql  # PostgreSQL Service
  ```
2.Perform a ```cf push``` from directory where ```manifest.yml``` file exists.

### Customizing and Using ###

This application can be customized and modified before you can push to the Predix.io Cloud as well. And follows steps are to be done in order to make sure that there are no problem while doing so.

1. Update the Code and Test on Local machine using 
2. [Follow the Steps mentioned in the above section.](#pushing-to-predixio-cloud)

## Application Routing - Help ##

This application has some basic routing modes built for the purpose of testing and demo. Below is a list of all the Routes that are available and what each of them do.

| Routing Paths    | Python Function | Description                                                                                               |
|------------------|-----------------|-----------------------------------------------------------------------------------------------------------|
| /                | home            | This is the base page that loads up when you point the URL to the default Predix.io Application Home Page |
| /sample          | sample          | This is the first sample URL that routes away from the Home page into a new page/URL                      |
| /signup          | signup          | This is the HTML form that is used to perform a POST request on the Application                           |
| /submit          | submit          | This is the HTML page that renders after the request from /signup is successfully completed               |
| /redis-signup    | redis_signup    | This is the HTML form that is used to perform a POST request on the application with REDIS and PostgreSQL |
| /redis-submit    | redis_submit    | This is the HTML page that renders after the request from /redis-signup is successfully completed         |
| /redis-rest-submit| create_redis_item| This is the RESTful Function responsible for storing data into Redis and PostgreSQL.                    |
| /get-redis       | get_redis       | This is the HTML page that contains the details of each Key-Value pair in REDIS                           |
| /redis-status    | redis_status    | This is the HTML page that displays the REDIS status information                                          |
| /postgres-status | postgres_status | This is the HTML page that displays the PostgreSQL status information                                     |
| /get-postgres    | get_postgres    | This is the HTML page that displays the data stored in PostgreSQL's DEMO table.                           |

## Application Structure ##

The following section contains the infomration about the Directory strucutre of this application.

```yml

|-- app.py                      # Main Application File.
|-- config.py                   # Global Config Settings File
|-- handle_postgres.py          # PostgreSQL Handler
|-- handle_redis.py             # Redis Handler
|-- manifest.yml                # CF Manifest File
|-- predix-python-demo.iml      # IntelliJ IDEA Config File.
|-- Procfile                    # Proc File
|-- README.md                   # Readme.
|-- requirements.txt            # Pip Installation List
|-- static
|   `-- style.css               # Static Style Sheet File.
`-- templates 
    |-- error.html              # Error Display Page.
    |-- index.html              # Home Page Template
    |-- postgres.html           # PostgreSQL Info Dispaly Template
    |-- postgres_status.html    # PostgreSQL Status Display Template
    |-- redis.html              # Redis Key-Value Display Template
    |-- redis_status.html       # Redis Status Display Template
    |-- sample.html             # Sample Template File.
    |-- signup.html             # HTML Submit Form
    `-- submit.html             # HTML Respose Page.

```
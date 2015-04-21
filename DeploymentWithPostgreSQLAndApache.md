# Here's how to deploy ERP Libre with a Postgres db and Apache with mod\_wsgi in a GNU/Linux environment.

Using the default setup options with a sqlite db and single OS user is not recommended if you need to deploy ERP Libre for multiple client instances and hosts. Using sqlite limits the possible host users (and therefore client installations) to one because of system user rights issues. For multiple instances, it's recommended to use the PostgreSQL database engine. Note that the Apache server configuration is only needed if you intend to implement a high performance web application, for less requirements you might want to consider using web2py's rocket built-in server or  other software (i.e. nginx).

## Pre-requisit-t-tes ##

  * PostgreSQL
  * Python >= 2.5
  * wxPython
  * python-psycopg2
  * web2py configured with Apache and mod\_wsgi

Note: OS console commands used in this wiki are based in Ubuntu 12.04 distribution (please check your OS documentation for other syntaxes or commands available)

## Preparing your pg database ##

To create an erplibre user and database in your system's PostgreSQL installation, open a terminal and type the following:

```
]$ sudo -u postgres createuser -P -s erplibre
]$ sudo -u postgres createdb -O erplibre -E UTF-8 erplibre
```

For client applications over the network you'll need to configure postgres server to allow remote db connections. Detailed options of PostgreSQL connection and authentication can be read at:

  * [setting parameters](http://www.postgresql.org/docs/9.1/static/config-setting.html)
  * [connection](http://www.postgresql.org/docs/9.1/static/runtime-config-connection.html)
  * [hba\_conf](http://www.postgresql.org/docs/9.1/static/auth-pg-hba-conf.html)

## Now, for something completely different ##

We're going to install ERP Libre gui and web applications in the Apache/mode\_wsgi user space. This is needed for the webapp to have read/write access to ERP Libre files

If your web2py installation did not create a wsgi daemon user homedir, you should create one (for Ubuntu installation script it is www-data):

```
]$sudo mkdir /home/<username>
]$sudo chown -R <username> /home/<username>
```

Next step is to download and unzip erplibre zip installer into the wsgi user homedir
and run the installation.

```
]$cd <wsgi user homedir>/erplibre
]$sudo -u <wsgiuser> python install.py
```

Skip web2py installation so you can provide the installer with the path to where it was installed for Apache.
When asked for the connection string use the new pg database and user defined previously:

postgres://erplibre:`<`password`>`@`<`host name or IP address`>`/erplibre

Now you should have a working erplibre webapp available at yourhost/erplibre

## Add client desktop apps ##

Adding client app instances is much more simple.

Just unzip the erplibre installer on each user homedir and run the installation using the same connection string as in the server installation, using this command:

```
/home/<user>/erplibre]$python install_client.py
```

For db demo setup and other initial configurations see this [wiki](http://code.google.com/p/erplibre/wiki/FirstStepsWithERPLibreGUI)
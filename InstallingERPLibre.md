# explains how to install ERP Libre

# INSTALLATION INSTRUCTIONS #

Wether you unzip a copy of the installation file or clone the erplibre gui repository, the target folder becomes the root of the application instance, so before running the setup script you can choose to keep the original target folder or change the installation path to a new one in your system by copying the target folder to another location.

### Application dependencies ###

Your system must have the following software dependencies in order to
install ERP Libre:

  * Python - http://www.python.org `*`
  * web2py - http://www.web2py.com `*`
  * wxPython (wx for short) - http://sourceforge.net/projects/wxpython/
  * gui2py -http://code.google.com/p/gui2py/

`*` Setup version 1.0.0 installs web2py and gui2py by default. To skip this installations use `./setup.py --install --no_dep`

---


When you install ERP Libre for a new empty database, db initialization is not performed by the installation facility, instead, it is made when calling ./main.py for starting the desktop application for the first time. Note that this step is required for the web2py application to work properly.

### Installation with .zip archive ###
  1. Unzip erplibre.zip somewhere in your user folder
  1. Open a terminal in your operating system (run -> cmd for win)
  1. From the new extracted application folder run this command:

` python setup.py --install `

The command will start a wizard to install dependencies and configure the application.
If there are no errors in console output, you have now a working copy of ERP Libre in your system

### Installation from the mercurial repository ###

1 Make a clone of the _gui_ repository in your system
> From a terminal run:

` hg clone https://code.google.com/p/erplibre.gui/ ./erplibre `

2 Inside the new created folder run:

` python setup.py --install `

### Alternative no\_gui installation ###

There is an installation mode wich disables the gui interface for install ERP Libre in case you
cannot run a desktop environment. The target system still needs the before mentioned dependencies (Python, wxPython, web2py and gui2py)
and the script will exit with an error code if they are not satisfied. Note that this script waits for user input during installation

from the erplibre unzipped/downloaded folder run:

` python setup.py --install --no_gui `

To skip the path requests you can also pass this arguments:
  * --web2py\_path <absolute. path to web2py>
  * --gui2py\_path <absolute path to gui2py>

### Installing multiple instances (network db clients) ###

If you installed ERP Libre with a PostgreSQL connection, it is possible to
share the database for inter-operating clients.

Each client instance has its own installation for different network machines. So any installed gui app within the network (wether it is LAN or WAN based) can have access to the database for CRUD functions

Here is how to install multiple clients:

Make sure the client system has all dependencies installed:
(See _Application dependencies_)
Your client system will also need the python PostgreSQL driver _psycopg2_

1 Download and unzip the installation zipped package or clone the ERP Libre gui repository in a new folder in your user space.

2 Change the system current directory to the new gui app folder

3 Type this command:

` python setup.py --install --client --no_web2py_app `

The _client_ option instructs ERP Libre to avoid altering the remote database but still write the needed local database files

_no\_web2py\_app_ tells ERP Libre to install the app without writing the web app to the local web2py installation. (this would add a duplicated webapp since it is normally installed at the same system as your initial gui app installation)

4 The client app is started with the same terminal command as the initial server application:

` python main.py `

### Choosing language file on installation ###

It is possible to set the gui application language on installation with the _language_ argument

This example configures the gui app to use the spanish language file

` install <other installation arguments> --language es-es `

Note that for default english interface this argument is not needed.

You can configure the language option in the setup page after installing the application
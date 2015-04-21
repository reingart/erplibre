# Exposes command line options for ERP Libre modules.

# Options for command modules of ERP Libre #

The accepted syntax for terminal commands is
` ./module.py --arg1 arg2 arg2 arg2value -arg3 `
Note that it is possible to use dash [-], double dash [--] or just the argument, but [arg1=value] is not supported

### setup.py ###
  * _--install_ : Start server/client configuration. It asks for the web2py/gui2py folders, db URI, and wether it must install the webapp in the current web2py installation. Writes the config.ini file with the installation basic parameters
  * _--no\_web2py\_app_ : Do not install the web2py application (used with _--install_)
  * _--client_ : Configure as client gui application (used with _--install_)
  * _--no\_gui_ : Skip graphical dialogs on installation. Displays the installation options in the terminal (used with _--install_)
  * _--web2py\_path_: Absolute path to the local web2py installation (used with _--install_)
  * _--gui2py\_path_: Absolute path to the local gui2py installation (used with _--install_)
  * _--hmc\_key_: special key for web2py auth encryption. You must use the same hmac\_key for all inter-operating installations (used with _--install_)
  * _--language_: configure language file. Use the language[-country] notation. For example es-es for spanish and Spain. The required language file must be included in the languages gui app folder. By default ERP Libre is configured for the english language (used with _--install_)

### main.py ###
  * _--user_ : authentication string with the form user@mailserver:password to auto login on application start.
  * _--legacy\_db_ : Tells ERP Libre to avoid db errors by skipping database modifications
  * _--verbose_ : Return extra script progress information in standard output
  * _--db\_timeout_ : An integer in milliseconds to reset the database connection periodically (used to prevent network issues with remote databases. Only available for PostgreSQL)
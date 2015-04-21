# How to start using the gui desktop application

# Post-installation setup #

To start using ERP Libre you must first create an administrative user and load the database initial records (i.e. the demo database) for the configured database connection (by default the database included with the installation files)

  * At the HTML panel (work space) click the _setup_ link
  * Enter the user's email in the user field
  * When finishing the first start admin user registration form, click on the link _login_ and complete the form with the new user authentication email and password
  * The standard output emits a warning message because the user has no referenced contact record in the database. This parameter can be provided later.
  * To avoid the repeated warning about user contact information, click on _specify firm's tin_. Enter a tin number from the list (the list is only available after loading the db data with company information records. See the section _Demo database setup_) and accept the form. If the tin value is accepted, a validation message is sent to the standard output.

### Demo database setup ###

Some modules and functions of ERP Libre need an initial set of db records to work properly.

When a new instance of ERP Libre is installed in the system, there is no database records unless it is connected to a pre-existent db.

To load database records you must be logged in as an administrative user (See _first steps_ to create the admin user and login instructions)

In order to load demo records to a new database from the gui application, a CSV load action is provided at the setup html interface:

Go to setup from the initial html view. Click on the link _Load db records from a CSV file_

  * _path_ is the absolute system route to the db\_example folder in your ERP Libre installation path
  * _file_ is the name of the CSV data file to load (the demo file names included with the installation have the form _erplibre\_languagename\_example\_db.csv_)
  * _suspend integrity check_ option prevents errors when uploading csv data. For PostgreSQL, a superuser database connection is required.
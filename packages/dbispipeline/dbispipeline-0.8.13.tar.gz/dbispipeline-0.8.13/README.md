# DBIS Pipeline
This pipline can be used to run analyses in a structured way, and stores
configurations and results in a database.

## Usage

the user writes a minimal plan file which contains only the following
information:
 * "how do I get the data?", by providing a dataloader
 * "what to do with the data?", by providing a scikit pipeline
 * "how to process the result?", by providing result handlers.
 * "where to additionally store results?" by providing storage handlers.


Please have a look at the examples for more information.

### CLI
We provide a `dbispipeline-link` tool that can be used to link datasets to
the data directory. To use this feature provide a `data/links.yaml` file.

An example could look like this:
```yaml
---
datasets:
  - music/acousticbrainz
  - music/billboard
  - music/millionsongdataset
```

To set the root path where the datasets are linked from either set the CLI
parameter or configure the dbispipeline acordingly (See the sample config
below).


## Requirements

* python >= 3.6
* a PostgreSQL database
* an email server if you want to use notification emails


## Installation

1. Install dbispipeline in your python. We recommend using pipenv to keep your
   dependencies clean: `pipenv install dbispipeline`
   This call will install a virtual environment as well as all dependencies.
2. Write your plan(s). See the example plan files for guidance.
3. call `pipenv run dp <yourplanfile.py>`

Enjoy!


## Configuration
The framework look in multiple directories for its configuration files.
* `/usr/local/etc/dbispipeline.ini` used for system wide default.
* `$HOME/.config/dbispipeline.ini` used for user specific configurations.
* `./dbispipeline.ini` for project specific configurations.

And example configuration file looks like this:
```ini
[database]

# url to your postgres database
host = your.personal.database

# your database user name
user = user

# port of your postgres database, default = 5432
# port = 5432

# password of your database user
password = <secure-password>

# database to use
database = pipelineresults

# table to be used
result_table = my_super_awesome_results

[project]
# this will be stored in the database
name = dbispipeline-test

# this is used to store backups of the execution
# it is possible to override this by setting the DBISPIPELINE_BACKUP_DIR
# environment variable
# the default is the temp dir of the os if this option is not set.
backup_dir = tmp

# this is used to linke the used datasets spcified in data/links.yaml
# it is possible to override this by setting the DBISPIPELINE_DATASET_DIR
# environment variable
dataset_dir = /storage/nas/datasets

[mail]
# email address to use as sender
sender = botname@yourserver.com

# recipient. This should probably be set on a home-directory-basis.
recipient = you@yourserver.com

# smtp server address to use
smtp_server = smtp.yourserver.com

# use smtp authentication, default = no
# authenticate = no

# username for smtp authentication, required if authenticate = yes
# username = foo

# password for smtp authentication, required if authenticate = yes
# password = bar

# port to use for smtp server connection, default = 465
# port = 465
```

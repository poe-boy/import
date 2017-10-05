# PoEBoy Importer

## Requirements

* Python 3.6+
* Docker latest

## Setup

* Removes existing postgres docker container if existing
* Starts up new docker container
* Runs the setup on the database (db creation, schema, etc...)

```bash
$ ./setup.sh
```

**If you are already running postgres with the `postgres` name, you can run the following to delete the poeboy database and set up.**

```bash
$ ./reset.sh
```

## Run

```bash
$ python import.py
```

## TODO

* Save more data than just the `next_change_id`
* Do a polling check instead of exiting if no new changes

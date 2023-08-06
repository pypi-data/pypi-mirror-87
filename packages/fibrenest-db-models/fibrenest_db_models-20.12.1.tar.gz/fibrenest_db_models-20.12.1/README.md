# fibrenest_db_models
This is the DB schema and sqlalchemy db models for fibrenest

# Usage
You would want to install this module in your project and then import the 
needed db model.  
There is separate model if the backend DB is postgres. 

DB Models for OLD Mysql DB are in `old.py`

#### Installation
`pip install fibrenest-db-models`

#### Example import for postgres
`from fibrenest_db_models.postgres import *`

#### Example import for all other DBs
`from fibrenest_db_models.all import *`

#### Creating the DB and tables
If the DB is not created, then you would need to first create the DB. Use [sqlalchemy-utils](https://sqlalchemy-utils.readthedocs.io/en/latest/database_helpers.html) for this.  

After the DB is created, you can connect to this DB and create tables. Detailed instructions [here](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#connecting)
```python
engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)
```

## Models
1) ONT: Table for ONTs info
2) SUBSCRIPTION: Table for Service subscriptions
3) RADCHECK: Table for radius radcheck
4) RADUSERGROUP: Table for radius user group
5) RADACCT: Radius accounting table. Available only for postgres


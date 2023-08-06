This library provides a simple interface for auditing of user actions in Flask-based web applications. 

### Example

To setup auditing, simply import the package and run the setup method with the appropriate arguments. As an example, let's consider a postgres database. First, spin up the database via docker

    docker run --name my-postgres -p 5432:5432 -d postgres

Next, setup the connection to the database,

    import auditing

    args_to_postgres = dict(database="mydb", user="postgres", host="127.0.0.1")
    auditing.setup("postgres_auto", args=args_to_postgres)

The special "postgres_auto" driver creates databases and tables dynamically. Furthermore, it extends tables when new data entries are added to the audit call. If this behaviour is not desired, simply use the "postgres" driver instead. Subsequently, auditing can be performed as

    from auditing import audit
    
    audit("mytag", a="some data", c="some other data", b=0, username="me")

where "mytag" identifies the audit collection (in postgres sql it will map to the table name) while the following keyword arguments denotes the data. The current datetime is always appended unless overwritten via the "dt" argument. Querying the database

    docker exec -it my-postgres bash
    psql -U postgres
    \c mydb
    select * from mytag;
    
now yields

     username |          datetime          |     a     |        c        | b 
    ----------+----------------------------+-----------+-----------------+---
     me       | 2019-12-05 13:55:55.636742 | some data | some other data | 0

If the username is not provided, an attempt is made to extract it from the session context. If the user cannot be identified, the audit is cancelled. If the audit is made within a request context, the following data is appended

* path, host, ip (from "X-Forwarded-For" header)

[*] In addition to postgres, elastic search is supported. Other databases can also be used, simply inject a driver via the "inject_driver" method. 

#### Deployment

Bump the version number in setup.py and run

    python3 setup.py sdist
    pip3 install twine
    twine upload dist/*

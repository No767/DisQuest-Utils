<div align=center>


# DisQuest-Utils

![PyPI](https://img.shields.io/pypi/v/disquest-utils?label=PyPi&logo=pypi&logoColor=white) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/disquest-utils?label=Python&logo=python&logoColor=white)
![PyPI - License](https://img.shields.io/pypi/l/disquest-utils?label=License&logo=github&logoColor=white)

A set of async utils for DisQuest

<div align=left>

# Info

DisQuest is an base system for storing and giving users on Discord xp. This is just the base set of coroutines needed in order to use DisQuest. DisQuest uses PostgreSQL. Alternatively, if you plan on passing in your own URI (which probably u would have to), DisQuest technically also supports MySQL/MariaDB. For MySQL/MariaDB, use `asyncmy` instead of `asyncpg`

# Installing


With Asyncpg (default):

```sh
pip install disquest-utils
```
With Asyncmy:

```sh
pip install disquest-utils[asyncmy]
```

# URI Connections

DisQuest-Utils accepts URI connections in order to connection to the database. It is recommended to have python-dotenv installed, and then add the credentials as needed. The example below are only for examples, and adjust them as needed

Asyncpg:

```python
CONNECTION_URI = "postgresql+asyncpg://user:password@host:port/dbname[?key=value&key=value...]"
```

Asyncmy:

```python
CONNECTION_URI = "mysql+asyncmy://user:password@host:port/dbname[?key=value&key=value...]"
```

Now pass the variable `CONNECTION_URI` as the uri arg of any method, and you should be ready to go
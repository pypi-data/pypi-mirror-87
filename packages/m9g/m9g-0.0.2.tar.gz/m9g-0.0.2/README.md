![Build Status](https://github.com/radiocutfm/m9g/workflows/Run%20tests/badge.svg)

## m9g : Define models for communication between components, handling MarshallinG (m9g)

### Usage


```python
import m9g
class Book(m9g.Model):
    id = m9g.IntField(pk=True)
    author = m9g.StringField()

book = Book(id=1, author="Hemingway")
book.serialize()  # JSON as default
'{"id": 1, "author": "Hemingway"}'
```


#### Complex types

```python
import datetime

class Author(m9g.Model):
    id = m9g.IntField(pk=True)
    authored_books = m9g.ListField(
            m9g.StringField()
    )
    birth_date = m9g.DateField()

author = Author(
    id=1,
    authored_books=[
            "The Torrents of Spring",
            "The Sun Also Raises",
            "A Farewell To Arms"
    ],
    birth_date = datetime.date(
            year=1899,
            month=7,
            day=21
    )
)
author.serialize()
'{"id": 1, "authored_books": ["The Torrents of Spring", "The Sun Also Raises", "A Farewell To Arms"], "birth_date": "1899-07-21"}'

```


## Contributing

### Run tests for python 2.7 / 3.6

```shell
    tox
```

### Run one-off test

```shell
    tox -- tests/<test_file>.py::<test_name>
```

# ajsonapi: asynchronous JSON API

![coverage](https://gitlab.com/rvdg/ajsonapi/badges/master/coverage.svg?job=coverage)

## What is it?

*ajsonapi* is a Python package for creating a [JSON API][json-api] web server
backed by a database from a user-provided object model.


## How to specify an object model?

Let's look at a simple object model specification.

```python
# model.py

from ajsonapi import (JSON_API,
                      OneToManyRelationship,
                      ManyToOneRelationship,
                      Attribute,
                      String)

class Persons(JSON_API):
    name = Attribute(String)
    articles = OneToManyRelationship('Articles', rfkey='person_id')

class Articles(JSON_API):
    title = Attribute(String)
    author = ManyToOneRelationship('Persons', lfkey='person_id')
```

This model contains two class definitions: `Persons` and `Articles`. A person
has a name and can author zero of more articles. An article has a title and
has exactly one author (who is a person). The only parts in the model that may
be unobvious are the `lfkey` and `rfkey` parameters in the relationship
definitions. They are abbreviations for *local foreign key* and *remote
foreign key*, respectively. Ajsonapi uses these parameters to identify that
`Persons.articles` and `Articles.author` are each other's reverse relationship
and to persist objects and their relationships in the database.

For a more elaborate (albeit abstract) object model see [ajsonapi's model for
functional testing][functest-model].


## How to create a web server?

```python
# app.py

from aiohttp.web import run_app
from ajsonapi import Application

import model  # Or directly include the above code snippet

async def make_app():
    app = Application()
    await app.connect_database('postgresql://user:password@localhost:5432/db')
    await app.create_tables()
    app.add_json_api_routes()
    return app.app

run_app(make_app())
```

## What does ajsonapi provide?

From the above six line model, ajsonapi creates a web server that supports the
following eighteen operations (combinations of HTTP method and URI) as
described by the [JSON API specification][json-api-spec].

```
GET, POST                 /persons
GET, PATCH, DELETE        /persons/{id}
GET, POST, PATCH, DELETE  /persons/{id}/relationships/articles
GET                       /persons/{id}/articles
GET, POST                 /articles
GET, PATCH, DELETE        /articles/{id}
GET, PATCH                /articles/{id}/relationships/author
GET                       /articles/{id}/author
```

All `GET` operations that return a collection support the `?include`, `?fields`,
`?filter`, `?sort`, and `?page` query parameters.  All objects created and
manipulated through the web server are persisted in a Postgres database by ajsonapi.


## Where to get it?

```sh
pip install ajsonapi
```



[json-api]: https://jsonapi.org
[json-api-spec]: https://jsonapi.org/format
[functest-model]: https://gitlab.com/rvdg/ajsonapi/blob/master/ajsonapi/functests/model.py

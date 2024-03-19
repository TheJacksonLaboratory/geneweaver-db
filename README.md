# Geneweaver DB

[![Tests](https://github.com/TheJacksonLaboratory/geneweaver-db/actions/workflows/tests.yml/badge.svg?event=push)](https://github.com/TheJacksonLaboratory/geneweaver-db/actions/workflows/tests.yml)
[![Style](https://github.com/TheJacksonLaboratory/geneweaver-db/actions/workflows/style.yml/badge.svg?event=push)](https://github.com/TheJacksonLaboratory/geneweaver-db/actions/workflows/style.yml)
[![Coverage](https://github.com/TheJacksonLaboratory/geneweaver-db/actions/workflows/coverage.yml/badge.svg?event=push)](https://github.com/TheJacksonLaboratory/geneweaver-db/actions/workflows/coverage.yml)

The Geneweaver DB library provides database access functionality for the Geneweaver 
project. The library contains SQL queries wrapped in standard python functions, as well
as a database connection manager.


## Installation

To install the Geneweaver DB library, run one of the following commands:

#### Using Pip
```
pip install geneweaver-db
```

#### Using Poetry
```
poetry add geneweaver-db
```

## Usage
The Geneweaver DB library is intended to be used as a dependency for other Geneweaver
packages, but can also be used as a stand-alone pacakge.

The package has three main sections:
- `geneweaver.db` - contains non-async database functions.
- `geneweaver.db.aio` - contains async database functions.
- `geneweaver.db.query` - contains SQL queries and SQL generation functions.

Database functions _usually_ take a `Cursor` or `AsyncCursor` object as their first
argument.

### Non-Async Functions
```python
import psycopg
import geneweaver
from geneweaver.db.core.settings import settings

def get_my_gene():
    with psycopg.connect(settings.URI) as conn:
            with conn.cursor() as cur:
                result = geneweaver.db.gene.get(cur, 'my_gene')
    return result
```

### Async Functions
```python
import psycopg
import geneweaver
from geneweaver.db.core.settings import settings

async def get_my_gene():
    async with psycopg.AsyncConnection.connect(settings.URI) as conn:
            async with conn.cursor() as cur:
                result = await geneweaver.db.aio.gene.get(cur, 'my_gene')
    return result
```
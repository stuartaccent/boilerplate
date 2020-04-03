# Starlette Boilerplate Project

[![Sourcery](https://img.shields.io/badge/Sourcery-refactored-blueviolet.svg)](https://sourcery.ai)

## Getting Started

Build the container:

```bash
docker-compose build
```

Up the container:

```bash
docker-compose up
```

## Migrations

Setup your database by creating your first revision, you may need to add some missing imports:

```bash
docker-compose exec app sh
alembic revision --autogenerate -m "first revision"
```

Then apply it:

```bash
docker-compose exec app sh
alembic upgrade head
```

## Create Tables Without Migrations

```python
from app.db import metadata
from app.settings import DATABASE_URL
from sqlalchemy import create_engine
engine = create_engine(str(DATABASE_URL))
metadata.drop_all(engine)
metadata.create_all(engine)
```

## Ready!!

The container is ready at http://localhost

## Environment Variables

### base
- ALLOWED_HOSTS
- DATABASE_URL
- DEBUG
- SECRET_KEY

### email
- EMAIL_HOST
- EMAIL_PORT
- EMAIL_DEFAULT_FROM_ADDRESS
- EMAIL_DEFAULT_FROM_NAME
- EMAIL_USERNAME
- EMAIL_PASSWORD

### aws
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_BUCKET
- AWS_REGION

### other
- SENTRY_DSN

## Formatting and Linting

Sorts imports, removes unused variables, max line length etc

```bash
docker-compose exec app ./scripts/lint
```

## Testing

Run tests and coverage

```bash
docker-compose exec app ./scripts/test
```

## New User & Example Scope

```bash
docker-compose exec app python
```

The following will just paste into the python shell to
save you copying each line.

```python
from app.db import metadata
from app.settings import DATABASE_URL
from sqlalchemy import create_engine
from starlette_auth.tables import scope, user, user_scope
from starlette_auth.utils.crypto import hash_password
engine = create_engine(str(DATABASE_URL))
ent1 = engine.execute(
    user.insert().values(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        password=hash_password("password")
    )
)
ent2 = engine.execute(
    scope.insert().values(
        code="admin",
        description="Full administrators access"
    )
)
engine.execute(
    user_scope.insert().values(
        user_id=ent1.inserted_primary_key[0],
        scope_id=ent2.inserted_primary_key[0]
    )
)
```

## Styles

npm install:

```bash
npm install
```

build css:

```bash
npm run watch-css
```

## Postgres Query Stats

The following line must be added the the `postgresql.conf` file:

```bash
shared_preload_libraries = 'pg_stat_statements'
```

Enable the extension in postgres:

```sql
CREATE EXTENSION pg_stat_statements;
```

Reset stats:

```sql
SELECT pg_stat_statements_reset();
```

View all logged stats:

```sql
SELECT
query,
calls,
total_time,
min_time,
max_time,
mean_time,
rows,
100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
INNER JOIN pg_catalog.pg_database db
ON pg_stat_statements.dbid = db.oid
WHERE db.datname = 'appdb'
ORDER BY total_time
DESC LIMIT 25;
```

More info: https://www.postgresql.org/docs/current/pgstatstatements.html

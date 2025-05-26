## Test project for PostGis with SQLAlchemy and GeoAlchemy2

### Key libs
- geoalchemy2
- shapely

### Important Notes
As known there is a problem with postgis tables with alembic migrations
- adjust alembic migrations [env.py](https://github.com/korneyka3000/postgis_test/blob/main/src/migrations/env.py)
  - add function to prevent no diff migrations runs -> [function](https://github.com/korneyka3000/postgis_test/blob/main/src/migrations/env.py#L31-L34)
    - add this function into `context.configure` args [link](https://github.com/korneyka3000/postgis_test/blob/main/src/migrations/env.py#L66)
  - add lines like suggest `geoalchemy` [docs](https://geoalchemy-2.readthedocs.io/en/stable/alembic.html#helpers)
    - `alembic_helpers.include_object` <sub>(ignores the internal tables managed by the spatial extensions (note that in some cases this function might need some customization, see the details in the doc of this function).)</sub>
    - `alembic_helpers.writer` <sub>(adds specific spatial operations to Alembic)</sub>
  - adjust [script.py.mako](https://github.com/korneyka3000/postgis_test/blob/main/src/migrations/script.py.mako)

# How to run

### Create env(adjust if needed)
```shell
  cp .env.template .env
```

### To start db and app
```shell
  docker compose up --build -d
```

### To load dump data
```shell
  docker compose exec app uv run cli load
```
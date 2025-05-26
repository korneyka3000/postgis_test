__all__ = ("load_dumps",)

import logging

from pathlib import Path

import click
import polars as pl

from roga_and_kopyta.config import settings


load_order = (
    "activity",
    "building",
    "organization",
    "phone_number",
    "organization_activity",
)
logger = logging.getLogger(__file__)


def _get_root_path() -> Path:
    return Path(__file__).parent.parent.parent.parent


def _get_db_url() -> str:
    scheme = settings.DB_URL.scheme
    if scheme != "postgresql":
        sync_url = settings.DB_URL.unicode_string().replace(scheme, "postgresql")
    else:
        sync_url = settings.DB_URL.unicode_string()
    return sync_url


def _read_csv(path: Path) -> dict[str, pl.DataFrame]:
    df_dict: dict[str, pl.DataFrame] = {}
    for file in path.glob("*.csv"):
        name = file.name.split(".", 1)[0]
        if name in load_order:
            df_dict[name] = pl.read_csv(file)
        else:
            click.secho(f"File for unknown table: {file.name!r}", fg="red")
    return df_dict


def _add_from_df(name: str, df: pl.DataFrame, db_url: str) -> None:
    df.write_database(name, db_url, if_table_exists="append")


def load_dumps() -> None:
    path = _get_root_path() / "db_dumps"
    df_dict = _read_csv(path)
    db_url = _get_db_url()
    for name in load_order:
        result = pl.read_database_uri(
            query=f"SELECT count(*) FROM {name}",  # noqa: S608
            uri=db_url,
        )
        if not result["count"].sum():
            _add_from_df(name=name, df=df_dict[name], db_url=db_url)
        else:
            click.secho(
                message=f"The table {name!r} is not empty, skipping.",
                fg="red",
            )

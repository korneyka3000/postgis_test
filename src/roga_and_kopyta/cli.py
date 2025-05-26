from logging import INFO

import click
import uvicorn

from alembic.command import upgrade

from roga_and_kopyta.config.config import alembic_config
from roga_and_kopyta.management import load_dumps


@click.group()
def cli() -> None:
    pass


@cli.command(help="run server")
@click.option("--port", default=8000, help="port to run app")
@click.option("--reload", is_flag=True, default=False)
@click.option("--workers", default=1, help="number of workers")
def run(port: int, reload: bool, workers: int) -> None:
    if workers > 1 and reload:
        raise ValueError("reload and workers cannot be used together")
    uvicorn.run(
        "roga_and_kopyta.app:app",
        host="0.0.0.0",
        port=port,
        reload=reload,
        workers=workers,
        access_log=False,
        log_level=INFO,
    )


@cli.command(name="upgrade", help="alembic upgrade head to revision")
@click.argument("revision_id", default="head")
def upgrade_head(revision_id: str = "head") -> None:
    upgrade(config=alembic_config, revision=revision_id)


@cli.command(name="load", help="Load data to db from csv files")
def load() -> None:
    load_dumps()


@cli.command(name="echo", help="Echo command")
@click.argument("message")
def echo(message: str) -> None:
    click.secho(message, fg="cyan")


if __name__ == "__main__":
    cli()

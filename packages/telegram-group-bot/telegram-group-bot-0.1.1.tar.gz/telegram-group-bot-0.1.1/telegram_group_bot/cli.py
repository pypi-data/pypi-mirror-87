import click

from . import __version__
from .bot import Bot
from .config import Config


@click.command(help="Bot for telegram groups")
@click.version_option(__version__, help="Show the version and exit")
@click.help_option(help="Show this message and exit")
@click.argument("config_path", type=click.Path(exists=True))
def cli(config_path: str):
    config = Config.from_toml_file(config_path)
    bot = Bot(config)
    bot.start()

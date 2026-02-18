import logging
import click
from .checker import check_urls

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-8s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


logger = logging.getLogger(__name__)


@click.command()
@click.argument("urls", nargs=-1)
@click.option(
    "--timeout",
    default=5,
    help="timeout in seconds for each request.",
)
@click.option(
    "--verbose", "-v", is_flag=True, help="Enable debug logging"
)
def main(urls, timeout, verbose):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("verbose logging enabled")
    logger.debug(f"received urls: {urls}")
    logger.debug(f"received timeout: {timeout}")
    logger.debug(f"received verbose: {verbose}")
    if not urls:
        logger.warning("no urls provided to check.")
        click.echo("Usage: check-urls <url1><url2> ...")
    logger.info(f"starting check for {len(urls)} urls .")

    results = check_urls(list(urls), timeout)

    click.echo("\n--- Results ---")
    for url, status in results.items():
        if "ok" in status:
            fg_color = "green"
        else:
            fg_color = "red"
        click.secho(f"{url:<40} -> {status}", fg=fg_color)

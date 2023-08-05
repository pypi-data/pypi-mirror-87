import click

import logging
import klogs


@click.group()
@click.option("--log-line-no", default=False)
@click.option("--log-level", type=str, default=logging.INFO)
@click.option("--log-file", type=str, default=None)
def main(log_line_no, log_level, log_file):
    klogs.configure_logging(
        level=log_level,
        with_line_no=log_line_no,
        log_file=log_file,
    )


@main.command()
def demo():
    logging.getLogger().info("Info level")
    logging.getLogger().debug("Debug level outside context manager")
    with klogs.push_log_level(logging.DEBUG):
        logging.getLogger().debug("Debug level inside context manager")


if __name__ == "__main__":
    main()

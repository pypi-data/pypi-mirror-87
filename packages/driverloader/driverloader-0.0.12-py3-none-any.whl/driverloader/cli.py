import click
from driverloader import chrome_driver, firefox_driver
from driverloader.driver import DEFAULT_FIREFOX_VERSION, DEFAULT_CHROME_VERSION


def download_driver(name: str, path=None, version=None, force=False):
    if name.lower() == 'chrome':
        version = version or DEFAULT_CHROME_VERSION
        return chrome_driver(path=path, version=version, force=force)
    elif name.lower() == 'firefox':
        version = version or DEFAULT_FIREFOX_VERSION
        return firefox_driver(path=path, version=version, force=force)
    raise ValueError("name must be chrome or firefox")


@click.command()
@click.argument('driver_name', type=click.Choice(['chrome', 'firefox']))
@click.argument('path', type=click.Path(exists=True))
@click.option('-v', '--version')
@click.option('-f', '--force')
def cli(driver_name, path, version, force):
    """Webdriver downloader  of chrome and firefox.

    - driver_name: Which driver, [chrome, firefox] supported.\n
    - path: Path to save the driver.
    """
    driver = download_driver(driver_name, path=path, version=version, force=force)
    click.echo(driver)


if __name__ == '__main__':
    cli()

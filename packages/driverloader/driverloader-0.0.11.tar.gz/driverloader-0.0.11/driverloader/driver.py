import os
import logging
import re
import platform
import sys
import tempfile
import zipfile
import tarfile
import pathlib
from urllib import request
from driverloader import config

DEFAULT_HOST = 'https://npm.taobao.org'
DEFAULT_CHROME_VERSION = '71.0.3578.80'
DEFAULT_FIREFOX_VERSION = '0.27.0'

logging.basicConfig(level=logging.INFO)


class BaseDriver:
    host = DEFAULT_HOST
    pattern = r'<a href="(/mirrors/(chromedriver|geckodriver)/v?([0-9.]+)\/)">'

    def __init__(self, name, host=None):
        self.name = name
        if self.name == 'firefox':
            self.name = 'gecko'
        # self.version = str(version)
        self.host = host or DEFAULT_HOST
        self.version = ''
        self.full_version = ''
        self.url = ''
        self.index_url = self.host + '/mirrors/' + self.name + 'driver'

    @property
    def versions(self):
        r = request.urlopen(self.index_url)
        html = r.read().decode('utf8')
        regex = re.compile(self.pattern)
        for e in regex.finditer(html):
            url, version = e.group(1), e.group(3)
            yield url, version

    @property
    def _get_file(self):
        """parse filename using platform"""
        raise NotImplementedError("use child class")

    @property
    def full_version_and_url(self):
        for url, v in self.versions:
            if v.startswith(self.version):
                self.full_version = v
                self.url = self.host + url + self._get_file
                return self.full_version, self.url
        raise ValueError("no this version {}".format(self.version))

    def __call__(self, version, path=None, force=False):
        save_dir_str = path if path else config.DRIVER_PATH
        save_dir = pathlib.Path(save_dir_str).resolve()
        self.version = str(version)

        if not force:
            gen = save_dir.iterdir()
            for f in gen:
                if self.version in f.name:
                    return str(f)
        self.full_version_and_url
        driver_data = self.download()
        return self.save(driver_data, save_dir)

    def download(self):
        """Download web driver from URL"""
        logging.info("Downloading chrome webdriver. Please wait...")
        r = request.urlopen(self.url)
        logging.info("Downloading chrome webdriver finished")
        return r

    def save(self, response, path):
        """Save the data of download.
        """
        f = tempfile.NamedTemporaryFile(dir=path, delete=False)
        f.write(response.read())
        if zipfile.is_zipfile(f.name):
            zip_file = zipfile.ZipFile(f)
            filelist = zip_file.filelist
            for file in filelist:
                download_file = zip_file.extract(file.filename, path)
                download_file = pathlib.Path(download_file)
        elif tarfile.is_tarfile(f.name):
            zip_file = tarfile.open(f.name)
            filelist = zip_file.getmembers()
            for file in filelist:
                zip_file.extract(file.name, path)
                download_file = pathlib.Path(path) / file.name
        else:
            raise ValueError("not zip or tar format")

        f.close()
        pathlib.Path(f.name).unlink()

        new_name = download_file.stem + self.full_version + download_file.suffix
        new_target = path / new_name
        try:
            download_file.rename(new_target)
            return str(new_target)
        except FileExistsError:
            download_file.unlink()
            return str(new_target)



class ChromeDriver(BaseDriver):
    def __init__(self, host=None):
        super().__init__('chrome', host)

    def __call__(self, path=None,
                 version=DEFAULT_CHROME_VERSION,
                 force=False):
        return super().__call__(path=path,
                                version=version,
                                force=force)

    @property
    def default(self):
        return self.__call__(path=None,
                             version=DEFAULT_CHROME_VERSION,
                             force=False)

    @property
    def _get_file(self):
        """parse filename using platform"""
        platform = sys.platform
        platforms = {
            "win32": "win32",
            "win64": "win64",
            "linux": "linux64",
            "darwin": "mac64",
        }
        return 'chromedriver_{}.zip'.format(platforms.get(platform, ''))


class FirefoxDriver(BaseDriver):
    def __init__(self, host=None):
        super().__init__('firefox', host=host)

    def __call__(self, path=None,
                 version=DEFAULT_FIREFOX_VERSION, force=False):
        return super().__call__(path=path,
                                version=version,
                                force=force)

    @property
    def default(self):
        return self.__call__(path=None, version=DEFAULT_FIREFOX_VERSION, force=False)

    @property
    def _get_file(self):
        """parse filename using platform"""
        system = sys.platform
        if system.startswith('win'):
            system = system[:3]
        file_map = {
            "linux32": f"geckodriver-v{self.full_version}-linux32.tar.gz",
            "linux64": f"geckodriver-v{self.full_version}-linux64.tar.gz",
            "darwin32": f"geckodriver-v{self.full_version}-macos.tar.gz",
            "darwin64": f"geckodriver-v{self.full_version}-macos.tar.gz",
            "win32": f"geckodriver-v{self.full_version}-win32.zip",
            "win64": f"geckodriver-v{self.full_version}-win64.zip",
        }
        bit = platform.architecture()[0][:2]
        file = file_map.get(system + bit, '')
        return file

## Quick start:

Download chrome driver:
```python
from driverloader import chrome_driver
print(chrome_driver.default)
```

Download firefox driver:
```python
from driverloader import firefox_driver
print(firefox_driver.default)
```

The drivers would be downloaded in **executor/** dir of the webdrivers package.
You can find chromedriver.exe or geckodriver.exe in the dir.


Using with selenium:
```python
from selenium.webdriver import Chrome
from driverloader import chrome_driver

browser = Chrome(chrome_driver.default)
browser.quit()
```

Downloading to customized path:
```python
from driverloader import chrome_driver
driver_path = chrome_driver(path='.')
```

or absolute path:
```python
import pathlib
from driverloader import chrome_driver

current_dir = pathlib.Path(__file__).parent.parent
print(chrome_driver(current_dir))
```

customized version:
```python
from driverloader import chrome_driver
driver_path = chrome_driver(path='.', version='70')
```


## command line
Using driverloader by command line like this:
```bash
driverloader chrome .
driverloader firefox .
```
Two arguments:
- driver_name, chrome and firefox supported.
- path,  the path you want to save the driver.

Options:
- `-v` or `--version`,  the version would be downloaded.
- `-f` or `--force`, force downloading if the similar driver exists

## System Platform
Driverloader would download the given version according to your OS,
windows, mac, linux are all OK.


## Mirror URL
webdriver-downloader get the drivers from https://npm.taobao.org/mirrors/
- chrome driver: https://npm.taobao.org/mirrors/chromedriver/
- firefox driver: https://npm.taobao.org/mirrors/geckodriver/
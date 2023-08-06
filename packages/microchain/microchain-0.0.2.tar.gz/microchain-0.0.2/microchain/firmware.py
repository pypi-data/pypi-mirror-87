import requests
import logging

log = logging.getLogger(__name__)

def download(filename='/tmp/microchain-firmware.bin'):
    # TODO: scrap the micropython download page and list firmware sorted by version
    url = 'https://micropython.org/resources/firmware/esp32-idf3-20200902-v1.13.bin'
    r = requests.get(url)
    log.info(f'Downloading firmware from {url}')
    with open(filename, 'wb') as f:
        f.write(r.content)

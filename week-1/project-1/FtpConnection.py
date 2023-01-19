import os
from ftplib import FTP  # importing library to connect to the server

from dotenv import load_dotenv  # importing method to load config data
from configparser import ConfigParser  # importing file to read configurating params

load_dotenv()  # loading config data
try:  # trying to load settings from config.ini
    local_settings = ConfigParser()
    local_settings.read("config.ini")
    path_to_download = local_settings['local-path']['local-path']
except KeyError:
    path_to_download = './'

host = os.environ["host"]
user = os.environ["user"]
psw = os.environ["psw"]


def download_data_from_ftp_server(host: str, usr: str, psw: str, download_path: str):
    if not os.path.exists(download_path):
        raise FileNotFoundError('Local directory for downloading was not find')

    with FTP(host) as ftp:
        ftp.login(user=usr, passwd=psw)
        files = ftp.nlst()
        for file in files:
            with open(f'{path_to_download}{"/" if path_to_download[-1] != "/" else ""}{file}', 'wb') as fp:
                ftp.retrbinary(f'RETR {file}', fp.write)


if __name__ == '__main__':
    download_data_from_ftp_server(host=host, usr=user, psw=psw, download_path=path_to_download)
    print(3)

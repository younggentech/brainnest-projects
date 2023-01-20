import os
import shutil
import time
from ftplib import FTP  # importing library to connect to the server

from dotenv import load_dotenv  # importing method to load config data
from configparser import ConfigParser  # importing file to read configurating params
from schedule import repeat, every, run_pending

load_dotenv()  # loading config data
try:  # trying to load settings from config.ini
    local_settings = ConfigParser()
    local_settings.read("config.ini")
    path_to_download = local_settings['local-path']['local-path']
    path_to_move = local_settings['local-path']['moving-path']
except KeyError:
    path_to_download = './'
    path_to_move = "./moving-folder/"

host = os.environ["host"]
user = os.environ["user"]
psw = os.environ["psw"]


@repeat(every(10).seconds, host=host, usr=user, psw=psw,
        download_path=path_to_download)  # this decorator will run the next method every specified time
def download_data_from_ftp_server(host: str, usr: str, psw: str, download_path: str):
    if not os.path.exists(download_path):
        os.mkdir(download_path)
        # raise FileNotFoundError('Local directory for downloading was not find')

    with FTP(host) as ftp:
        ftp.login(user=usr, passwd=psw)
        files = ftp.nlst()
        for file in files:
            with open(f'{path_to_download}{"/" if path_to_download[-1] != "/" else ""}{file}', 'wb') as fp:
                ftp.retrbinary(f'RETR {file}', fp.write)


@repeat(every(10).seconds, src=path_to_download,
        dist=path_to_move)  # this decorator will run the next method every specified time
def move_downloaded(src: str, dist: str) -> None:
    """a wrapper method to use `shutil.move()` method
    to move files/folders from source to destination
    :param src: the source path to move file/folders from.
    :param dist: the destination path to move file/folders to.
    :return: None
    """
    if not src or not dist:
        raise ValueError("You must specify both source and destination folders.")

    if not os.path.exists(src):
        raise FileNotFoundError("The source file/folder doesn't exists, make sure you entered the correct path.")

    try:
        shutil.move(src=src, dst=dist)
    except shutil.Error as e:
        print(e)


if __name__ == '__main__':
    while 1:
        run_pending()
        time.sleep(1)
    # print(3)

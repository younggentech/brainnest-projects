import ftplib
import os
import shutil
import time
import logging
from ftplib import FTP  # importing library to connect to the server
from schedule import repeat, every, run_pending

from dotenv import load_dotenv  # importing method to load config data
from configparser import ConfigParser  # importing file to read configurating params

load_dotenv()  # loading config data
try:  # trying to load settings from config.ini
    local_settings = ConfigParser()
    local_settings.read("config.ini")
    path_to_download = local_settings['local-path']['local-path']
    path_to_move = local_settings['local-path']['moving-path']
    scheduled_time = local_settings['local-path']['run-time']
except KeyError:
    path_to_download = './'
    path_to_move = "./moving-folder/"
    scheduled_time = "9:00"

host = os.environ["host"]
user = os.environ["user"]
psw = os.environ["psw"]


# @repeat(every(10).seconds, host=host, usr=user, psw=psw,
#         download_path=path_to_download)  # this decorator will run the next method every specified time
def download_data_from_ftp_server(host: str, usr: str, psw: str, download_path: str) -> None:
    """
    Downloads file from specified ftp server
    :param host:
    :param usr:
    :param psw:
    :param download_path:
    :return:
    """
    if not host or not usr or not psw or not download_path:
        raise ValueError('Plese provide all params')
    if not os.path.exists(download_path):
        os.mkdir(download_path)
        # raise FileNotFoundError('Local directory for downloading was not find')

    with FTP(host) as ftp:
        try:
            ftp.login(user=usr, passwd=psw)
        except ftplib.error_perm:
            raise ValueError("Incorrect login or password")
        files = ftp.nlst()
        for file in files:
            with open(f'{path_to_download}{"/" if path_to_download[-1] != "/" else ""}{file}', 'wb') as fp:
                ftp.retrbinary(f'RETR {file}', fp.write)


# @repeat(every(10).seconds, src=path_to_download,
#         dist=path_to_move)  # this decorator will run the next method every specified time
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
        if not os.path.exists(dist):
            os.mkdir(dist)
        shutil.copytree(src=src, dst=dist, dirs_exist_ok=True)  # method copies data from source path to dest,
        # overriding existing files
    except shutil.Error as e:
        print(e)


def work(host: str, usr: str, psw: str, download_path: str, dist: str) -> None:
    print('starting')
    if not host or not usr or not psw or not download_path or not download_path or not dist:
        raise ValueError('Plese provide all params')
    download_data_from_ftp_server(host, usr, psw, download_path)
    move_downloaded(download_path, dist)
    print('done')


def main():
    every().day.at(scheduled_time).do(work, host, user, psw, path_to_download, path_to_move)
    while 1:
        run_pending()
        time.sleep(1)


if __name__ == '__main__':
    # TODO: SET UP LOGGING
    main()

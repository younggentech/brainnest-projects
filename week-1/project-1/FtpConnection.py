import datetime
import os
import shutil
import time
import logging
from ftplib import FTP, error_perm  # importing library to connect to the server
from schedule import every, run_pending

from dotenv import load_dotenv  # importing method to load config data
from configparser import ConfigParser  # importing file to read configurating params

load_dotenv()  # loading config data
try:  # trying to load settings from config.ini
    local_settings = ConfigParser()
    local_settings.read("config.ini")
    path_to_download = local_settings['local-path']['local-path']
    path_to_move = local_settings['local-path']['moving-path']
    scheduled_time = local_settings['local-path']['run-time'] # o start execution current_time < scheduled_time
except KeyError:   # if the file wasn't found we put default settings
    path_to_download = './'
    path_to_move = "./moving-folder/"
    scheduled_time = "9:00"  # to start execution current_time < scheduled_time

# loading config data from .env file to connect to ftp server.
# we assume that the server is secured and has authentification
host = os.environ["host"]
user = os.environ["user"]
psw = os.environ["psw"]


# specify config for logging, logs go to the terminal and to the file with the name DATE_OF_RUNNING_THE_SCRTIPT.log
# for example 20.01.2023.log
logging.basicConfig(format='%(asctime)s-%(levelname)s - %(message)s',
                    level=logging.INFO,
                    datefmt='%d.%m.%Y %H:%M:%S',
                    handlers=[
                        logging.FileHandler(filename=f'{datetime.datetime.now().date().strftime("%d.%m.%Y")}.log'),
                        logging.StreamHandler()
                    ])


def download_data_from_ftp_server(host: str, usr: str, psw: str, download_path: str) -> None:
    """
    Downloads file from specified ftp server
    :param host:
    :param usr:
    :param psw:
    :param download_path:
    :return:
    """
    if not host or not download_path:  # raise ValueError if not enought params
        raise ValueError('Plese provide all params')
    if not os.path.exists(download_path):  # if local path for download wasn't found, we create a folder
        os.mkdir(download_path)

    with FTP(host) as ftp:  # oppening connection to ftp server using context manager with
        try:  # try to login to server
            ftp.login(user=usr, passwd=psw)
            logging.info(f'succesful login host {usr}@{host}')
        except error_perm:  # raise an error if credentials are incorrect
            logging.error(f'Incorrect login or password')
            raise ValueError("Incorrect login or password")
        files = ftp.nlst()  # get names of files in current directory of ftp server
        logging.info(f'downloaded from {host} files: {files}')
        for file in files:  # downloading files to the specified location
            with open(f'{path_to_download}{"/" if path_to_download[-1] != "/" else ""}{file}', 'wb') as fp:
                ftp.retrbinary(f'RETR {file}', fp.write)
        logging.info(f'downloading from {host} finished')


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
        logging.info(f'starting transfering from {src} to {dist}')
        if not os.path.exists(dist):  # creating a destination directory if the one does not exist
            os.mkdir(dist)
        shutil.copytree(src=src, dst=dist, dirs_exist_ok=True)  # method copies data from source path to dest,
        # overriding existing files
        logging.info(f'transfer finished')
    except shutil.Error as e:
        logging.error(f'shutil.Error {e}', stack_info=True)


def work(host: str, usr: str, psw: str, download_path: str, dist: str) -> None:
    """
    Function to put all actions in one place.
    Firstly downloads data from FTP and then moves it to destination path
    """
    logging.info('starting working process')
    if not host or not download_path or not download_path or not dist:
        raise ValueError('Plese provide all params')
    try:
        download_data_from_ftp_server(host, usr, psw, download_path)
    except Exception as e:
        logging.error(e, stack_info=True)
        exit()
    try:
        move_downloaded(download_path, dist)
    except Exception as e:
        logging.error(e, stack_info=True)
        exit()
    logging.info('finished working proccess')


def main():
    """Main function. Specifies and runs the scheduler"""
    logging.info('start main')
    every().day.at(scheduled_time).do(work, host, user, psw, path_to_download, path_to_move)
    while 1:
        run_pending()
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()  # call the main function and start execution process
    except KeyboardInterrupt:
        logging.info('program finished by user')

#!/usr/bin/python3
from myauthenticationdata import authenticate_open, path
import urllib.request
import re
import bz2
import pandas as pd


def openfiles(url=path):
    """
    Open a dir or file in https
    :rtype : List of files in the directory
    """
    # print "open %s" % url
    if "https" in url:
        req = authenticate_open(url)
    else:
        req = urllib.request.urlopen(url)
    return req.read()


def get_dir_files(dir_list):
    """
    get all the .csv files from a named directory
    :param dir_list: directory to search for csv files in
    :return: array of file names from the directory that are .csv files
    """
    pattern = re.compile('<a href=.*csv.*>(.*csv.*?)</a')
    file_list = pattern.findall(dir_list)
    return file_list


def open_decrypted_file(url):
    """
    open a decrypted file, return a handle to the file
    :param url:
    :return: handle to the decrypted file
    """
    # decompress the file
    input_file = bz2.BZ2File(url, 'rb')
    return input_file


def open_csv(url):
    """
    open a csv file.
    :rtype : csv.reader object
    """
    input_file = open_decrypted_file(url)
    iter_csv = pd.read_csv(input_file, sep="^", iterator=True, chunksize=100000, parse_dates=True)
    # open the csv file and read it
    return iter_csv


def download_it(url):
    """
    download the file locally so we can decrypt it.
    :rtype : None
    """
    full_path = path + url
    urllib.request.urlretrieve(full_path, filename=url)
    print("Downloaded file %s to %s" % (full_path, url))
    return
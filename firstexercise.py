#!/usr/bin/python3
"""
First exercise
Count the number of lines in Python for each file.
"""
from openfiles import open_csv, download_it, openfiles, get_dir_files


def sum_it(url):
    """
    Count the number of lines in a python file.
    :rtype : None
    """
    count = 0
    # open the csv file and read it
    for chunk in open_csv(url):
        count += len(chunk.index)
    print("The %s file contains %d lines" % (url, count))
    return


def main():
    # open the dir and get the files
    # authenticate_setup()
    dir_list = openfiles().decode('utf-8')
    if dir_list:
        file_list = get_dir_files(dir_list)

        # for each file in the file list, count the lines
        for csv_filename in file_list:
            print("processing %s" % csv_filename)
            download_it(csv_filename)
            sum_it(csv_filename)
    return


if __name__ == "__main__":
    main()

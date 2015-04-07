#!/usr/bin/python3
"""
Second exercise
Print the top 10 arrival airports in 2013 in the standard output, including the number of passengers
(using the bookings file)
Arrival airport is the column arr_port. It is the IATA code for the airport.
To get the total number of passengers for an airport, you can sum the column pax, grouping by
arr_port. Note that there is negative pax. That corresponds to cancellations. So to get the total
number of passengers that have actually booked, you should sum including the negatives (that will
remove the canceled bookings).
Bonus point: Solve this problem using pandas (http://pandas.pydata.org/)
"""

from openfiles import openfiles, get_dir_files, download_it, open_decrypted_file
import pandas as pd
import operator
from pprint import pprint


def find_top_ten(url):
    """
    Find top 10 arrival airports by bookings.
    :param : bookings csv file to read
    :rtype : None
    """
    my_list = {}
    input_file = open_decrypted_file(url)

    # Read the csv file in chunks
    iter_csv = pd.read_csv(input_file, sep="^", iterator=True, chunksize=10000)
    for chunk in iter_csv:
        for row in chunk.iterrows():
            try:
                if str(row[1]["year"]) == "2013":
                    arr_port = row[1]["arr_port"].strip()
                    if arr_port in my_list:
                        my_list[arr_port] += int(row[1]["pax"])
                    else:
                        my_list[arr_port] = int(row[1]["pax"])

            except IndexError:
                pprint("Invalid Record Found, Skipping  %s" % row)

    # sort the values
    sorted_list = sorted(my_list.items(), key=operator.itemgetter(1), reverse=True)

    # Print out the top 10 airports and passenger totals
    pprint("The top ten arrival airports for 2013 were:")
    for num in sorted_list[:10]:
        pprint("    Airport: %s  had %s passengers in 2013" % (num[0], num[1]))
    return


def main():
    # open the dir and get the files
    dir_list = openfiles().decode('utf-8')

    if dir_list:
        file_list = get_dir_files(dir_list)
        # for each file in the file list, find the bookings file
        for csv_filename in file_list:
            if "bookings" in csv_filename:
                # download the bookings file to a make it faster
                print("processing %s" % csv_filename)
                download_it(csv_filename)
                find_top_ten(csv_filename)


if __name__ == "__main__":
    main()

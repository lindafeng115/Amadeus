#!/usr/bin/python
"""
Third exercise
Plot the monthly number of searches for flights arriving at Malaga, Madrid or Barcelona.
For the arriving airport, you can use the Destination column in the searches file. Plot a curve for
Malaga, another one for Madrid, and another one for Barcelona, in the same figure.
Bonus point: Solving this problem using pandas.
"""

from openfiles import openfiles, get_dir_files, download_it, open_decrypted_file
import pandas as pd
import matplotlib.pyplot as plt
import datetime


def valid(chunks):
    """
    Return a list of only destination airports in ["AGP", "MAD", "BLA"]
    :param chunks:
    :return: data frame of destination airports in ["AGP", "MAD", "BLA"]
    """
    for chunk in chunks:
        mask = chunk.query('["AGP", "MAD", "BLA"] in Destination')
        yield mask
    return


def monthly_searches(url):
    """
    read a csv file and sort the data by date and destination.  Graph the values
    :param : csv file url
    :rtype : None
    """
    input_file = open_decrypted_file(url)
    # avoiding memory errors and reading in this large csv file by chunks
    iter_csv = pd.read_csv(input_file, sep="^", iterator=True, chunksize=10000,
                           usecols=["Date", "Destination"], parse_dates=True, na_values=["Nope"])

    df = pd.concat(valid(iter_csv))
    df["Date"] = pd.to_datetime(df["Date"], format='%Y-%m-%d')
    graph_it(df)
    return


def graph_it(bigdata):
    """
    Plot a line graph for all the destination locations in bigdata, using "Destination" and "Date" columns.
    Aggregate by month
    :param bigdata:
    :return:
    """
    fig, ax = plt.subplots(sharex=True, sharey=True)
    ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

    # Add the Plot Labels
    ax.set_xlabel("Date")
    ax.set_ylabel("Searches")
    ax.set_title("Monthly Searches by Airport")
    ax.set_ylim(-5000, 30000)
    ax.set_xlim(1, 12)

    # Set the colors
    color_list = {'MAD': 'r', 'BLA': 'g', 'AGP': 'b'}

    # Group the date by month & Destination ( this is probably completely unnecessary but I don't know pandas well
    # enough)
    months = bigdata.Date.apply(lambda x: datetime.datetime.strftime(x, '%m'))
    by_months = bigdata.groupby([months, 'Destination'], as_index=False)
    monthly_series = {}

    for (idx, (grp, val)) in enumerate(by_months):
        if grp[1] not in monthly_series:
            # initialize all the months to zero for the plot
            monthly_series[grp[1]] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
        monthly_series[grp[1]][int(grp[0])] = len(val)

    for dest_airport in monthly_series:
        ax.plot(list(monthly_series[dest_airport].keys()), list(monthly_series[dest_airport].values()),
                color=color_list[dest_airport], label=dest_airport)

    # Create the Legend
    plt.legend(loc='best')
    plt.show()
    return


def main():
    # open the dir and get the files
    dir_list = openfiles().decode('utf-8')
    if dir_list:
        file_list = get_dir_files(dir_list)
        # find the "searches file and plot the data
        for csv_filename in file_list:
            if "searches" in csv_filename:
                print("processing %s" % csv_filename)
                # download the file so we can decompress it
                download_it(csv_filename)
                monthly_searches(csv_filename)
    return


if __name__ == "__main__":
    main()

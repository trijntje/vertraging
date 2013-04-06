#!/usr/bin/python3.2

import sys
import os
import datetime
import ovnl

def main():

    if len(sys.argv) != 2:
        error("Please specify a xls datafile")
        exit(-1)

    # Check if file exists
    filename=sys.argv[1]
    if not os.path.exists(filename):
        error("Cannot find file '{}', exiting..".format(filename))
        exit(-1)

    # TODO implement checking of file typ properly
    extension=sys.argv[1].split('.')[-1]
    if extension == "csv":
        # Read ov-chipkaart.nl travels file
        travels=ovnl.read_ov_travels_file(filename)
    elif extension == "xls":
        # Read the NS travels file
        travels,transactions=ovnl.read_ns_travels_file(filename)

    for transaction in transactions:
        print("{}\t{}\t{}".format(transaction.time, transaction.place, transaction.price))

    
    # PRINT THE MINIMUM TRAVEL TIMES
    #min_times=minimum_travel_times(travels)
    #for key in min_times.keys():
    #    print("Van {} naar {}\t{}".format(key[0],key[1],min_times[key]))

    # PRINT POSSIBLE DELAYS:
    delays=ovnl.possible_delays(travels)
    print("Possible delays in {} of {} trips:".format(len(delays), len(travels)))
    for trip in delays:
        print(trip)

    # PRINT THE MISSING CHECKOUTS
    #no_checkout=get_missing_checkout(travels)
    #for trip in no_checkout:
    #    print(trip)

    # PRINT THE TOTAL OF ALL INTERACTIONS
    #added,deducted=ovnl.transactions_total(travels)
    #print("Total added to card:{}".format(added))
    #print("Total deducted from card:{}".format(deducted))
    #for trip in travels:
        #if trip.transaction_type != 'Reis': 
            #print(trip.price)

if __name__ == "__main__":
    # 
    main()

#!/usr/bin/python3.2

import sys
import os
import datetime
import ovnl

separator='-'*80

def print_all_trips(travels):
    print("There are a total of {} trips:".format(len(travels)))
    for trip in travels:
        print(trip)
    print(separator)

def print_all_transactions(transactions):
    print("There are a total of {} transactions:".format(len(transactions)))
    for trans in transactions:
        print(trans)
    print(separator)

def print_all_delays(travels):
    delays=ovnl.possible_delays(travels)
    if len(delays) == 0:
        print("No delays in {} trips detected".format(len(travels)))
    else:
        print("Possible delays in {} of {} trips:".format(len(delays), len(travels)))
        for trip in delays:
            print(trip)
    print(separator)

def print_all_missed_checkouts(transactions,travels):
    no_checkout=ovnl.get_missing_checkout(transactions)
    if len(no_checkout) == 0:
        print("No missed checkouts in {} trips detected".format(len(no_checkout)))
    else:
        print("You forgot to checkout in {} of {} trips:".format(len(no_checkout), len(travels)))
        for transaction in no_checkout:
            print(transaction)
    print(separator)

def main():

    if len(sys.argv) != 2:
        ovnl.error("Please specify a xls datafile")
        exit(-1)

    # Check if file exists
    filename=sys.argv[1]
    if not os.path.exists(filename):
        ovnl.error("Cannot find file '{}', exiting..".format(filename))
        exit(-1)

    # TODO implement checking of file typ properly
    extension=sys.argv[1].split('.')[-1]
    if extension == "csv":
        # Read ov-chipkaart.nl travels file
        travels,transactions=ovnl.read_ov_travels_file(filename)
    elif extension == "xls":
        # Read the NS travels file
        travels,transactions=ovnl.read_ns_travels_file(filename)

    # This is mainly for debuggin purposes
    print_all_trips(travels)
    print_all_delays(travels)

    print_all_transactions(transactions)
    #This needs travels to say 'forgot to checkout in x out of N travels'
    print_all_missed_checkouts(transactions,travels)



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

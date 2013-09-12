#!/usr/bin/python3.2

import sys
import os
import datetime
import ovdata
from collections import namedtuple

# Checkin/checkout event, has a time and a place
Event=namedtuple('Event', 'time place')

# Transaction (either adding credit or forgetting to checkout and getting 
# the fine). Has a time, a place and a price
Transaction=namedtuple('Transaction', 'time place price')

# Unparsed traveldata, as an itermediate step from converting the datafile to
# Trip objects. ci=checkin, co=checkout. klasse=dutch for class
Traveldata=namedtuple('Traveldata', 'ci_date ci_time ci_loc co_time co_loc price klasse product private_or_business notes')

# Unparsed transaction data, as an intermediate step
Transactiondata=namedtuple('Transactiondata', 'date time location price')

class Trip:
    """ Class for trip objects, ie a single travel movement
    """
    def __init__(self, dataline):
        # Get check in datetime
        dtime=_create_datetime(dataline.ci_date,dataline.ci_time)

        # Create checkin event
        self.checkin=Event(dtime,dataline.ci_loc)

        # Get check out datetime (date is only specified for checkin)
        dtime=_create_datetime(dataline.ci_date,dataline.co_time)

        # If the checkout was before the checkin, checkout was on 
        # the next day
        if dtime < self.checkin.time:
            dtime+=datetime.timedelta(days=1)

        # Create checkout event
        self.checkout=Event(dtime,dataline.co_loc)

        # Get the price, convert to decimal format and then to float
        self.price=float(dataline.price.replace(',','.'))

        # Other stuf, not sure what to do with this, but its in the data
        self.klasse = dataline.klasse
        self.product= dataline.product
        self.notes= dataline.notes

        # Duration of the trip
        self.duration=self.checkout.time-self.checkin.time
        
        # TODO self.discount=_determine_discount(self)
    
    def __str__(self):
        return "{}\t{:25}\t{}\t{:25}\t{}".format(self.checkin.time, self.checkin.place, self.checkout.time, self.checkout.place, self.price)

def _create_datetime(date,time):
        """ Converts strings date and time into a datetime object and returns it
        """
        day,month,year=date.split('-')

        # Check the format of the year (ie, 2013 or 13)
        if len(year) == 2:
            year="20"+year
        elif len(year) == 4:
            pass
        else:
            error("Warning, weird year format:{}".format(year))

        day,month,year=int(day),int(month),int(year)
        hour,minute=time.split(':')
        hour,minute=int(hour),int(minute)

        return datetime.datetime(year,month,day,hour,minute)

def error(*arguments):
    """
    Convienience function: behaves as print, but prints to stderr instead of stdout
    """
    for i in arguments:
        sys.stderr.write(str(i))
    sys.stderr.write('\n')

def xls_row_to_list(row):
    output=list()
    for field in row:
        output.append(field.value.strip())
    return output

def _ov_line_to_list(line):
    spline=line.split(';')
    # Remove quotes from each field, and trainling spaces/nulllines
    spline = [field.replace('"','').strip() for field in spline]
    return spline

def _ov_events_to_trip(checkin,checkout):
    check_in_date, check_in_time, check_in_loc = checkin[:3]
    check_out_date=checkout[0]
    check_out_time=checkout[3]
    check_out_loc=checkout[4]
    price=checkout[5]

    # Convert price to float
    price=price.replace(',','.')
    # price is negative
    price=-1*float(price)

    # Get checkin/checkout datetime objects
    check_in_datetime=_date_and_time(check_in_date,check_in_time)
    check_out_datetime=_date_and_time(check_out_date,check_out_time)
    t=Trip(check_in_datetime, check_in_loc, check_out_datetime, check_out_loc, price)
    return t

def _valid_ov_file(filename):
    fileIN=open(filename,'r')

    # Lets check if this is a well formatted csv file
    line=fileIN.readline()
    fileIN.close()
    spline=line.strip().split(';')
    if spline != ovdata.ov_header:
        return False
    else:
        return True

def _long_ov_file(filename):
    fileIN=open(filename,'r')
    # Skip header
    line=fileIN.readline()
    line=fileIN.readline()

    while line:
        spline=line.split(';')
        # Remove trailing newlines and enclosing quotes
        spline = [field.replace('"','').strip() for field in spline]

        # If a checkin time is specified for at least one trip
        if spline[1] != "":
            fileIN.close()
            return True
        
        line=fileIN.readline()

    fileIN.close()
    return False

def read_ov_travels_file(filename):
    # Lets check if this is a well formatted csv file
    if not _valid_ov_file(filename):
        error("Unable to recognise the csv file by the header, please file a bug")
        #error("{}\nis not equal to the expected\n{}".format(spline,ovdata.ov_header))
        return(travels,transactions)

    if _long_ov_file(filename):
        return _read_ov_long_travels_file(filename)
    else:
        _read_ov_short_travels_file(filename)

# TODO
def _read_ov_short_travels_file(filename):
        print("Reading short ov-datafiles is not yet implemented")
        exit()

def _read_ov_long_travels_file(filename):
    # TODO What if the file is in reverse from the default?
    travels=list()
    transactions=list()
    fileIN=open(filename,'r')
    #HEADER LINE
    line=fileIN.readline()
    #Second line
    line=fileIN.readline()

    # Reading the file is a bit messy, because for some rediculous reason 
    # ov-chipkaart.nl insists on printing the checkout event before the checkin event 
    while line:
        spline=_ov_line_to_list(line)

        # If the current line is a checkout, the next line is a checkin
        if spline[6] == "Reis":
            checkout_line=spline
            checkin_line=_ov_line_to_list(fileIN.readline())

            # Add checkin time to checkout line (which is the most complete line of the two)
            checkout_line[1]=checkin_line[1]

            # Add the iminus to the price
            checkout_line[5]='-'+checkout_line[5]

            # Remove the transaction type since we know its a trip
            del checkout_line[6]

            # Add empty field because data from ov-chipkaart.nl does not 
            # contain a private_or_business field
            checkout_line.append("")

            t=Traveldata(*checkout_line)
            
            travels.append(Trip(t))
            #travels.append(_ov_events_to_trip(checkin_event, checkout_event))
        else: # TODO what if it isn't a checkout?
            pass
        line=fileIN.readline()

    fileIN.close()
    return (travels,transactions)

def _determine_price(price_plus,price_minus):
        # Make sure plus and minus aren't specified at the same time
        price=None

        if (price_minus != "") and (price_plus != ""):
            error("Af en Bij cannot be specified at the same time")
            return price
        else:
            # What was the price of this trip
            if price_minus != "":
                price='-'+price_minus
            else:
                price=price_plus

        # Now convert to decimal, eg 6,75 to 6.75 so python doesnt choke
        price=price.replace(",",".")

        return float(price)
    
def _determine_checkin_checkout_time(date,check_in_time,check_out_time):
        # What was the check in time?
        check_in_time=_date_and_time(date,check_in_time)

        # What was the check out time, if present?
        if check_out_time == "":
            check_out_time=None
        else:
            check_out_time=_date_and_time(date,check_out_time)

        # If the checkout time is before the checkin time, the checkout was on the next day
        # TODO, check if both are not equal to None
        if check_out_time is not None and check_out_time is not None:
            if check_out_time < check_in_time:
                check_out_time += datetime.timedelta(days=1)

        return (check_in_time,check_out_time)

def _is_transaction(line):
    if line[7] == "Laadtransactie" or line[4] == "":
        return True
    else:
        return False

def create_transaction(line):
    # Time of the transaction
    date, time=line[:2]
    dtime=_create_datetime(date,time)

    # Location of the transaction
    place=line[2]

    # What is the credit change on the card
    # If we added credit to the card
    if line[7] == "Laadtransactie":
        price=float(line[6].replace(',','.'))
    else: # If we forgot to checkout, price was deducted
        price=-1*float(line[5].replace(',','.'))

    return Transaction(dtime, place, price)


def create_trip(line):
    # This function assumes that there only was a 'deduction' from the card, so the 'added' field is empty
    
    ci_date, ci_time, ci_loc, co_time, co_loc = line[:5]

    # Position 5 in the line is the 'deducted' column, so prefix the price with a minus
    price='-'+line[5]
    
    # Get the other relevant fields (ignore 'added' column and 'transaction type', since we already know its a trip
    klasse, product, private_or_business,notes = line[8:]

    # Intermediate format of the data, to avoid code duplications
    dataline=Traveldata(ci_date, ci_time, ci_loc, co_time, co_loc, price, klasse, product, private_or_business, notes)
    return Trip(dataline)

def read_ns_travels_file(filename):
    """
    Reads the specified xls filename, returns all trips in a list
    """
    import xlrd
    workbook=xlrd.open_workbook(filename)
    worksheet=workbook.sheet_by_name('Reistransacties')

    # Lets check if it is a well formatted xls file
    if xls_row_to_list(worksheet.row(0)) != ovdata.ns_header:   
        error("Unable to recognise the xls file by the header, please file a bug")
        error("{}\nis not equal to the expected\n{}".format(xls_row_to_list(worksheet.row(0)),ovdata.ns_header))
        exit(-1)

    # Store all trips
    travels=list()
    transactions=list()

    # Read all the trips, ignore first row as this is the header
    for row in range(1,worksheet.nrows):
        line=xls_row_to_list(worksheet.row(row))

        # If its a transaction (no checkout)
        if _is_transaction(line):
            transactions.append(create_transaction(line))
        else:
            travels.append(create_trip(line))

    return (travels,transactions)

def read_travels_csv_file(filename):
    """
    [DEPRICATED] Reads the specified csv filename, returns all trips in a list
    """

    fileIN=open(filename, 'r')

    # Read the first line
    line=fileIN.readline()

    # Try to guess the seperator
    separator=None
    for sep in [';', ',', '\t']:
        if line.strip().split(sep) == ns_header:
            separator=sep
            break
    else:
        error("I cannot recognise the specified file '{}', sorry.".format(filename))
        error("Try exporting the file to csv with a semicolon (;) as field separator")
        exit(-1)
        
    # Store all trips
    travels=list()

    # Read all the lines in the file
    # NOTE: entries in the file are not guaranteed to be ordered on time/date
    line=fileIN.readline()
    while line:
        # Remove trailing newline and split the line on the separator we found
        spline=line.split(separator)

        # If the line does not contain as many fields as the header, something is wrong
        if len(spline) != len(header):
            error("Error, invalid line detected:\n{}".format(line))

        # Unpack the split line, and make a Trip object out of it
        travels.append(Trip(*spline))
        line=fileIN.readline()

    # Close the file
    fileIN.close()
    return travels

def transactions_total(travels):
    """
    Print to total of all transactions. Returns a tuple with the added and 
    deducted total.
    """
    added=0
    deducted=0
    for trip in travels:    
        if trip.price > 0:
            added+=trip.price
        else:   
            deducted+=trip.price

    return(round(added,2),round(deducted,2))
    
def get_missing_checkout(transactions):
    """
    Returns a list of all trips where the user forgot the check out.
    """
    missing_checkout=list()

    for transaction in transactions:
        # If there is no checkout
        if transaction.price == -10.0:
            missing_checkout.append(transaction)

    return missing_checkout
            
def minimum_travel_times(travels):  
    minimum_times=dict()

    for trip in travels:    
        key=(trip.checkin.place, trip.checkout.place)
        if key not in minimum_times.keys(): 
            minimum_times[key]=trip.duration
        else:   
            minimum_times[key]=min(minimum_times[key],trip.duration)

    return minimum_times

def possible_delays(travels):
    delays=list()
    min_times=minimum_travel_times(travels)
    
    for trip in travels:
        key=(trip.checkin.place, trip.checkout.place)
        if trip.duration > min_times[key] + datetime.timedelta(minutes=30):
            delays.append(trip)

    return delays

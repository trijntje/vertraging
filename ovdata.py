#!/usr/bin/python3.2

import datetime

"""
This is where some data needed by ovnl is stored. Things like file headers,
card types, when the travel schedule changes etc
"""

# Header for valid xls datafile for the NS
ns_header=['Datum', 'Check in', 'Vertrek', 'Check uit', 'Bestemming', 'Af', 'Bij', 'Transactie', 'Kl', 'Product', 'Prive/ Zakelijk', 'Opmerking']

# Header for valid csv datafile for ov-chipkaart.nl
ov_header=['"Datum"', '"Check-in"', '"Vertrek"', '"Check-uit"', '"Bestemming"', '"Bedrag"', '"Transactie"', '"Klasse"', '"Product"', '"Opmerkingen"']

# Formatting
place_width=25
# Different products that can be loaded on a card
# Tuple speciefies the times between which the user can travel with a discount TODO add weekeind
product={"Reizen op Saldo NS Korting":[datetime.time(hour=0),datetime.time(hour=3),(datetime.time(hour=8,minute=55),datetime. time(hour=23,minute=59,second=59))]}

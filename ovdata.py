#!/usr/bin/python3.2

"""
This is where some data needed by ovnl is stored. Things like file headers,
card types, when the travel schedule changes etc
"""

# Header for valid xls datafile for the NS
ns_header=['Datum', 'Check in', 'Vertrek', 'Check uit', 'Bestemming', 'Af', 'Bij', 'Transactie', 'Kl', 'Product', 'Prive/ Zakelijk', 'Opmerking']

# Header for valid csv datafile for ov-chipkaart.nl
ov_header=['"Datum"', '"Check-in"', '"Vertrek"', '"Check-uit"', '"Bestemming"', '"Bedrag"', '"Transactie"', '"Klasse"', '"Product"', '"Opmerkingen"']

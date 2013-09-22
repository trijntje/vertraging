vertraging
==========
Programma om reisgegevens van de OV-chipkaart te analyseren

==Installatie==
Dit programma heeft het pakket python-xlrd nodig. (sudo apt-get install python-xlrd)

==Uitvoeren==
Download de reisdata van je ov-kaart, van ns.nl of ov-chipkaart.nl
python ./travels.py /pad/naar/reisdata.xls

==Achtergrond==
Dit programma ondersteunt reisdata van ns.nl (xls) en ov-chipkaart.nl (csv). Dit programma gebruikt de reisdata om te leren hoe lang een reis tussen twee stations duurt, en geeft een melding als een reis meer dan een half uur langer duurt.

Momenteel is het nog een command-line only programma.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import csv
from datetime import datetime
from imagen_databank import PSC2_FROM_PSC1
from imagen_databank import DOB_FROM_PSC1
import logging
logging.basicConfig(level=logging.INFO)

IMAGEN_PATHWAYS_PSC1 = '/neurospin/imagen/PATHWAYS/RAW/PSC1/IP_hair_analysis_2019-02-18.csv'
IMAGEN_PATHWAYS_PSC2 = '/neurospin/imagen/PATHWAYS/RAW/PSC2/IP_hair_analysis_2019-02-18.csv'


def main():
    with open(IMAGEN_PATHWAYS_PSC1, newline='') as psc1_file:
        psc1_reader = csv.DictReader(psc1_file, dialect='excel')
        psc1_columns = [key for key in psc1_reader.fieldnames
                        if 'Code' in key]
        date_columns = [key for key in psc1_reader.fieldnames
                        if 'Date' in key]
        with open(IMAGEN_PATHWAYS_PSC2, 'w', newline='') as psc2_file:
            psc2_writer = csv.DictWriter(psc2_file,
                                         fieldnames=psc1_reader.fieldnames,
                                         quoting=csv.QUOTE_MINIMAL)
            psc2_writer.writeheader()
            for row in psc1_reader:
                for column in psc1_columns:
                    psc1 = row[column]
                    if not psc1.startswith('0'):
                        psc1 = '0' + psc1
                    if psc1 in PSC2_FROM_PSC1:
                        row[column] = PSC2_FROM_PSC1[psc1]
                    else:
                        logging.error('%s: invalid "%s"',
                                      psc1, column)
                        row[column] = ''
                
                if psc1 in DOB_FROM_PSC1:
                    for column in date_columns:
                        if row[column]:
                            try:
                                timestamp = datetime.strptime(row[column],
                                                              '%d.%m.%Y')
                            except ValueError:
                                try:
                                    timestamp = datetime.strptime(row[column],
                                                                  '%d.%m.%y')
                                except ValueError:
                                    logging.error('%s: invalid "%s": %s',
                                                  psc1, column, row[column])
                                    timestamp = None
                            if timestamp:
                                age = timestamp.date() - DOB_FROM_PSC1[psc1]
                                row[column] = str(age.days)
                            else:
                                row[column] = ''
                else:
                        logging.warning('%s: unknown date of birth', psc1)

                psc2_writer.writerow(row)


if __name__ == "__main__":
    main()

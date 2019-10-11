#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
from datetime import datetime
from operator import itemgetter
from imagen_databank import PSC2_FROM_PSC1
from imagen_databank import DOB_FROM_PSC1
import logging
logging.basicConfig(level=logging.INFO)

PATHWAYS_SURVEY_PSC1 = '/neurospin/imagen/PATHWAYS/RAW/PSC1/IMAGENpathways.surveydata.csv'
PATHWAYS_SURVEY_PSC2 = '/neurospin/imagen/PATHWAYS/RAW/PSC2/surveydata.csv'


def main():
    with open(PATHWAYS_SURVEY_PSC1, newline='', encoding='latin_1') as psc1_file:
        psc1_reader = csv.DictReader(psc1_file, dialect='excel')

        rows = []
        for row in psc1_reader:
            psc1 = row['PSC1id']
            if psc1 in PSC2_FROM_PSC1:
                row['PSC2'] = PSC2_FROM_PSC1[psc1]
            else:
                logging.error('%s: invalid "PSC1id"', psc1)
                row['PSC2'] = ''
            del row['PSC1id']
            del row['UserID']
            for column in psc1_reader.fieldnames:
                if '.date' in column:
                    try:
                        timestamp = datetime.strptime(row[column],  # fromisoformat() in Python 3.7
                                                      '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        row[column] = ''
                    else:
                        if psc1 in DOB_FROM_PSC1:
                            dob = DOB_FROM_PSC1[psc1]
                            age = timestamp.date() - dob
                            row[column] = age.days
                        else:
                            logging.error('%s: missing date of birth', psc1)
                            row[column] = ''
            rows.append(row)

        psc2_writer_fieldnames = [x if x != 'PSC1id' else 'PSC2'
                                  for x in psc1_reader.fieldnames
                                  if x != 'UserID']

        rows = sorted(rows, key=itemgetter('PSC2'))

        with open(PATHWAYS_SURVEY_PSC2, 'w', newline='', encoding='latin_1') as psc2_file:
            psc2_writer = csv.DictWriter(psc2_file,
                                         fieldnames=psc2_writer_fieldnames,
                                         quoting=csv.QUOTE_MINIMAL)
            psc2_writer.writeheader()
            for row in rows:
                psc2_writer.writerow(row)


if __name__ == "__main__":
    main()

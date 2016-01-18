#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import glob
import os
import sys

input_path = sys.argv[1]
output_file = sys.argv[2]

#Argument: . pour traiter l'ensemble des fichiers du dossier ou se trouve le script
#Attention: le nom fichier cible doit le faire apparaitre avant les fichiers a traiter ex. 01_

filewriter = csv.writer(open(output_file,'wb'))
file_counter = 0
row_counter = 0
for input_file in glob.glob(os.path.join(input_path,'*.csv')):
        with open(input_file,'rU') as csv_file:
                filereader = csv.reader(csv_file)
                if file_counter < 1:
                        for row in filereader:
                                filewriter.writerow(row)
                                row_counter+=1
                                print(row_counter)
                else:
                        header = next(filereader,None)
                        for row in filereader:
                                filewriter.writerow(row)
                                row_counter+=1
                                print(row_counter, input_file)
        file_counter += 1
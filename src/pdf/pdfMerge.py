#!/usr/bin/python

from PyPDF2 import PdfMerger

#Create an instance of PdfFileMerger() class
merger = PdfMerger()

#Create a list with the file paths
pdf_files = ['pdf_files/Astraknots It\'s Just A Phase Moon Phase Headband.pdf', 'pdf_files/Moon-Phase-Headband Chart.pdf']

#Iterate over the list of the file paths
for pdf_file in pdf_files:
    #Append PDF files
    merger.append(pdf_file)

#Write out the merged PDF file
merger.write("pdf_files/Astraknots It's Just A Phase Moon Phase Headband Chart and Written Instructions Full.pdf")
merger.close()
#!/usr/bin/python

from PyPDF2 import PdfMerger

#Create an instance of PdfFileMerger() class
merger = PdfMerger()

#Create a list with the file paths
pdf_files = ['pdf_files/Astraknots Alli\'s Ribbon Hat Pattern Written Instructions.pdf', 'pdf_files/Alli\'s-Ribbon-hat_chart_with_legend_final.pdf']

#Iterate over the list of the file paths
for pdf_file in pdf_files:
    #Append PDF files
    merger.append(pdf_file)

#Write out the merged PDF file
merger.write("pdf_files/Astraknots_Alli's Ribbon Hat Pattern Chart and Written Instructions Full.pdf")
merger.close()
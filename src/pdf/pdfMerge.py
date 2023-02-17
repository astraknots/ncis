#!/usr/bin/python

from PyPDF2 import PdfFileMerger

#Create an instance of PdfFileMerger() class
merger = PdfFileMerger()

#Create a list with the file paths
pdf_files = ['pdf_files/Astraknots CO Mtn Sunset Hat.pdf', 'pdf_files/CO Flag Mtn Sun w Legend.pdf']

#Iterate over the list of the file paths
for pdf_file in pdf_files:
    #Append PDF files
    merger.append(pdf_file)

#Write out the merged PDF file
merger.write("pdf_files/Astraknots_CO_Mtn_Sunset_hat_w_chart.pdf")
merger.close()
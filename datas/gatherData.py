import pandas as pd
import matplotlib.pyplot as plt
import PyPDF2, re

#import lxml, html5lib, beautifulsoup4

#dfAstraFall = pandas.read_csv('./Astrology Knitting Dignity - Fall.csv')

#print(dfAstraFall)

knitDigFile = pd.ExcelFile('./Astrology Knitting Dignity.xlsx')
kdf_sheet_names = knitDigFile.sheet_names
#print(kdf_sheet_names)

dfAstra = {}
for sheet_name in kdf_sheet_names:
    dfa_sheet = pd.read_excel('./Astrology Knitting Dignity.xlsx', sheet_name)
    dfAstra[sheet_name] = dfa_sheet

#print(dfAstra)

gkAstraHtmlFile = pd.read_html('./GKNatal Chart Report.html')
print(gkAstraHtmlFile)


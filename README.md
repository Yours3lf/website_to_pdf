# website_to_pdf
a python project to convert websites recursively to pdf

author: Marton Tamas
created: 2015. 05. 03.
description: This script recursively crawls websites and converts them to pdf files. The concatenates those files to form a book.
notes: feel free to modify in case of unexpected behaviour or crash
licence: MIT licence applies
usage: website_to_pdf.py -o OUTFILE -u URL

depends on:
pdfkit: https://pypi.python.org/pypi/pdfkit
you need to install pdftk-server (and restart after that, so that the PATH envvar works)
https://www.pdflabs.com/tools/pdftk-server/
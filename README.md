# website_to_pdf
a python project to convert websites recursively to pdf

author: Marton Tamas <br> created: 2015. 05. 03. <br> description: This script recursively crawls websites and converts them to pdf files. The concatenates those files to form a book. <br> notes: feel free to modify in case of unexpected behaviour or crash <br> licence: MIT licence applies <br> usage: website_to_pdf.py -o OUTFILE -u URL <br>

depends on: pdfkit: [https://pypi.python.org/pypi/pdfkit](https://pypi.python.org/pypi/pdfkit) <br> you need to install pdftk-server (and restart after that, so that the PATH envvar works) <br> [https://www.pdflabs.com/tools/pdftk-server/](https://www.pdflabs.com/tools/pdftk-server/)

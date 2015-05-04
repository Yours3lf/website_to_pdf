# author: Marton Tamas
#created: 2015. 05. 03.
#description: This script recursively crawls websites and converts them to pdf files. The concatenates those files to form a book.
#notes: feel free to modify in case of unexpected behaviour or crash
#licence: MIT licence applies
#usage: website_to_pdf.py -o OUTFILE -u URL

#depends on:
#pdfkit: https://pypi.python.org/pypi/pdfkit
#you need to install pdftk-server (and restart after that, so that the PATH envvar works)
#https://www.pdflabs.com/tools/pdftk-server/

import re
import urllib.request
import urllib.parse
import pprint
import sys, getopt
import os
import pdfkit
import subprocess
import shutil

outputfile = 'out.pdf'
#url = 'http://www.dataorienteddesign.com/dodmain/'
url = 'http://google.com/'
help_str = 'website_to_pdf.py -o OUTFILE -u URL'
max_depth = 100

try:
  #first argument is this file's name, ignore
  opts, args = getopt.getopt( sys.argv[1:], "o:u:" )
except getopt.GetoptError:
  #in case argument parsing failed
  print( 'ERROR: argument parsing failed. try:' )
  print( help_str )
  exit( 2 )
for opt, arg in opts:
  if opt == '-o':
    outputfile = arg
  elif opt == '-u':
    url = arg

#sanitize filename
file_pattern = re.compile( '([A-Za-z0-9\.\-_]*)' )
#matching never throws exception
outputfile = file_pattern.match( outputfile ).group( 0 )

#if outputfile is empty, there's no valid filename obviously
if len( outputfile ) < 1:
  print( help_str )
  print( 'ERROR: you must specify a proper output file name' )
  exit( 1 )

###
# now output file is valid
###
alt_outputfile = outputfile
alt_outputfile = alt_outputfile[:alt_outputfile.rfind( '.' )] + '_alt.pdf'
base_o = urllib.parse.urlparse( url )
visited_websites = []

good_file_extensions = ['.asp', '.aspx', '.htm', '.html', '.jsp', '.php', '.xhtml', '.cshtml', '.xhtm']


def crawl( base_url, depth ):
  if base_url in visited_websites:
    return
  else:
    visited_websites.append( base_url )

  o = urllib.parse.urlparse( base_url )

  if base_o.netloc != o.netloc:
    return

  if depth >= max_depth:  #prevent stack overflow
    return

  if o.path.rfind( '.' ) != -1:
    extension = o.path[o.path.rfind( '.' ):]
    if not extension in good_file_extensions:
      return

  #pprint.pprint(o)
  pprint.pprint( base_url )

  try:  #prevent html errors eg. 404
    try:
      if not os.path.isfile( alt_outputfile ):  #file exists
        pdfkit.from_url( base_url, alt_outputfile, { 'quiet': '' } )
      else:
        pdfkit.from_url( base_url, 'tmp.pdf', { 'quiet': '' } )
    except OSError:
      None

    if os.path.isfile( alt_outputfile ) and os.path.isfile( 'tmp.pdf' ):  #file exists
      subprocess.call( 'pdftk A=' + alt_outputfile + ' B=tmp.pdf cat A1-end B1-end output ' + outputfile )

    if os.path.isfile( alt_outputfile ) and os.path.isfile( outputfile ):
      shutil.copyfile( outputfile, alt_outputfile )
    elif os.path.isfile( alt_outputfile ):
      shutil.copyfile( alt_outputfile, outputfile )

    html = ''
    with urllib.request.urlopen( base_url ) as response:
      html = response.read( ).decode( "utf-8" )

    list = re.findall( '''href=["'](.[^"']+)["']''', html, re.I )
    for i in list:
      next_o = urllib.parse.urlparse( i )

      nexturl = ''
      if next_o.scheme == '':  #if relative path
        nexturl = base_o.scheme + '://' + base_o.netloc + base_o.path
        if base_o.path[-1:] != '/' and next_o.path[0:1] != '/':
          nexturl += '/'
          nexturl += next_o.path
        elif base_o.path[-1:] == '/' and next_o.path[0:1] == '/':
          nexturl += next_o.path[1:]
        else:
          nexturl += next_o.path

        if next_o.query != '':
          nexturl += '?' + next_o.query
      else:  #absolute path
        nexturl = i

      crawl( nexturl, depth + 1 )
  except urllib.error.HTTPError as e:
    pprint.pprint( e )
    return
  except:
    pprint.pprint( 'Unknown error: ' + base_url )
    return


crawl( url, 0 )

try:
  os.remove( alt_outputfile )
  os.remove( 'tmp.pdf' )
except:
  None
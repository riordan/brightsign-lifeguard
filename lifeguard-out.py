from __future__ import print_function
import shutil
import os
import xml.etree.cElementTree as ElementTree
import argparse
import logging
from copyfile import copyFile


parser = argparse.ArgumentParser()
parser.add_argument("presentation_directory",
    help="Root directory containing Brightsign presentation (current-sync.xml + pool/).")
args = parser.parse_args()
PRESENTATION_LOCATION = args.presentation_directory


if os.path.isdir(PRESENTATION_LOCATION):
    if PRESENTATION_LOCATION[-1] != '/':
        PRESENTATION_LOCATION = PRESENTATION_LOCATION + '/'
else:
    print("ERROR: Target not a valid directory. (Sorry)")
    exit()

if not os.path.isdir(PRESENTATION_LOCATION+"kiddie_pool"):
    os.mkdir(PRESENTATION_LOCATION+"kiddie_pool")


if not os.path.isfile(PRESENTATION_LOCATION + 'current-sync.xml'):
    print("""Presentation directory is missing a current-sync.xml file.
        Probably not a full Brightsign Presentation folder""")


tree = ElementTree.parse(PRESENTATION_LOCATION + 'current-sync.xml')
root = tree.getroot()
baseurl = root.find('./meta/client/base').text
for elem in root.findall('.//download'):
    name = elem.find('.//name').text
    urlpath = elem.find('.//link').text
    filepath = PRESENTATION_LOCATION + urlpath[len(baseurl)+1:]

    copyFile(os.path.abspath(filepath), os.path.abspath(PRESENTATION_LOCATION+"kiddie_pool/"+name))

print("Adult swim is over. Presentation files are now in the kiddle_pool.")

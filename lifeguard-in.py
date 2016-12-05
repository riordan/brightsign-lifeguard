# Builds a Brightsign pool + current-sync.xml from a kiddie_pool directory
from __future__ import print_function
import shutil
import os
import xml.etree.cElementTree as ET
import argparse
import logging
import hashlib
from copyfile import copyFile



# FUNCTIONS

def sha1file(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()

def shapath(sha):
    return "pool/"+sha[-2]+"/"+sha[-1]+"/sha1-"+sha

# for Printing the XML correctly!
# Borrowed from http://effbot.org/zone/element-lib.htm#prettyprint
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


# PROGRAM
parser = argparse.ArgumentParser()
parser.add_argument("presentation_directory",
    help="Root directory containing Brightsign presentation with a kiddie_pool.")
args = parser.parse_args()
PRESENTATION_LOCATION = args.presentation_directory


if os.path.isdir(PRESENTATION_LOCATION):
    if PRESENTATION_LOCATION[-1] != '/':
        PRESENTATION_LOCATION = PRESENTATION_LOCATION + '/'
else:
    print("ERROR: Target not a valid directory. (Sorry)")
    exit()


##############################################################

tree = ET.parse(PRESENTATION_LOCATION + 'template-sync.xml')

root = tree.getroot()
baseurl = root.find('./meta/client/base').text
# THIS IS THE THING! MAKE SENSE OF THE MADNESS!

elfiles = ET.Element("files")


for f in os.listdir(PRESENTATION_LOCATION+"kiddie_pool"):

    pathf = PRESENTATION_LOCATION+"kiddie_pool/"+f
    filename, file_extension = os.path.splitext(pathf)
    if file_extension == '.brs' or file_extension == ".bsfw" or file_extension == ".rok": script = True
    else: script = False
    sha = sha1file(pathf)
    size = os.path.getsize(pathf)
    poolpath = PRESENTATION_LOCATION+shapath(sha)
    finalurl = baseurl+poolpath

    #print(f, pathf, sha, size, poolpath)

    # Copy the file
    #print(os.path.abspath(pathf), os.path.abspath(poolpath))
    #exit()
    copyFile(os.path.abspath(pathf), os.path.abspath(poolpath))

    # Build XML Element
    eldownload = ET.Element("download")

    elname = ET.Element("name")
    elname.text=f
    eldownload.append(elname)

    elhash = ET.Element("hash", {"method":"SHA1"})
    elhash.text = sha
    eldownload.append(elhash)

    elsize = ET.Element("size")
    elsize.text = str(size)
    eldownload.append(elsize)

    ellink = ET.Element("link")
    ellink.text = finalurl
    eldownload.append(ellink)

    elheaders = ET.Element("headers", {"inherit":"no"})
    eldownload.append(elheaders)

    elchargeable = ET.Element("chargeable")
    elchargeable.text="no"
    eldownload.append(elchargeable)

    if script:
        elgroup = ET.Element("group")
        elgroup.text = "script"
        eldownload.append(elgroup)

    elfiles.append(eldownload)

# Add the other footer elements

# Deletes
scripts = ["*.brs", "*.rok", "*.bsfw"]
for s in scripts:
    eldelete = ET.Element("delete")
    elpattern = ET.Element("pattern")
    elpattern.text = s
    eldelete.append(elpattern)
    elfiles.append(eldelete)

elignore = ET.Element("ignore")
elpattern = ET.Element("pattern")
elpattern.text = "*"
elignore.append(elpattern)
elfiles.append(elignore)

root.append(elfiles)

indent(root)
tree.write(PRESENTATION_LOCATION+'current-sync.xml', xml_declaration=True, encoding='utf-8')

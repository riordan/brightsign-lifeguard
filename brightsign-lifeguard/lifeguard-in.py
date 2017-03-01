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

def listfiles(base_directory):
    """
    returns list of tuples of:
    (relative paths of all files in base_directory, path names within base_directory)
    """

    filelist = []
    for root,directories, filenames, in os.walk(base_directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            name = filepath[len(base_directory):]
            filelist.append((filepath,name))

    return filelist

def theprogram():
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
    if not os.path.exists(os.path.join(PRESENTATION_LOCATION, 'current-sync.xml')):
        print("Missing a current-sync.xml file")
        exit()
    tree = ET.parse(PRESENTATION_LOCATION + 'current-sync.xml')

    root = tree.getroot()

    #If there's a <files> element, kill it
    try:
        root.remove(root.find('./files'))
        print("<files> found, replacing")
    except:
        print("Did not find a <files>. Passing")
        pass

    baseurl = root.find('./meta/client/base').text
    # THIS IS THE THING! MAKE SENSE OF THE MADNESS!

    elfiles = ET.Element("files")


    for fullpath, filename in listfiles(PRESENTATION_LOCATION+"kiddie_pool"):

        nil, file_extension = os.path.splitext(filename)
        if file_extension == '.brs' or file_extension == ".bsfw" or file_extension == ".rok": script = True
        else: script = False

        sha = sha1file(fullpath)
        size = os.path.getsize(fullpath)
        poolpath = PRESENTATION_LOCATION+shapath(sha)
        finalurl = baseurl+"/"+shapath(sha)

        #print(f, pathf, sha, size, poolpath)

        # Copy the file
        #print(os.path.abspath(pathf), os.path.abspath(poolpath))
        #exit()
        copyFile(os.path.abspath(fullpath), os.path.abspath(poolpath))

        # Build XML Element
        eldownload = ET.Element("download")

        elname = ET.Element("name")
        elname.text=filename[1:]
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


theprogram()

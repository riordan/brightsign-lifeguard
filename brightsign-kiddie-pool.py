import shutil
import os
import xml.etree.cElementTree as ElementTree
import argparse

# XML dictionary parsing because I'm laaaazy.
# Also so this doesn't require any kind of pip installs
# XML -> Dictionary code from Stack Overflow
# https://stackoverflow.com/questions/8933237/how-to-find-if-directory-exists-in-python
class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})

parser = argparse.ArgumentParser()
parser.add_argument("presentation_directory",
    help="Root directory containing Brightsign presentation (local-sync.xml + pool/).")
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


if not os.path.isfile(PRESENTATION_LOCATION + 'local-sync.xml'):
    print("""Presentation directory is missing a local-sync.xml file.
        Probably not a full Brightsign Presentation folder""")


tree = ElementTree.parse(PRESENTATION_LOCATION + 'local-sync.xml')
root = tree.getroot()
xmldict = XmlDictConfig(root)


for f in xmldict['files']['download']:
    try:
        link = f['link']
        name = f['name']
        shutil.copy2(PRESENTATION_LOCATION+link, PRESENTATION_LOCATION+"kiddie_pool/"+name)
    except:
        pass

print("Adult swim is over. Presentation files are now in the kiddle_pool.")

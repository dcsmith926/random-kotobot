"""
Utilities for working with teh JMdict file
"""

import gzip
import os
import random
import requests
import xml.etree.ElementTree as ET

FILENAME_GZ = 'JMdict_e.gz'
FILENAME_XML = 'JMdict_e.xml'

def download_JMdict():

    url = 'http://ftp.monash.edu/pub/nihongo/JMdict_e.gz'

    with open(FILENAME_GZ, 'wb') as f:
        r = requests.get(url)
        f.write(r.content)

    with gzip.open(FILENAME_GZ, 'rb') as gz_file:
        with open(FILENAME_XML, 'wb') as xml_file:
            xml_file.write(gz_file.read())
    
    os.remove(FILENAME_GZ)

def map_entry_to_dict(entry):

    d = {
        'senses': [],
    }

    for child in entry:

        tag = child.tag

        if tag == 'ent_seq':
            d['seq'] = child.text

        elif tag == 'k_ele':
            keb = child.find('keb')
            d['kanji'] = keb.text

        elif tag == 'r_ele':
            reb = child.find('reb')
            d['reading'] = reb.text

        elif tag == 'sense':
            sense = []
            for c in child:
                if c.tag == 'gloss':
                    sense.append(c.text)
            d['senses'].append(sense)
    
    return d

class JMDict_entry(object):

    def __init__(self, xml_tree_entry):
        self.d = map_entry_to_dict(xml_tree_entry)

    def __repr__(self):
        return self.to_string()

    def to_string(self, with_reading=False):

        kanji = self.d.get('kanji', None) 
        reading = self.d['reading'] 

        if kanji:
            if with_reading:
                return '{} ({})'.format(kanji, reading)
            else:
                return kanji
        else:
            return reading

    def get_definition(self):
        definition_parts = ['{}. {}'.format(i + 1, '; '.join(sense)) for i, sense in enumerate(self.d['senses'])]
        definition = '\n'.join(definition_parts)
        return '{}:\n{}'.format(self.to_string(with_reading=True), definition)

class JMDict(object):

    def __init__(self):
        if not os.path.isfile(FILENAME_XML):
            download_JMdict()
        tree = ET.parse(FILENAME_XML)
        self.tree = tree
        
    def random_entry(self):
        root = self.tree.getroot()
        i = random.randint(0, len(root) - 1)
        return JMDict_entry(root[i])

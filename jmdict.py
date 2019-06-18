"""
Utilities for working with the JMdict file
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

    # an entry element can have:
    # 0 or more kanji elements
    # 1 or more reading elements
    # 1 or more sense elements

    d = {
        'kanji': [],
        'readings': [],
        'senses': [],
    }

    for child in entry:

        tag = child.tag

        if tag == 'ent_seq':
            d['seq'] = child.text

        elif tag == 'k_ele':
            for c in child:
                if c.tag == 'keb':
                    d['kanji'].append(c.text)

        elif tag == 'r_ele':
            for c in child:
                if c.tag == 'reb':
                    d['readings'].append(c.text)

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

    def to_string(self, include_kanji='first', include_reading='first_if_no_kanji'):
        """
        We display only the text from this first kanji element listed, with all readings listed,
        or only the first reading listed if no kanji element exists
        by default.
        """

        kanji = self.d['kanji']
        kanji_text = None

        if len(kanji) > 0:
            if include_kanji == 'first':
                kanji_text = kanji[0]
            elif include_kanji == 'random':
                random.choice(kanji)
            elif include_kanji == 'all':
                kanji_text = ', '.join(kanji)

        readings = self.d['readings']

        if include_reading == 'first' or (include_reading == 'first_if_no_kanji' and kanji_text is None):
            reading_text = readings[0]
        elif include_reading == 'random':
            reading_text = random.choice(readings)
        else:
            reading_text = ', '.join(readings)

        if not kanji_text is None:
            return '{} ({})'.format(kanji_text, reading_text)
        else:
            return reading_text

    def get_definition(self):
        definition_parts = ['{}. {}'.format(i + 1, '; '.join(sense)) for i, sense in enumerate(self.d['senses'])]
        definition = '\n'.join(definition_parts)
        return '{}:\n{}'.format(self.to_string(), definition)

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

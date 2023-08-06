import unittest
import json
import os, os.path
import shutil
from rdflib import Graph, plugin
from rdflib.parser import Parser
from rdflib.serializer import Serializer
from sauce.imagenet.imagenet import ImagenetGenerator

class ImagenetGeneratorTestCase(unittest.TestCase):

    
    def setUp(self):
        #shutil.rmtree('./testoutput')
        self.generator = ImagenetGenerator('./testoutput','http://localhost:1080/synsets','http://localhost:1080/word')
        

    def tearDown(self):
        shutil.rmtree('./testoutput')


    def test_extraction(self):
        self.generator.extract()
        f = open("./testoutput/synsets.txt")
        assert len(f.readlines()) == 5
        assert len(os.listdir('./testoutput/raw')) == 5
        f.close()
        f2 = open("./testoutput/raw/n02119789.urls")
        assert len(f2.readlines()) == 3
        f2.close()

    def test_cleanse(self):
        self.generator.extract()
        self.generator.cleanse_synsets()
        assert len(os.listdir('./testoutput/cleansed')) == 5
        f = open("./testoutput/cleansed/n02119789.urls")
        assert len(f.readlines()) == 2
        f.close()

    def test_cleanse_with_maximum(self):
        self.generator.extract()
        self.generator.cleanse_synsets(1)
        assert len(os.listdir('./testoutput/cleansed')) == 5
        f = open("./testoutput/cleansed/n02119789.urls")
        assert len(f.readlines()) == 1
        f.close()

    def test_limit(self):
        self.generatorLimit = ImagenetGenerator('./testoutput','http://localhost:1080/synsets','http://localhost:1080/word/', limit=2)
        self.generatorLimit.extract()
        assert len(os.listdir('./testoutput/raw')) == 2